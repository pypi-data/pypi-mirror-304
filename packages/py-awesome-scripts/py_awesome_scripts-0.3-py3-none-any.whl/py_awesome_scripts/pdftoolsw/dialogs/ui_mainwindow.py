# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import pdftools_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(752, 386)
        icon = QIcon()
        icon.addFile(
            ":/assets/images/pdftools.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        MainWindow.setWindowIcon(icon)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAboutQt = QAction(MainWindow)
        self.actionAboutQt.setObjectName("actionAboutQt")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gbConvert = QGroupBox(self.centralwidget)
        self.gbConvert.setObjectName("gbConvert")
        self.horizontalLayout = QHBoxLayout(self.gbConvert)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vlImg2PDF = QVBoxLayout()
        self.vlImg2PDF.setObjectName("vlImg2PDF")
        self.pbImg2PDF = QPushButton(self.gbConvert)
        self.pbImg2PDF.setObjectName("pbImg2PDF")
        icon1 = QIcon()
        icon1.addFile(
            ":/assets/images/image.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.pbImg2PDF.setIcon(icon1)
        self.pbImg2PDF.setIconSize(QSize(100, 100))

        self.vlImg2PDF.addWidget(self.pbImg2PDF)

        self.lImg2PDF = QLabel(self.gbConvert)
        self.lImg2PDF.setObjectName("lImg2PDF")
        self.lImg2PDF.setLayoutDirection(Qt.LeftToRight)
        self.lImg2PDF.setAlignment(Qt.AlignCenter)

        self.vlImg2PDF.addWidget(self.lImg2PDF)

        self.horizontalLayout.addLayout(self.vlImg2PDF)

        self.vlWord2PDF = QVBoxLayout()
        self.vlWord2PDF.setObjectName("vlWord2PDF")
        self.pbWord2PDF = QPushButton(self.gbConvert)
        self.pbWord2PDF.setObjectName("pbWord2PDF")
        icon2 = QIcon()
        icon2.addFile(
            ":/assets/images/word.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.pbWord2PDF.setIcon(icon2)
        self.pbWord2PDF.setIconSize(QSize(100, 100))

        self.vlWord2PDF.addWidget(self.pbWord2PDF)

        self.lWord2PDF = QLabel(self.gbConvert)
        self.lWord2PDF.setObjectName("lWord2PDF")
        self.lWord2PDF.setLayoutDirection(Qt.LeftToRight)
        self.lWord2PDF.setAlignment(Qt.AlignCenter)

        self.vlWord2PDF.addWidget(self.lWord2PDF)

        self.horizontalLayout.addLayout(self.vlWord2PDF)

        self.vlExcel2PDF = QVBoxLayout()
        self.vlExcel2PDF.setObjectName("vlExcel2PDF")
        self.pbExcel2PDF = QPushButton(self.gbConvert)
        self.pbExcel2PDF.setObjectName("pbExcel2PDF")
        icon3 = QIcon()
        icon3.addFile(
            ":/assets/images/excel.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.pbExcel2PDF.setIcon(icon3)
        self.pbExcel2PDF.setIconSize(QSize(100, 100))

        self.vlExcel2PDF.addWidget(self.pbExcel2PDF)

        self.lExcel2PDF = QLabel(self.gbConvert)
        self.lExcel2PDF.setObjectName("lExcel2PDF")
        self.lExcel2PDF.setLayoutDirection(Qt.LeftToRight)
        self.lExcel2PDF.setAlignment(Qt.AlignCenter)

        self.vlExcel2PDF.addWidget(self.lExcel2PDF)

        self.horizontalLayout.addLayout(self.vlExcel2PDF)

        self.vlPPT2PDF = QVBoxLayout()
        self.vlPPT2PDF.setObjectName("vlPPT2PDF")
        self.pbPPT2PDF = QPushButton(self.gbConvert)
        self.pbPPT2PDF.setObjectName("pbPPT2PDF")
        icon4 = QIcon()
        icon4.addFile(
            ":/assets/images/ppt.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.pbPPT2PDF.setIcon(icon4)
        self.pbPPT2PDF.setIconSize(QSize(100, 100))

        self.vlPPT2PDF.addWidget(self.pbPPT2PDF)

        self.lPPT2PDF = QLabel(self.gbConvert)
        self.lPPT2PDF.setObjectName("lPPT2PDF")
        self.lPPT2PDF.setLayoutDirection(Qt.LeftToRight)
        self.lPPT2PDF.setAlignment(Qt.AlignCenter)

        self.vlPPT2PDF.addWidget(self.lPPT2PDF)

        self.horizontalLayout.addLayout(self.vlPPT2PDF)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_9 = QPushButton(self.gbConvert)
        self.pushButton_9.setObjectName("pushButton_9")
        icon5 = QIcon()
        icon5.addFile(
            ":/assets/images/html.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.pushButton_9.setIcon(icon5)
        self.pushButton_9.setIconSize(QSize(100, 100))

        self.verticalLayout_6.addWidget(self.pushButton_9)

        self.label_6 = QLabel(self.gbConvert)
        self.label_6.setObjectName("label_6")
        self.label_6.setLayoutDirection(Qt.LeftToRight)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_6)

        self.horizontalLayout.addLayout(self.verticalLayout_6)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.pushButton_15 = QPushButton(self.gbConvert)
        self.pushButton_15.setObjectName("pushButton_15")
        icon6 = QIcon()
        icon6.addFile(
            ":/assets/images/markdown.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.pushButton_15.setIcon(icon6)
        self.pushButton_15.setIconSize(QSize(100, 100))

        self.verticalLayout_12.addWidget(self.pushButton_15)

        self.label_12 = QLabel(self.gbConvert)
        self.label_12.setObjectName("label_12")
        self.label_12.setLayoutDirection(Qt.LeftToRight)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.label_12)

        self.horizontalLayout.addLayout(self.verticalLayout_12)

        self.verticalLayout.addWidget(self.gbConvert)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pushButton_10 = QPushButton(self.groupBox_3)
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.setIcon(icon1)
        self.pushButton_10.setIconSize(QSize(100, 100))

        self.verticalLayout_7.addWidget(self.pushButton_10)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.label_7.setLayoutDirection(Qt.LeftToRight)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_7)

        self.horizontalLayout_2.addLayout(self.verticalLayout_7)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton_11 = QPushButton(self.groupBox_3)
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_11.setIcon(icon1)
        self.pushButton_11.setIconSize(QSize(100, 100))

        self.verticalLayout_8.addWidget(self.pushButton_11)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName("label_8")
        self.label_8.setLayoutDirection(Qt.LeftToRight)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_8)

        self.horizontalLayout_2.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_12 = QPushButton(self.groupBox_3)
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_12.setIcon(icon1)
        self.pushButton_12.setIconSize(QSize(100, 100))

        self.verticalLayout_9.addWidget(self.pushButton_12)

        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName("label_9")
        self.label_9.setLayoutDirection(Qt.LeftToRight)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_9)

        self.horizontalLayout_2.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.pushButton_13 = QPushButton(self.groupBox_3)
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_13.setIcon(icon1)
        self.pushButton_13.setIconSize(QSize(100, 100))

        self.verticalLayout_10.addWidget(self.pushButton_13)

        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName("label_10")
        self.label_10.setLayoutDirection(Qt.LeftToRight)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_10)

        self.horizontalLayout_2.addLayout(self.verticalLayout_10)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.pushButton_14 = QPushButton(self.groupBox_3)
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_14.setIcon(icon1)
        self.pushButton_14.setIconSize(QSize(100, 100))

        self.verticalLayout_11.addWidget(self.pushButton_14)

        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName("label_11")
        self.label_11.setLayoutDirection(Qt.LeftToRight)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_11)

        self.horizontalLayout_2.addLayout(self.verticalLayout_11)

        self.verticalLayout.addWidget(self.groupBox_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 752, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setLayoutDirection(Qt.LeftToRight)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionAbout)
        self.menu.addAction(self.actionAboutQt)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "about PDFTools", None)
        )
        self.actionAboutQt.setText(
            QCoreApplication.translate("MainWindow", "about Qt", None)
        )
        self.gbConvert.setTitle(
            QCoreApplication.translate("MainWindow", "\u8f6c\u5316", None)
        )
        self.pbImg2PDF.setText("")
        self.lImg2PDF.setText(
            QCoreApplication.translate(
                "MainWindow", "\u56fe\u7247\u8f6cPDF", None
            )
        )
        self.pbWord2PDF.setText("")
        self.lWord2PDF.setText(
            QCoreApplication.translate("MainWindow", "Word\u8f6cPDF", None)
        )
        self.pbExcel2PDF.setText("")
        self.lExcel2PDF.setText(
            QCoreApplication.translate("MainWindow", "Excel\u8f6cPDF", None)
        )
        self.pbPPT2PDF.setText("")
        self.lPPT2PDF.setText(
            QCoreApplication.translate("MainWindow", "PPT\u8f6cPDF", None)
        )
        self.pushButton_9.setText("")
        self.label_6.setText(
            QCoreApplication.translate("MainWindow", "HTML\u8f6cPDF", None)
        )
        self.pushButton_15.setText("")
        self.label_12.setText(
            QCoreApplication.translate("MainWindow", "MD\u8f6cPDF", None)
        )
        self.groupBox_3.setTitle(
            QCoreApplication.translate("MainWindow", "\u7f16\u8f91", None)
        )
        self.pushButton_10.setText("")
        self.label_7.setText(
            QCoreApplication.translate("MainWindow", "\u5408\u5e76PDF", None)
        )
        self.pushButton_11.setText("")
        self.label_8.setText(
            QCoreApplication.translate("MainWindow", "\u62c6\u5206PDF", None)
        )
        self.pushButton_12.setText("")
        self.label_9.setText(
            QCoreApplication.translate(
                "MainWindow", "\u56fe\u7247\u8f6cPDF", None
            )
        )
        self.pushButton_13.setText("")
        self.label_10.setText(
            QCoreApplication.translate(
                "MainWindow", "\u56fe\u7247\u8f6cPDF", None
            )
        )
        self.pushButton_14.setText("")
        self.label_11.setText(
            QCoreApplication.translate(
                "MainWindow", "\u56fe\u7247\u8f6cPDF", None
            )
        )
        self.menu.setTitle(
            QCoreApplication.translate("MainWindow", "\u5173\u4e8e", None)
        )

    # retranslateUi
