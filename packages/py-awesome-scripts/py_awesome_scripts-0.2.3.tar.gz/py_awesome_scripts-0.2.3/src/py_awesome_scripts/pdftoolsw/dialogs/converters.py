import typing
from pathlib import Path

from PIL import Image
from PySide2.QtWidgets import QFileDialog, QMessageBox, QMainWindow


class Converter:
    fmt: str = "文件(*.*)"

    def __init__(self, parent: typing.Optional[QMainWindow] = None) -> None:
        super().__init__()

        self.parent: typing.Optional[QMainWindow] = parent

    def convert(self):
        pass

    def get_files(self) -> typing.List[str]:
        if self.parent is not None:
            self.parent.statusBar().showMessage("选择文件")
            files = QFileDialog.getOpenFileNames(
                self.parent, "选择文件", str(Path.cwd()), self.fmt
            )[0]
            if len(files):
                return files
            else:
                self.parent.statusBar().showMessage("用户取消")

        return []


class WordConverter(Converter):
    fmt = "文档(*.docx)"

    def convert(self):
        try:
            from docx2pdf import convert
        except ImportError as err:
            QMessageBox.warning(
                self.parent, "错误", f"缺少 docx2pdf 支持库! {err=}"
            )
            return

        if len(files := self.get_files()) > 0:
            for file in files:
                convert(str(Path(file)), str(Path(file).with_suffix(".pdf")))
            self.parent.statusBar().showMessage("转化结束")


class ImgConverter(Converter):
    fmt = "图片(*.png *.jpg *.jpeg *.bmp)"

    def convert(self):
        if len(files := self.get_files()) > 0:
            for file in files:
                img = Image.open(file)
                if file.endswith("png"):
                    r, g, b, a = img.split()
                    img = Image.merge("RGB", (r, g, b))
                    img.save(Path(file).with_suffix(".jpg"))
                else:
                    continue

            pdf_name = Path(files[0]).with_suffix(".pdf").as_posix()
            image_file = Image.open(files[0])
            image_list = (
                [Image.open(f) for f in files[1:]] if len(files) >= 2 else []
            )
            try:
                image_file.save(
                    pdf_name,
                    "PDF",
                    resolution=100.0,
                    save_all=True,
                    append_images=image_list,
                )
            except IOError as err:
                QMessageBox.critical(
                    self.parent, "错误", f"输出pdf文件失败, {pdf_name=}, {err=}"
                )
            else:
                self.parent.statusBar().showMessage(
                    f"转化结束， 输出pdf文件{pdf_name=}"
                )


class ExcelConverter(Converter):
    fmt = "表格(*.xlsx)"

    def convert(self):
        try:
            from win32com.client import DispatchEx
        except ImportError as err:
            QMessageBox.warning(
                self.parent, "错误", f"缺少 win32com 支持库! {err=}"
            )
            return

        if len(files := self.get_files()) > 0:
            excel_path = Path(files[0]).as_posix()
            pdf_path = Path(excel_path).with_suffix(".pdf").as_posix()

            xl_app = DispatchEx("Excel.Application")
            xl_app.Visible = False
            xl_app.DisplayAlerts = 0
            books = xl_app.Workbooks.Open(excel_path, False)
            books.ExportAsFixedFormat(0, pdf_path)
            books.Close(False)
            xl_app.Quit()
