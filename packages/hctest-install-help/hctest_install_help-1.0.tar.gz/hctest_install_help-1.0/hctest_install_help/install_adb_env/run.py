# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：run.py


import sys
import os


def start_install_help():
    if sys.platform == "win32":
        from hctest_install_help.package.windows_env import run_cmd_as_admin
        check_file = str(__file__).replace(f"run.py", "check_env.py")
        run_cmd_as_admin(f'{sys.executable} {check_file}')

        env_file = str(__file__).replace(f"run.py", "adb_env.py")
        run_cmd_as_admin(f"{sys.executable} {env_file}")

    else:
        check_file = str(__file__).replace(f"run.py", "check_env.py")
        os.system(f'{sys.executable} {check_file}')

        env_file = str(__file__).replace(f"run.py", "adb_env.py")
        os.system(f'{sys.executable} {env_file}')
