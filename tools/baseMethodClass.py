# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 18:43
# @Author  : zhang
# @Email   : 1114570651@qq.com
# @File    : baseMethodClass.PY
# @Software: PyCharm
import os

from prettytable import PrettyTable

from Config.Config import SCRIPTS_DIR
from tools.public_method import subprocess_run_cmd


class BaseMethodClass(object):

    def __init__(self):
        pass

    def print_table(self, head, rows):
        pty_table = PrettyTable()
        pty_table.field_names = head
        pty_table.add_rows(rows)
        print(pty_table.get_string())

    def get_arch(self, host):
        result = subprocess_run_cmd(f'getArch.py -target {host}')
        if 'is 64-bit' in result:
            return '64-bit'
        elif 'is 32-bit' in result:
            return '32-bit'
        else:
            return 'unknown'

    def get_platform(self, host):
        pass

    def get_17010(self, host):
        scripts_file_path = os.path.join(SCRIPTS_DIR, 'smb_ms17_010.py')
        result = subprocess_run_cmd(f'python {scripts_file_path} {host}')
        if result.startswith('[+]'):
            return True
        return False
