# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：check_env.py
import subprocess


def check_java():
    try:
        proc = subprocess.Popen(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err, out = proc.communicate()
        if err or b'java version' not in out:
            print('没有装java环境')
            return False
        else:
            print('java环境检测通过')
            return True
    except OSError:
        print('没有装java环境')
        return False


if __name__ == '__main__':
    if not check_java():
        from hctest_install_help.install_java_env import java_env
