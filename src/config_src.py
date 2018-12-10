import os
import sys

base_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[:-1][0]
sys.path.append(base_dir)

import config_global

config = config_global
