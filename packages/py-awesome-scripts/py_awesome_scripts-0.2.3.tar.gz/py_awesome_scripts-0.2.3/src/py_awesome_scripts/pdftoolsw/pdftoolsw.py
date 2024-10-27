import sys
# import PIL

from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtWidgets import QApplication

from dialogs.mainwindow import MainWindow


def main():
    # 设置高分辨率缩放
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
