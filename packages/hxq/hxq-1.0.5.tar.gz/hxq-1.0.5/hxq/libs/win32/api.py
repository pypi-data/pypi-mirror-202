# -*- coding: utf-8 -*-
# @Time    : 2023/4/5 12:51
# @Author  : hxq
# @Software: PyCharm
# @File    : api.py
import os
import getpass
import winshell


class API:
    def __init__(self):
        pass

    @property
    def desktop(self):
        """
        桌面路径
        """
        return winshell.desktop()

    @property
    def username(self):
        """
        系统用户名
        """
        return getpass.getuser()

    @staticmethod
    def start_file(path):
        """
        启动文件/应用
        """
        os.startfile(path)

    @property
    def startup_path(self):
        """
        自启动目录
        """
        startup_path = r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        return os.path.join(os.getenv("SystemDrive"), r"\users", self.username, startup_path)

    @staticmethod
    def create_shortcut(exe_path: str, shortcut_name: str, desc: str):
        """
        生成快捷方式
        :param exe_path: exe路径
        :param shortcut_name: 需要创建快捷方式的路径
        :param desc: 描述，鼠标放在图标上面会有提示
        :return:
        """
        if not shortcut_name.endswith('.lnk'):
            shortcut_name = shortcut_name + ".lnk"
        try:
            winshell.CreateShortcut(
                Path=shortcut_name,
                Target=exe_path,
                Icon=(exe_path, 0),
                Description=desc
            )
            return True
        except ImportError as err:
            print("'winshell' lib may not available on current os")
            print("error detail %s" % str(err))
        return False


if __name__ == '__main__':
    api = API()
    print(api.startup_path)
    print(api.start_file(api.startup_path))
    # bin_path = r"D:\InstallData\日常软件\XQ工具\XQ工具.exe"
    # link_path = api.startup_path + "\\tools"
    # api.create_shortcut(bin_path, link_path, "小工具")
