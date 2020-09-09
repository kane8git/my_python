# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6
# 主程序

import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(BASE_DIR)
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    from modules.actions import excute_from_command_line
    excute_from_command_line(sys.argv)




