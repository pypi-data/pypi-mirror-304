import pathlib
import typing
import zipfile

from .base import BaseReader
from .excel import ExcelReaderXls, ExcelReaderXlsx
from .pdf import PdfReaderPlumber
from .text import TextReader
from .word import WordReader

DOCUMENT_READERS: typing.Dict[str, type(BaseReader)] = dict(
    docx=WordReader(),
    txt=TextReader(),
    c=TextReader(),
    xls=ExcelReaderXls(),
    xlsx=ExcelReaderXlsx(),
    pdf=PdfReaderPlumber(),
)


class ZipReader(BaseReader):
    def __init__(self):
        super().__init__()

    def read(
        self, file_path: typing.Union[pathlib.Path, typing.IO[bytes]]
    ) -> str:
        with zipfile.ZipFile(file_path, "r") as zip_file:
            file_names = zip_file.namelist()

            for file_name in file_names:
                with zip_file.open(file_name) as file:
                    reader: typing.Union[BaseReader, None] = (
                        DOCUMENT_READERS.get(
                            pathlib.Path(file_name).suffix[1:], None
                        )
                    )
                    content = reader.read(file) if reader else None
                    return content


ARCHIVE_READERS: typing.Dict[str, type(BaseReader)] = dict(
    zip=ZipReader(),
)

ALL_READERS: typing.Dict[str, type(BaseReader)] = dict(
    **DOCUMENT_READERS, **ARCHIVE_READERS
)
