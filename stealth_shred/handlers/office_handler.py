import zipfile
import defusedxml.ElementTree as ET
from xml.etree.ElementTree import Element
import os
from .base import BaseHandler

class OfficeHandler(BaseHandler):
    def process(self, input_path, output_path):
        removed_fields = []
        try:
            with zipfile.ZipFile(input_path, 'r') as zin:
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
                    for item in zin.infolist():
                        content = zin.read(item.filename)
                        
                        if item.filename == 'docProps/core.xml':
                            content, fields = self._clean_core_xml(content)
                            if fields:
                                removed_fields.extend(fields)
                        elif item.filename == 'docProps/app.xml':
                            content, fields = self._clean_app_xml(content)
                            if fields:
                                removed_fields.extend(fields)
                                
                        zout.writestr(item, content)
            
            return removed_fields
        except Exception as e:
            self.logger.log_error(input_path, f"Office processing failed: {e}")
            return None

    def _clean_core_xml(self, content):
        """
        Sanitize core properties (Author, LastModifiedBy, Dates).
        """
        try:
            root = ET.fromstring(content)
            namespaces = {
                'dc': 'http://purl.org/dc/elements/1.1/',
                'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
                'dcterms': 'http://purl.org/dc/terms/'
            }
            
            fields_removed = []
            
            # Fields to clear
            targets = [
                ('dc:creator', 'Author'),
                ('cp:lastModifiedBy', 'Last Modified By'),
                ('cp:revision', 'Revision Number'),
                ('dcterms:created', 'Creation Date'),
                ('dcterms:modified', 'Modification Date'),
                ('dc:title', 'Title'),
                ('dc:subject', 'Subject'),
                ('dc:description', 'Description')
            ]
            
            for tag, name in targets:
                # Find handling namespaces manually is annoying with ElementTree simple find
                # So we iterate and check tag ends with...
                # Actually defusedxml behaves like standard ET
                
                # Simple logic: iterate all elements and match tags
                for elem in root.iter():
                    if self._match_tag(elem.tag, tag):
                        if elem.text:
                            fields_removed.append(name)
                            elem.text = ""
                            
            return ET.tostring(root, encoding='utf-8'), fields_removed
        except Exception:
            return content, []

    def _clean_app_xml(self, content):
        """
        Sanitize app properties (TotalTime, Company).
        """
        try:
            root = ET.fromstring(content)
            fields_removed = []
            
            targets = [
                ('TotalTime', 'Editing Time'),
                ('Company', 'Company'),
                ('Manager', 'Manager')
            ]
            
            for elem in root.iter():
                for tag, name in targets:
                    if elem.tag.endswith(tag):
                        if elem.text and elem.text != "0": # Don't log if already 0
                            fields_removed.append(name)
                            # Reset to empty or zero
                            if tag == 'TotalTime':
                                elem.text = "0"
                            else:
                                elem.text = ""
                                
            return ET.tostring(root, encoding='utf-8'), fields_removed
        except Exception:
            return content, []

    def _match_tag(self, elem_tag, target_tag):
        # target_tag is like 'dc:creator'
        # elem_tag is like '{http://purl.org/dc/elements/1.1/}creator'
        parts = target_tag.split(':')
        local_name = parts[-1]
        return elem_tag.endswith(f"}}{local_name}")
