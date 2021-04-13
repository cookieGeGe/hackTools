# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 13:12
# @Author  : zhang
# @Email   : 1114570651@qq.com
# @File    : main.PY
# @Software: PyCharm
from hostTool.hostDiscovery import HostDiscovery
from wifiTools.scanWifi import Wifi


def scan_wifi():
    wifi_tool = Wifi('wlan0')
    wifi_tool.sccan()


def discover_host():
    host = HostDiscovery('192.168.31.1/24')
    host.discovery()


def main():
    # discover_host()
    scan_wifi()

if __name__ == '__main__':
    main()
