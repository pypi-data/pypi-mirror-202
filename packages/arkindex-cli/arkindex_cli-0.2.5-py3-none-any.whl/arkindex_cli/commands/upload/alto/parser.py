# -*- coding: utf-8 -*-
import json
import logging
from math import floor
from pathlib import Path
from typing import Optional

from apistar.exceptions import ErrorResponse
from lxml import etree as ET

logger = logging.getLogger(__name__)


class MetsProcessingError(Exception):
    """
    Raised when there has been an error in the Mets upload processing
    """


def _is_alto_namespace(namespace: str) -> bool:
    return (
        namespace.startswith("http://www.loc.gov/standards/alto/")
        # Older URLs for ALTO≤2.0
        or namespace.startswith("http://schema.ccs-gmbh.com/docworks/")
    )


class AltoElement:
    def __init__(
        self,
        node: ET.Element,
        page_width: Optional[int] = None,
        page_height: Optional[int] = None,
        alto_namespace: Optional[str] = None,
        unit: str = "pixel",
        dpi_x: Optional[int] = None,
        dpi_y: Optional[int] = None,
    ):
        if alto_namespace:
            self.namespaces = {"alto": alto_namespace}
        else:
            alto_namespaces = set(filter(_is_alto_namespace, node.nsmap.values()))

            if len(alto_namespaces) == 1:
                self.namespaces = {"alto": alto_namespaces.pop()}
            elif len(alto_namespaces) > 1:
                raise ValueError(f"Multiple ALTO namespaces found: {alto_namespaces}")
            else:
                raise ValueError("ALTO namespace not found")

        assert not (
            (dpi_x is None) ^ (dpi_y is None)
        ), "The horizontal and vertical resolutions must be both set or both unset."
        assert (
            dpi_x is None or dpi_x > 0
        ), "The horizontal resolution must be a strictly positive integer."
        assert (
            dpi_y is None or dpi_y > 0
        ), "The vertical resolution must be a strictly positive integer."

        assert unit in ("pixel", "mm10"), f"Unsupported measurement unit {unit}"
        if unit == "mm10":
            assert (
                dpi_x is not None and dpi_y is not None
            ), "The horizontal and vertical resolutions must be set to import ALTO elements using the mm10 unit."

        self.node_name = ET.QName(node).localname.lower()
        self.has_text = node.findall("{*}String", namespaces=self.namespaces)
        self.page_width = page_width or self.get_width(node)
        self.page_height = page_height or self.get_height(node)
        self.unit = unit
        self.dpi_x = dpi_x
        self.dpi_y = dpi_y
        # If there are more than one Page node in the file, the image id required
        # to build the IIIF url for the images is retrieved from the Page's
        # PHYSICAL_IMG_NR attribute and stored as page_image_id.
        self.page_image_id = self.get_page_image_id(node)
        self.content = node
        self.children = []

    def xml_int_value(self, node, attr_name):
        value = node.get(attr_name)
        if value is None:
            raise ValueError(f"Missing required value: {attr_name}")
        # The ALTO specification accepts float coordinates, but Arkindex only supports integers
        return round(float(value))

    def get_polygon_coordinates(self, node):
        if not (
            "HPOS" in node.attrib
            and "VPOS" in node.attrib
            and "WIDTH" in node.attrib
            and "HEIGHT" in node.attrib
        ):
            return

        # Skip elements with polygons with w or h <= 0 (invalid polygons)
        width = self.xml_int_value(node, "WIDTH")
        height = self.xml_int_value(node, "HEIGHT")
        if width <= 0 or height <= 0:
            return

        return {
            "x": self.xml_int_value(node, "HPOS"),
            "y": self.xml_int_value(node, "VPOS"),
            "width": width,
            "height": height,
        }

    def get_width(self, node):
        if "WIDTH" not in node.attrib:
            return
        return self.xml_int_value(node, "WIDTH")

    def get_height(self, node):
        if "HEIGHT" not in node.attrib:
            return
        return self.xml_int_value(node, "HEIGHT")

    def get_page_image_id(self, node):
        if "PHYSICAL_IMG_NR" not in node.attrib:
            return
        return node.get("PHYSICAL_IMG_NR")

    def ark_polygon(self, dict):
        """
        A polygon compatible with Arkindex.
        """
        if not dict:
            return None

        x, y, width, height = dict["x"], dict["y"], dict["width"], dict["height"]

        polygon = [
            [x, y],
            [x, y + height],
            [x + width, y + height],
            [x + width, y],
            [x, y],
        ]

        page_width, page_height = self.page_width, self.page_height

        # When using tenths of millimeters, we convert the coordinates to pixels
        if self.unit == "mm10":
            polygon = [
                [round(x * self.dpi_x / 254), round(y * self.dpi_y / 254)]
                for x, y in polygon
            ]
            # Also convert the page width and height, which also is in tenths of millimeters,
            # so we can trim the pixels properly and never go beyond the edges of the image
            page_width = floor(page_width * self.dpi_x / 254)
            page_height = floor(page_height * self.dpi_y / 254)

        # We trim the polygon of the element in the case where its dimensions are bigger than the dimensions of the image
        polygon = [
            [min(page_width, max(0, x)), min(page_height, max(0, y))]
            for x, y in polygon
        ]

        return polygon

    @property
    def has_children(self):
        return len(list(self.content)) > 0

    @property
    def polygon(self):
        return self.ark_polygon(self.get_polygon_coordinates(self.content))

    @property
    def width(self):
        return self.get_width(self.content)

    @property
    def height(self):
        return self.get_height(self.content)

    @property
    def name(self):
        return self.content.get("ID")

    def parse_children(self):
        if not self.has_children:
            return
        for child in self.content:
            child_element = AltoElement(
                child,
                page_width=self.page_width,
                page_height=self.page_height,
                alto_namespace=self.namespaces["alto"],
                unit=self.unit,
                dpi_x=self.dpi_x,
                dpi_y=self.dpi_y,
            )
            # String nodes are not sent to Arkindex as Elements, but their "CONTENT"
            # is sent as the transcription for their parent node.
            if child_element.node_name != "string":
                self.children.append(child_element)
                child_element.parse_children()

    def serialize(self):
        """
        Convert an Alto XML node and its children to a dictionary that will serve
        as a base for creating elements on Arkindex.
        """
        node_dict = {"type": self.node_name, "name": self.name, "children": []}
        if self.polygon:
            node_dict["polygon"] = self.polygon
        if len(self.has_text) > 0:
            full_text = " ".join(
                item.attrib["CONTENT"] for item in self.has_text
            ).strip()
            if len(full_text) > 0:
                node_dict["text"] = full_text
        if len(self.children):
            for item in self.children:
                node_dict["children"].append(item.serialize())
        return node_dict

    @property
    def serialized_children(self):
        return self.serialize()["children"]


