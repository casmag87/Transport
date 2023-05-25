import xml.etree.ElementTree as ET

class XMLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = ET.parse(file_path, parser=ET.XMLParser(encoding="utf-8"))
        self.namespace = {'netex': 'http://www.netex.org.uk/netex'}
    
    def get_tags_and_values(self, element, search_tag=None):
        tags_and_values = {}
        for child in element:
            if len(child) > 0:
                tags_and_values.update(self.get_tags_and_values(child, search_tag))
            else:
                if search_tag is None or child.tag == search_tag:
                    tags_and_values[child.tag.replace('{http://www.netex.org.uk/netex}', '')] = child.text
        return tags_and_values

    
    def parse(self, search_tag=None):
        root = self.tree.getroot()
        tags_and_values = {}
        for child in root:
            if len(child) > 0:
                tags_and_values.update(self.get_tags_and_values(child, search_tag))
            else:
                if search_tag is None or child.tag == search_tag:
                    tags_and_values[child.tag] = child.text
            for grandchild in child:
                if len(grandchild) > 0:
                    tags_and_values.update(self.get_tags_and_values(grandchild, search_tag))
                else:
                    if search_tag is None or grandchild.tag == search_tag:
                        tags_and_values[grandchild.tag] = grandchild.text
        return tags_and_values
    
    def print_all_tags(self):
        def recursive_print(element, depth=0):
            tag = element.tag.replace('{http://www.netex.org.uk/netex}', 'netex:')
            print(' ' * depth + tag)
            for child in element:
                recursive_print(child, depth+1)
        recursive_print(self.tree.getroot())

xml_parser = XMLParser('4a.xml')
tag_value = xml_parser.parse()
print(tag_value)