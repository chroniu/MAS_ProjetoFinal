"""
script to initialize the project folders and files.
"""

import configs
import os
from pathlib import Path


def initialize():
    # cria os diretórios se não existirem
    for directory in [configs.original_DIR, configs.extracted_DIR, configs.csv_dir, configs.control_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)


    for log_file in [configs.downloaded_files, configs.processed_files, configs.correct_files, configs.error_files, configs.imported_files_60]:
        _file = Path(log_file)
        if _file.is_file():
            pass
        else:
            open(log_file, 'w+').close()
