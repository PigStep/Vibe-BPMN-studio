from lxml import etree
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class BaseXmlBuilder:
    """
    Base class for working with XML via lxml.
    Handles low-level operations: creating elements, namespaces, saving.
    """

    def __init__(self, namespaces: Dict[str, str]):
        self._namespaces = namespaces
        self.root: Optional[etree.Element] = None
        self.tree: Optional[etree.ElementTree] = None

    def create_root(self, tag_name: str, ns_prefix: str, **attrs) -> etree.Element:
        """Creates the root element with nsmap."""
        full_tag = self._get_tag(ns_prefix, tag_name)
        # nsmap is only passed to the root
        self.root = etree.Element(full_tag, nsmap=self._namespaces, attrib=attrs)
        self.tree = etree.ElementTree(self.root)
        return self.root

    def create_element(
        self, parent: etree.Element, tag_name: str, ns_prefix: str, **attrs
    ) -> etree.Element:
        """Creates a child element."""
        full_tag = self._get_tag(ns_prefix, tag_name)
        # Clean attributes by removing None values
        clean_attrs = {k: str(v) for k, v in attrs.items() if v is not None}
        return etree.SubElement(parent, full_tag, attrib=clean_attrs)

    def _get_tag(self, prefix: str, name: str) -> str:
        """Formats {uri}tagname"""
        uri = self._namespaces.get(prefix)
        if not uri:
            raise ValueError(f"Prefix '{prefix}' not defined in namespaces")
        return f"{{{uri}}}{name}"

    def to_string(self, pretty_print=True) -> str:
        if self.root is None:
            return ""
        return etree.tostring(
            self.root, pretty_print=pretty_print, xml_declaration=True, encoding="utf-8"
        ).decode("utf-8")

    def save_to_file(self, filepath: str) -> bool:
        if self.tree is None:
            logger.error("XML Tree is not initialized")
            return False
        try:
            self.tree.write(
                filepath, pretty_print=True, xml_declaration=True, encoding="utf-8"
            )
            logger.info("Saved XML to %s", filepath)
            return True
        except Exception as e:
            logger.error("Failed to save XML: %s", e)
            return False
