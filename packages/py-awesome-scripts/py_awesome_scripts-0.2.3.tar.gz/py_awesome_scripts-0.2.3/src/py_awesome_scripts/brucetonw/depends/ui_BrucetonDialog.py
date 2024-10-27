# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BrucetonDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Bruceton(object):
    def setupUi(self, Bruceton):
        if not Bruceton.objectName():
            Bruceton.setObjectName("Bruceton")
        Bruceton.resize(647, 587)
        self.verticalLayout_3 = QVBoxLayout(Bruceton)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.hlData = QHBoxLayout()
        self.hlData.setSpacing(6)
        self.hlData.setObjectName("hlData")
        self.gbData = QGroupBox(Bruceton)
        self.gbData.setObjectName("gbData")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gbData.sizePolicy().hasHeightForWidth()
        )
        self.gbData.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.gbData)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hlVals = QHBoxLayout()
        self.hlVals.setSpacing(6)
        self.hlVals.setObjectName("hlVals")
        self.hlH = QHBoxLayout()
        self.hlH.setSpacing(6)
        self.hlH.setObjectName("hlH")
        self.lH = QLabel(self.gbData)
        self.lH.setObjectName("lH")
        self.lH.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.hlH.addWidget(self.lH)

        self.dsH = QDoubleSpinBox(self.gbData)
        self.dsH.setObjectName("dsH")
        self.dsH.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )
        self.dsH.setMinimum(0.000000000000000)
        self.dsH.setMaximum(9999.000000000000000)
        self.dsH.setSingleStep(1.000000000000000)
        self.dsH.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.dsH.setValue(3.500000000000000)

        self.hlH.addWidget(self.dsH)

        self.hlVals.addLayout(self.hlH)

        self.hld = QHBoxLayout()
        self.hld.setSpacing(6)
        self.hld.setObjectName("hld")
        self.ld = QLabel(self.gbData)
        self.ld.setObjectName("ld")
        self.ld.setLayoutDirection(Qt.LeftToRight)
        self.ld.setTextFormat(Qt.AutoText)
        self.ld.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.hld.addWidget(self.ld)

        self.dsd = QDoubleSpinBox(self.gbData)
        self.dsd.setObjectName("dsd")
        self.dsd.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )
        self.dsd.setDecimals(3)
        self.dsd.setMinimum(0.000000000000000)
        self.dsd.setMaximum(9999.000000000000000)
        self.dsd.setSingleStep(1.000000000000000)
        self.dsd.setValue(0.050000000000000)

        self.hld.addWidget(self.dsd)

        self.hlVals.addLayout(self.hld)

        self.verticalLayout.addLayout(self.hlVals)

        self.hlProb = QHBoxLayout()
        self.hlProb.setSpacing(6)
        self.hlProb.setObjectName("hlProb")
        self.hlC = QHBoxLayout()
        self.hlC.setSpacing(6)
        self.hlC.setObjectName("hlC")
        self.lC = QLabel(self.gbData)
        self.lC.setObjectName("lC")
        self.lC.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.hlC.addWidget(self.lC)

        self.dsC = QDoubleSpinBox(self.gbData)
        self.dsC.setObjectName("dsC")
        self.dsC.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )
        self.dsC.setMinimum(0.500000000000000)
        self.dsC.setMaximum(1.000000000000000)
        self.dsC.setSingleStep(0.100000000000000)
        self.dsC.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.dsC.setValue(0.950000000000000)

        self.hlC.addWidget(self.dsC)

        self.hlProb.addLayout(self.hlC)

        self.hlR = QHBoxLayout()
        self.hlR.setSpacing(6)
        self.hlR.setObjectName("hlR")
        self.lR = QLabel(self.gbData)
        self.lR.setObjectName("lR")
        self.lR.setLayoutDirection(Qt.LeftToRight)
        self.lR.setTextFormat(Qt.AutoText)
        self.lR.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.hlR.addWidget(self.lR)

        self.dsR = QDoubleSpinBox(self.gbData)
        self.dsR.setObjectName("dsR")
        self.dsR.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )
        self.dsR.setDecimals(10)
        self.dsR.setMinimum(0.900000000000000)
        self.dsR.setMaximum(1.000000000000000)
        self.dsR.setSingleStep(0.010000000000000)
        self.dsR.setValue(0.999900000000000)

        self.hlR.addWidget(self.dsR)

        self.hlProb.addLayout(self.hlR)

        self.verticalLayout.addLayout(self.hlProb)

        self.twFireData = QTableWidget(self.gbData)
        if self.twFireData.columnCount() < 3:
            self.twFireData.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.twFireData.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.twFireData.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.twFireData.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if self.twFireData.rowCount() < 7:
            self.twFireData.setRowCount(7)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.twFireData.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.twFireData.setVerticalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.twFireData.setVerticalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.twFireData.setVerticalHeaderItem(3, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.twFireData.setVerticalHeaderItem(4, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.twFireData.setVerticalHeaderItem(5, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.twFireData.setVerticalHeaderItem(6, __qtablewidgetitem9)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.Dense4Pattern)
        brush1 = QBrush(QColor(128, 131, 130, 255))
        brush1.setStyle(Qt.NoBrush)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setBackground(brush1)
        __qtablewidgetitem10.setForeground(brush)
        __qtablewidgetitem10.setFlags(
            Qt.ItemIsSelectable
            | Qt.ItemIsEditable
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsUserCheckable
        )
        self.twFireData.setItem(0, 0, __qtablewidgetitem10)
        brush2 = QBrush(QColor(128, 131, 130, 255))
        brush2.setStyle(Qt.NoBrush)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setBackground(brush2)
        __qtablewidgetitem11.setFlags(
            Qt.ItemIsSelectable
            | Qt.ItemIsEditable
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsUserCheckable
        )
        self.twFireData.setItem(1, 0, __qtablewidgetitem11)
        brush3 = QBrush(QColor(128, 131, 130, 255))
        brush3.setStyle(Qt.NoBrush)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setBackground(brush3)
        __qtablewidgetitem12.setFlags(
            Qt.ItemIsSelectable
            | Qt.ItemIsEditable
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsUserCheckable
        )
        self.twFireData.setItem(2, 0, __qtablewidgetitem12)
        brush4 = QBrush(QColor(128, 131, 130, 255))
        brush4.setStyle(Qt.NoBrush)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setBackground(brush4)
        __qtablewidgetitem13.setFlags(
            Qt.ItemIsSelectable
            | Qt.ItemIsEditable
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsUserCheckable
        )
        self.twFireData.setItem(3, 0, __qtablewidgetitem13)
        brush5 = QBrush(QColor(128, 131, 130, 255))
        brush5.setStyle(Qt.NoBrush)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setBackground(brush5)
        __qtablewidgetitem14.setFlags(
            Qt.ItemIsSelectable
            | Qt.ItemIsEditable
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsUserCheckable
        )
        self.twFireData.setItem(4, 0, __qtablewidgetitem14)
        brush6 = QBrush(QColor(128, 131, 130, 255))
        brush6.setStyle(Qt.NoBrush)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setBackground(brush6)
        __qtablewidgetitem15.setFlags(
            Qt.ItemIsSelectable
            | Qt.ItemIsEditable
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsUserCheckable
        )
        self.twFireData.setItem(5, 0, __qtablewidgetitem15)
        brush7 = QBrush(QColor(128, 131, 130, 255))
        brush7.setStyle(Qt.NoBrush)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setBackground(brush7)
        __qtablewidgetitem16.setFlags(
            Qt.ItemIsSelectable
            | Qt.ItemIsEditable
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsUserCheckable
        )
        self.twFireData.setItem(6, 0, __qtablewidgetitem16)
        self.twFireData.setObjectName("twFireData")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.twFireData.sizePolicy().hasHeightForWidth()
        )
        self.twFireData.setSizePolicy(sizePolicy1)
        self.twFireData.setFrameShape(QFrame.NoFrame)
        self.twFireData.setFrameShadow(QFrame.Sunken)
        self.twFireData.setLineWidth(1)
        self.twFireData.setMidLineWidth(1)
        self.twFireData.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContentsOnFirstShow
        )
        self.twFireData.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.twFireData.setGridStyle(Qt.DashLine)
        self.twFireData.horizontalHeader().setMinimumSectionSize(24)
        self.twFireData.horizontalHeader().setDefaultSectionSize(150)
        self.twFireData.horizontalHeader().setStretchLastSection(False)
        self.twFireData.verticalHeader().setMinimumSectionSize(24)
        self.twFireData.verticalHeader().setDefaultSectionSize(30)
        self.twFireData.verticalHeader().setProperty("showSortIndicator", False)
        self.twFireData.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.twFireData)

        self.hlData.addWidget(self.gbData)

        self.gbOperations = QGroupBox(Bruceton)
        self.gbOperations.setObjectName("gbOperations")
        self.verticalLayout_2 = QVBoxLayout(self.gbOperations)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pbCalc = QPushButton(self.gbOperations)
        self.pbCalc.setObjectName("pbCalc")

        self.verticalLayout_2.addWidget(self.pbCalc)

        self.pbRead = QPushButton(self.gbOperations)
        self.pbRead.setObjectName("pbRead")

        self.verticalLayout_2.addWidget(self.pbRead)

        self.pbSave = QPushButton(self.gbOperations)
        self.pbSave.setObjectName("pbSave")

        self.verticalLayout_2.addWidget(self.pbSave)

        self.pbSaveAs = QPushButton(self.gbOperations)
        self.pbSaveAs.setObjectName("pbSaveAs")

        self.verticalLayout_2.addWidget(self.pbSaveAs)

        self.vsOperations = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.vsOperations)

        self.hlData.addWidget(self.gbOperations)

        self.verticalLayout_3.addLayout(self.hlData)

        self.gbScore = QGroupBox(Bruceton)
        self.gbScore.setObjectName("gbScore")
        self.horizontalLayout = QHBoxLayout(self.gbScore)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tbScore = QTextBrowser(self.gbScore)
        self.tbScore.setObjectName("tbScore")

        self.horizontalLayout.addWidget(self.tbScore)

        self.verticalLayout_3.addWidget(self.gbScore)

        self.retranslateUi(Bruceton)

        QMetaObject.connectSlotsByName(Bruceton)

    # setupUi

    def retranslateUi(self, Bruceton):
        Bruceton.setWindowTitle(
            QCoreApplication.translate("Bruceton", "Form", None)
        )
        self.gbData.setTitle(
            QCoreApplication.translate("Bruceton", "\u6570\u636e", None)
        )
        self.lH.setText(QCoreApplication.translate("Bruceton", "H =", None))
        self.ld.setText(QCoreApplication.translate("Bruceton", "d =", None))
        self.dsd.setSuffix("")
        self.lC.setText(QCoreApplication.translate("Bruceton", "C =", None))
        self.lR.setText(QCoreApplication.translate("Bruceton", "R =", None))
        self.dsR.setSuffix("")
        ___qtablewidgetitem = self.twFireData.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("Bruceton", "\u6c34\u5e73v", None)
        )
        ___qtablewidgetitem1 = self.twFireData.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate(
                "Bruceton", "\u53d1\u706b\u6570n(x)", None
            )
        )
        ___qtablewidgetitem2 = self.twFireData.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate(
                "Bruceton", "\u4e0d\u53d1\u706b\u6570n(o)", None
            )
        )
        ___qtablewidgetitem3 = self.twFireData.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("Bruceton", "H+3d", None)
        )
        ___qtablewidgetitem4 = self.twFireData.verticalHeaderItem(1)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("Bruceton", "H+2d", None)
        )
        ___qtablewidgetitem5 = self.twFireData.verticalHeaderItem(2)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("Bruceton", "H+d", None)
        )
        ___qtablewidgetitem6 = self.twFireData.verticalHeaderItem(3)
        ___qtablewidgetitem6.setText(
            QCoreApplication.translate("Bruceton", "H", None)
        )
        ___qtablewidgetitem7 = self.twFireData.verticalHeaderItem(4)
        ___qtablewidgetitem7.setText(
            QCoreApplication.translate("Bruceton", "H-d", None)
        )
        ___qtablewidgetitem8 = self.twFireData.verticalHeaderItem(5)
        ___qtablewidgetitem8.setText(
            QCoreApplication.translate("Bruceton", "H-2d", None)
        )
        ___qtablewidgetitem9 = self.twFireData.verticalHeaderItem(6)
        ___qtablewidgetitem9.setText(
            QCoreApplication.translate("Bruceton", "H-3d", None)
        )
        __sortingEnabled = self.twFireData.isSortingEnabled()
        self.twFireData.setSortingEnabled(False)
        self.twFireData.setSortingEnabled(__sortingEnabled)

        self.gbOperations.setTitle(
            QCoreApplication.translate("Bruceton", "\u64cd\u4f5c", None)
        )
        self.pbCalc.setText(
            QCoreApplication.translate("Bruceton", "\u8ba1\u7b97", None)
        )
        self.pbRead.setText(
            QCoreApplication.translate("Bruceton", "\u8bfb\u53d6", None)
        )
        self.pbSave.setText(
            QCoreApplication.translate("Bruceton", "\u4fdd\u5b58", None)
        )
        self.pbSaveAs.setText(
            QCoreApplication.translate("Bruceton", "\u53e6\u5b58\u4e3a", None)
        )
        self.gbScore.setTitle(
            QCoreApplication.translate(
                "Bruceton", "\u8ba1\u7b97\u7ed3\u679c", None
            )
        )

    # retranslateUi