class RootAltoElement(AltoElement):
    def __init__(
        self,
        node: ET.Element,
        alto_namespace: Optional[str] = None,
        dpi_x: Optional[int] = None,
        dpi_y: Optional[int] = None,
    ):
        super().__init__(node, alto_namespace=alto_namespace, dpi_x=dpi_x, dpi_y=dpi_y)

        # Retrieve the file's measurement unit, used to specify the image(s) and polygons
        # dimensions. We support tenths of millimeters only when the DPI are set, and pixels whenever.
        try:
            self.unit = node.find(
                "{*}Description/{*}MeasurementUnit", namespaces=self.namespaces
            ).text
        except AttributeError:
            raise ValueError("The MesurementUnit is missing.")

        assert self.unit in (
            "pixel",
            "mm10",
        ), f"Unsupported measurement unit {self.unit}"
        if self.unit == "mm10":
            assert (
                self.dpi_x is not None and self.dpi_y is not None
            ), "The horizontal and vertical resolutions are required to parse ALTO files using the `mm10` measurement unit."

        try:
            # Retrieve the fileName node, which contains the identifier required to build the
            # IIIF url for the image (if there is only one Page node in the file.)
            self.filename = node.find(
                "{*}Description/{*}sourceImageInformation/{*}fileName",
                namespaces=self.namespaces,
            ).text
            assert self.filename, "Missing image file name"
        except AttributeError:
            raise ValueError("The fileName node is missing.")


