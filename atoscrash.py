# -*- conding:utf-8 -*-
# @Time : 2021/3/11 15:05 
# @Author : shanshan
# @File : atoscrash.py

import os
import sys
import time

default_appName = "/Contents/Resources/DWARF/CCTVVideo"


def atos(dsym_dir_path, crash_file_path, arm_str="arm64"):
    """
    自动解析ios crash日志
    :param dsym_dir_path:
    :param crash_file_path:
    :param arm_str:
    :return:
    """
    dsym_dir_path = dsym_dir_path + default_appName
    str_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    # 读取 crash 文件,正常写入到result中,如果遇到需要解析的堆栈,需要解析后,将解析后的内容再写到result文件中
    with open(crash_file_path, 'r')as fr:
        for i in fr:
            list_i = i.split()
            with open(str(str_time) + "result.crash", 'a+')as fw:
                # 判断有加号,而且分割后第三个元素和第四个元素是 0x 开头
                if "+" in i and list_i[2].startswith("0x") and list_i[3].startswith("0x"):
                    atos_result = os.popen(
                        f"atos -arch {arm_str} -o {dsym_dir_path} -l {list_i[3]} {list_i[2]}").read()
                    new_line_list = str(i.split('0x')[0]) + str(atos_result)
                    fw.write(new_line_list)
                else:
                    fw.write(i)


def check_params():
    "注意:堆栈信息的文件名不要有空格"
    try:
        assert sys.argv[1].endswith(".app.dSYM")  # 判断是否是符号表
        assert os.access(sys.argv[2], os.R_OK)  # 判断是否可读
        if len(sys.argv) == 3:
            atos(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 4:
            atos(sys.argv[1], sys.argv[2], arm_str=sys.argv[3])
    except Exception as e:
        print(e.args)


if __name__ == '__main__':
    # dsym_dir_path = sys.argv[1]  # .app.dSYM符号表的文件路径
    # crash_file_path = sys.argv[2]  # crash文件路径(可以是导出的 crash 文件路径,也可是待解析的原始堆栈)
    # arm_str = sys.argv[3]  # 架构名
    check_params()
