# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 16:12
# @Author  : zhang
# @Email   : 1114570651@qq.com
# @File    : hostDiscovery.PY
# @Software: PyCharm
import os

from Config.Config import TEMP_DIR
from tools.baseMethodClass import BaseMethodClass
from tools.parseXml import ParseXml
from tools.public_method import subprocess_run_cmd, get_random


class HostDiscovery(BaseMethodClass):

    def __init__(self, network):
        super(HostDiscovery, self).__init__()
        self.network = network
        self.host_list = []

    def discovery(self):
        xml_file_name = get_random(has_digits=False, suffix='xml')
        xml_file_path = os.path.join(TEMP_DIR, xml_file_name)
        # print(xml_file_path)
        result = subprocess_run_cmd(f'nmap -sP {self.network} -oX {xml_file_path}')
        # print(result)
        # xml_file_path = r'/home/hacktools/temp/nfpaKGBokJ.xml'
        xml_parse_obj = ParseXml(xml_file_path)
        xml_json_data = xml_parse_obj.parse()
        children_data = xml_json_data.get('children', [])
        host_node_list = xml_parse_obj.get_tag_nodes('host', children_data)

        for host_node in host_node_list:
            node_children = host_node.get('children', [])
            ip = xml_parse_obj.get_tag_nodes('ipv4', node_children, 'addrtype')
            mac = xml_parse_obj.get_tag_nodes('mac', node_children, 'addrtype')
            hostname = xml_parse_obj.get_tag_nodes('hostname', node_children)
            ports = xml_parse_obj.get_port_nodes(node_children)
            host_data = {
                "ip": ip[0]['addr'] if ip else '',
                "mac": mac[0]['addr'] if mac else '',
                "hostname": hostname[0]['name'] if hostname else '',
                "ports": ports,
                "17010": '',
            }
            host_data['arch'] = self.get_arch(host_data['ip'])
            if host_data['ip'] != '':
                host_data['17010'] = self.get_17010(host_data['ip'])
            self.host_list.append(host_data)
        head_list = ["ID", "IP", "MAC", "HOSTNAME", "ARCH", "PORTS", "17010"]
        rows = []
        for index, host in enumerate(self.host_list):
            rows.append([
                index,
                host.get('ip'),
                host.get('mac'),
                host.get('hostname'),
                host.get('arch'),
                ','.join([str(port['port']) for port in host['ports']]),
                host.get('17010'),
            ])
        self.print_table(head_list, rows)
