# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 16:16
# @Author  : zhang
# @Email   : 1114570651@qq.com
# @File    : public_method.PY
# @Software: PyCharm
import random
import string
import subprocess


def subprocess_run_cmd(cmd):
    pid = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return pid.stdout.decode()


def get_current_network(interface):
    result = subprocess_run_cmd(f'ip router')
    for line in result.split('\n'):
        line = line.strip('\n')
        if interface in line and 'link' in line:
            network = line.split('dev')[0].strip()
            return network
    return ''


def get_current_gateway():
    result = subprocess_run_cmd(f'ip router')
    for line in result.split('\n'):
        line = line.strip('\n')
        if 'default' in line:
            network = line.split('dev')[0].split('via')[0].strip()
            return network
    return ''


def get_random(length=10, has_digits=False, suffix=''):
    """
    生成随机字符串或生成指定后缀的文件
    :param length:
    :param has_digits:
    :param suffix:
    :return:
    """
    base_string = string.ascii_letters + string.ascii_lowercase
    if has_digits:
        base_string += string.digits
    random_str = ''.join(random.sample(base_string, length))
    if suffix != '':
        random_str += f'.{suffix}'
    return random_str
