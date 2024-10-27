import typing

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QWidget
from dialogs.config import STR_APP_NAME
from dialogs.converters import ExcelConverter, ImgConverter, WordConverter
from dialogs.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)

        font = QFont("Microsoft YaHei", 10, weight=QFont.Bold)
        self.setFont(font)
        self.setupUi(self)

        self.setWindowTitle(STR_APP_NAME)

        self.converters = dict(
            word=WordConverter(parent=self),
            img=ImgConverter(parent=self),
            excel=ExcelConverter(parent=self),
        )

        self.actionAbout.triggered.connect(self.on_about)
        self.actionAboutQt.triggered.connect(self.on_about_qt)

        self.pbImg2PDF.clicked.connect(self.on_img2pdf)
        self.pbWord2PDF.clicked.connect(self.on_word2pdf)
        self.pbExcel2PDF.clicked.connect(self.on_excel2pdf)

        self.last_directory = ""

    def _select_files(self, fmt: str) -> typing.List[str]:
        files = QFileDialog.getOpenFileNames(
            self, "选择文件", self.last_directory, fmt
        )[0]

        if not len(files):
            self.statusbar.showMessage("用户取消")
            return []
        else:
            return files

    def on_about(self):
        QMessageBox.about(
            self, "关于PDFTools", "PDF系列处理工具, 使用 PySide2 开发。"
        )

    def on_about_qt(self):
        QMessageBox.aboutQt(self)

    def on_img2pdf(self):
        self.converters["img"].convert()

    def on_word2pdf(self):
        self.converters["word"].convert()

    def on_excel2pdf(self):
        self.converters["excel"].convert()
