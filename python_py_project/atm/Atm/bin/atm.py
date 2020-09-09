# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

import os
import sys

# 都是取路径
# print(__file__)      #  相对 路径
# print(os.path.abspath(__file__))    # 取绝对 路径
# dirname 去掉最底层目录 路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)

sys.path.append(base_dir)

from core import main

if __name__ == '__main__':
    main.run()
