# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

import os
import sys

BASE_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_dir)

from core import main


if __name__ == '__main__':
    obj = main.MainLogic()





