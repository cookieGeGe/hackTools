# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 13:12
# @Author  : zhang
# @Email   : 1114570651@qq.com
# @File    : scanWifi.PY
# @Software: PyCharm
import subprocess
import time
from copy import deepcopy

from tools.baseMethodClass import BaseMethodClass


class Wifi(BaseMethodClass):

    def __init__(self, interface: str):
        super(Wifi, self).__init__()
        self.interface = interface
        self.wifi_list = []

    def get_wifi_item(self, essid: str = "", bssid: str = "", singal: str = "", channel: int = 0):
        """

        :param essid:
        :param bssid:
        :param singal:
        :param channel:
        :return:
        """
        return {
            "essid": essid,
            "bssid": bssid,
            "singal": singal,
            "channel": channel,
        }

    def sccan(self):
        pid = subprocess.run(f"iwlist {self.interface} scan", shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        result = pid.stdout.decode('utf-8')
        parse_wifi = False
        wifi_item = {}
        for index, line in enumerate(result.split('\n')):
            line = line.strip('\n')
            if 'Address:' in line:
                parse_wifi = True
                if len(wifi_item) != 0:
                    self.wifi_list.append(deepcopy(wifi_item))
                bssid = line.split(': ')[-1].strip()
                wifi_item = {"bssid": bssid}
                continue
            if line == '' and len(wifi_item) > 0:
                self.wifi_list.append(wifi_item)
                wifi_item = {}
            if not parse_wifi:
                continue
            if "Channel:" in line:
                channel = int(line.split(':')[-1])
                wifi_item['channel'] = channel
            elif "Frequency" in line:
                freq = line.split(':')[-1].split('(')[0].strip()
                wifi_item['frequency'] = freq
            elif "Signal level" in line:
                signal = line.split('=')[-1].strip().split(' ')[0]
                wifi_item['signal'] = signal
            elif "Encryption key" in line:
                need_pass = line.split(':')[-1].strip()
                wifi_item['encryption'] = 1 if need_pass == 'on' else 0
            elif 'ESSID' in line:
                # eval()可以将b''格式的字符串直接转换为bytes
                essid = eval('b' + (line.split(':')[-1].replace('"', "'")))
                wifi_item['essid'] = essid.decode('utf-8')
            elif "IEEE 802.11" in line:
                protol = line.split('/')[-1].split(' ')
                wifi_item['proto'] = protol
            elif "Group Cipher" in line:
                cipher = line.split(":")[-1].strip()
                wifi_item['cipher'] = cipher
            elif "Pairwise Ciphers" in line:
                cipher = line.split(":")[-1].strip()
                wifi_item['pairwise'] = cipher
            elif "Authentication" in line:
                cipher = line.split(":")[-1].strip()
                wifi_item['auth'] = cipher
        head = ["ID", 'ESSID', 'BSSID', "ENCRYP", "SIG", 'CHAN', "CIP", "AUTH_METHOD"]
        rows = []
        for index, wifi in enumerate(self.wifi_list):
            rows.append([
                index,
                wifi.get('essid', ''),
                wifi.get('bssid', ''),
                "True" if wifi.get('encryption', 0) == 1 else "False",
                wifi.get('signal', ''),
                wifi.get('channel', ''),
                wifi.get('cipher', ''),
                wifi.get('auth', ''),
            ])
        self.print_table(head, rows)

    def connect(self):
        pass
