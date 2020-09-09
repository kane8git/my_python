# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)


from core import ftp_server
from core import main
from config import settings

if __name__ == '__main__':
    a = main.Manager()
    a.interactive()























