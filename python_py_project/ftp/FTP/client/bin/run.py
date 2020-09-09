# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)


from core import ftp_client
from config import settings
if __name__ == '__main__':
    run = ftp_client.FTPClient(settings.ip_port)
    run.execute()






