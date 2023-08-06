# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：unzip.py

import zipfile
import os
import sys
import tarfile


def get_home_path():
    env_vars = os.environ
    home_path = "USERPROFILE" if sys.platform == "win32" else "HOME"
    return env_vars[home_path]


def unzip(source_path, target_path):
    if source_path.endswith("zip"):
        with zipfile.ZipFile(source_path, 'r') as zip_ref:
            zip_ref.extractall(target_path)
    else:
        with tarfile.open(source_path, "r:gz") as tar:
            tar.extractall(path=target_path)

    for root, dirs, files in os.walk(target_path):
        for file in files:
            os.chmod(os.path.join(root, file), 0o755)


if __name__ == '__main__':
    print(get_home_path())
