# -*- coding: utf-8 -*
"""
Config file path resolution
"""

import os
from xdg import BaseDirectory

def get_config_file():
	dir_full_path = BaseDirectory.save_data_path('codecook-bash.config')
	file_full_path = os.path.join(dir_full_path, 'user.config')
	return file_full_path