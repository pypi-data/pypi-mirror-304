import sys

from PySide2.QtWidgets import QApplication

from deps.CNMapViewer import CNMapViewer


def main():
    app = QApplication(sys.argv)
    win = CNMapViewer()
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
