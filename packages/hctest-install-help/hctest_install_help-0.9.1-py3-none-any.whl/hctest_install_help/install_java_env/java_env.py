# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：java_env.py
from hctest_install_help.package.unzip import *

JAVA_HOME_NAME = "JAVA_HOME"
jdk_zip_file = input("请输入你java/jdk/jre源文件(zip文件)绝对路径:\n")
save_path = input("请输入你想保存的位置(文件夹的绝对路径):\n")
jdk_path = None
if not save_path:
    home = get_home_path()
    target_path = os.path.abspath(home + r"\JAVA" if sys.platform == "win32" else home + r"/.JAVA")
    unzip(jdk_zip_file, target_path)

else:
    target_path = os.path.abspath(save_path)
    unzip(jdk_zip_file, target_path)

java_execute_name = "java.exe" if sys.platform == "win32" else "java"
for dir_path, dir_names, filenames in os.walk(target_path):
    for filename in filenames:
        if filename == java_execute_name:
            jdk_path = os.path.join(dir_path)
            break
if sys.platform == "win32":
    from hctest_install_help.package.windows_env import *
    import subprocess
    add_system_env_path(r"%JAVA_HOME%{}".format(jdk_path.replace(target_path, '')))
    add_system_env(JAVA_HOME_NAME, target_path)
    subprocess.call(["attrib", "+h", target_path])

else:
    from hctest_install_help.package.mac_env import *
    add_system_env_path(r"$JAVA_HOME{}".format(jdk_path.replace(target_path, '')))
    add_system_env(JAVA_HOME_NAME, target_path)
