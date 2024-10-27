"""
功能：方法 103 升降法计算工具
"""
# import numpy

import sys

from PySide2.QtWidgets import QApplication

from depends.BrucetonDialog import BrucetonDialog


def main():
    app = QApplication(sys.argv)
    win = BrucetonDialog()
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
