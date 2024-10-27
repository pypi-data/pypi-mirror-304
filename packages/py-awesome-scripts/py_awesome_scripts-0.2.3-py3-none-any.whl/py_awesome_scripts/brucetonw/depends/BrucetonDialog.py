from PySide2.QtWidgets import QWidget

from .ui_BrucetonDialog import Ui_Bruceton

BRUCETON_PARAMS = "H d C R".split(" ")


class BrucetonDialog(QWidget, Ui_Bruceton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def _calc(self):
        for param in BRUCETON_PARAMS:
            val_param = float(getattr(self, f"ds{param}").text())