class MetsElement:
    def __init__(self, node) -> None:
        self.node = node
        """Root node of the METS tree
        """
        # Parse namespaces
        self.namespaces = node.nsmap

    @property
    def children(self):
        return self.node.findall("div", namespaces=self.namespaces)

    def publish_element(self, arkindex_client, parent_id, corpus_id):
        self.element_type = self.node.get("TYPE")
        # if LABEL attribute is set, it must be used as element name. Else try ORDER. Fallback to 1.
        self.element_name = self.node.get("LABEL") or self.node.get("ORDER") or "1"
        try:
            # Create Element no image under current parent
            logger.info(f"Creating {self.element_type} {self.element_name}…")
            self.arkindex_id = arkindex_client.request(
                "CreateElement",
                slim_output=True,
                body={
                    "type": self.element_type,
                    "name": self.element_name,
                    "corpus": str(corpus_id),
                    "parent": str(parent_id),
                },
            )["id"]
        except ErrorResponse as e:
            logger.error(
                f"Could not create element {self.node.attrib}: HTTP {e.status_code} - {e.content}"
            )
            raise MetsProcessingError

    def publish_metadata(self, arkindex_client):
        logger.info(f"Storing Alto ID metadata on element ({self.arkindex_id})…")
        try:
            # Store Alto ID as metadata
            arkindex_client.request(
                "CreateMetaData",
                id=self.arkindex_id,
                body={
                    "name": "Alto ID",
                    "value": self.node.get("ID"),
                    "type": "reference",
                },
            )

        except ErrorResponse as e:
            logger.error(
                f"Could not create metadata on element ({self.arkindex_id}): HTTP {e.status_code} - {e.content}"
            )
            raise MetsProcessingError

    def publish_lines(self, arkindex_client, files_mapping):
        lines = self.node.findall("fptr//area", namespaces=self.namespaces)
        if not lines:
            return

        logger.info(
            f"Publishing {len(lines)} children under {self.element_type} {self.element_name}…"
        )
        for area in lines:
            # Get file id
            file_id = area.get("FILEID")
            assert (
                file_id
            ), f"Could not find the `FILEID` attribute on area under div ({self.node.get('ID')})"
            # Get line_name
            line_name = area.get("BEGIN")
            assert (
                line_name
            ), f"Could not find the `BEGIN` attribute on area under div ({self.node.get('ID')})"
            # Get Arkindex element id
            arkindex_line_id = files_mapping.get(file_id).get(line_name)
            assert arkindex_line_id, f"Arkindex ID not found for line {line_name}"
            # Link element with child line
            logger.info(
                f"Linking element ({arkindex_line_id}) under {self.element_type} {self.element_name}…"
            )
            try:
                arkindex_client.request(
                    "CreateElementParent",
                    child=str(arkindex_line_id),
                    parent=str(self.arkindex_id),
                )
            except ErrorResponse as e:
                logger.error(
                    f"Could not link element ({arkindex_line_id}) to parent ({self.arkindex_id}): HTTP {e.status_code} - {e.content}"
                )
                raise MetsProcessingError

    def publish(self, arkindex_client, parent_id, corpus_id, files_mapping):
        # Create Element no image under current parent
        self.publish_element(
            arkindex_client=arkindex_client, parent_id=parent_id, corpus_id=corpus_id
        )
        # Store Alto ID as metadata
        self.publish_metadata(arkindex_client=arkindex_client)

        # Find any lines children
        self.publish_lines(arkindex_client=arkindex_client, files_mapping=files_mapping)

        # Add node children to the queue
        return (self.arkindex_id, self.children)


class RootMetsElement(MetsElement):
    def __init__(self, filepath, node):
        super().__init__(node)

        self.files_mapping = {}
        """Mapping from file_ids (as defined in the METS) to tuple of
        - path to ALTO xml file,
        - Loaded Arkindex summary.
        """
        self.root = node

        self.parse_files(filepath)

        # Parse <structMap TYPE="logical"> to get a tree
        self.node = self.root.find(
            "structMap[@TYPE='logical']", namespaces=self.namespaces
        )

    def parse_files(self, toc_file: Path):
        """Parse files listed in the METS file section, and parse their JSON summary.
        Raise if any of these JSON summaries is not found.
        """
        # Iterate over <file> in any <filesec>
        for file in self.root.findall(
            "fileSec/fileGrp/file", namespaces=self.namespaces
        ):
            try:
                location = file.find("FLocat", namespaces=self.namespaces)
                assert (
                    location is not None
                ), f"Could not find location of file ({file.get('ID')}) in METS."
                href = location.get("{" + self.namespaces.get("xlink") + "}href")

                file_path = (toc_file.parent / href).resolve()
                assert file_path.exists(), f"File corresponding to {href} not found."

                # Check that corresponding JSON summary exists
                summary = file_path.with_suffix(".json")
                assert (
                    summary.exists()
                ), f"JSON summary corresponding to {href} not found."
            except AssertionError as e:
                logger.error(
                    f"Could not parse file {file} ({file.get('ID')}): {str(e)}"
                )
                raise MetsProcessingError

            self.files_mapping[file.get("ID")] = json.load(open(summary))["elements"]

    def parse_object_types(self):
        # each <div> with a type will generate a new arkindex element
        return {
            element.get("TYPE")
            for element in self.node.findall(
                ".//div[@TYPE]", namespaces=self.namespaces
            )
        }

    def publish(self, arkindex_client, parent_id, corpus_id):
        """Build the hierarchy on Arkindex, browsing the tree in a breadth-first fashion

        :param arkindex_client: Arkindex API client.
        :param parent_id: Root element id on Arkindex.
        :param corpus_id: ID of the corpus where the element will be created
        """
        # Queue of (parent, children) tuples.
        children = [(parent_id, self.children)]
        while len(children):
            # Take first elements to publish, top of the queue
            parent, elements = children.pop(0)
            logger.info(
                f"Publishing {len(elements)} children under element ({parent})…"
            )
            # Create each element under current parent
            for element in elements:
                child = MetsElement(node=element)
                children.append(
                    child.publish(
                        arkindex_client=arkindex_client,
                        parent_id=parent,
                        corpus_id=corpus_id,
                        files_mapping=self.files_mapping,
                    )
                )
