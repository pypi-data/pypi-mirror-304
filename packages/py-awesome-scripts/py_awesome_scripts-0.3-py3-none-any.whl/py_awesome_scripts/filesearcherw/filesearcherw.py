"""
功能: 用于实现各类文件中特定字符的识别。
特性:
- 支持文本文件: .py, .c, .txt, .md
- 支持OFFICE文件: .docx, .xls, .xlsx
- 支持压缩文件: .zip
"""
import sys

from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtWidgets import QApplication

from deps.gui.SearchWindow import SearchWindow


def main():
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    win = SearchWindow()
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
