# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 16:44
# @Author  : zhang
# @Email   : 1114570651@qq.com
# @File    : parseXml.PY
# @Software: PyCharm
try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET


class ParseXml(object):

    def __init__(self, xml):
        self.xml = xml

    def get_node_data(self, node):
        xml_data = {}
        xml_data.update(node.attrib)
        xml_data['tag'] = node.tag
        xml_data['text'] = node.text
        xml_data['children'] = []
        for child in node:
            child_data = self.get_node_data(child)
            # print(child_data)
            xml_data['children'].append(child_data)
        return xml_data

    def parse(self):
        try:
            tree = ET.parse(self.xml)
            root = tree.getroot()
            data = self.get_node_data(root)
            # print(data)
        except Exception as e:
            print(e)
            data = {}
        return data

    def get_tag_nodes(self, tag: str, data: list, field='tag'):
        tags_node_list = []
        for node in data:
            if node.get(field, '') == tag:
                tags_node_list.append(node)
            if 'children' in node.keys():
                chidlren_tags = self.get_tag_nodes(tag, node.get('children', []))
                tags_node_list.extend(chidlren_tags)
        return tags_node_list

    def get_port_nodes(self, data: list):
        tags_node_list = []
        for node in data:
            if node.get('tag', '') == 'port':
                port_data = {
                    "port": node.get('portid'),
                    "portocol": node.get('protocol'),
                    "state": '',
                    "service": ''
                }
                for child in node.get('children', []):
                    if child['tag'] not in ['state', 'service']:
                        continue
                    get_key = child['tag']
                    if child['tag'] == 'service':
                        get_key = 'name'
                    port_data[child['tag']] = child[get_key]
                tags_node_list.append(port_data)
            if 'children' in node.keys():
                chidlren_tags = self.get_port_nodes(node.get('children', []))
                tags_node_list.extend(chidlren_tags)
        return tags_node_list


if __name__ == '__main__':
    test = ParseXml(r'/home/hacktools/temp/nfpaKGBokJ.xml')
    print(test.parse())
