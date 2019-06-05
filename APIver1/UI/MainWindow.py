# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CapitalAPI(object):
    def setupUi(self, CapitalAPI):
        CapitalAPI.setObjectName("CapitalAPI")
        CapitalAPI.setWindowModality(QtCore.Qt.NonModal)
        CapitalAPI.resize(1024, 574)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        CapitalAPI.setFont(font)
        self.centralwidget = QtWidgets.QWidget(CapitalAPI)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1024, 507))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.KLineview = QtWidgets.QGraphicsView(self.tab)
        self.KLineview.setGeometry(QtCore.QRect(0, 0, 900, 479))
        self.KLineview.setObjectName("KLineview")
        self.KLinescene=QtWidgets.QGraphicsScene()
        self.KLinescene.
        self.commodityline = QtWidgets.QLineEdit(self.tab)
        self.commodityline.setGeometry(QtCore.QRect(901, 18, 113, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.commodityline.setFont(font)
        self.commodityline.setObjectName("commodityline")
        self.commoditybtn = QtWidgets.QPushButton(self.tab)
        self.commoditybtn.setGeometry(QtCore.QRect(954, 40, 61, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.commoditybtn.setFont(font)
        self.commoditybtn.setObjectName("commoditybtn")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(950, 0, 25, 15))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.TDetailbtn = QtWidgets.QPushButton(self.tab)
        self.TDetailbtn.setGeometry(QtCore.QRect(940, 70, 75, 23))
        self.TDetailbtn.setObjectName("TDetailbtn")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget.addTab(self.tab_2, "")
        CapitalAPI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CapitalAPI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        CapitalAPI.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(CapitalAPI)
        self.statusBar.setObjectName("statusBar")
        CapitalAPI.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(CapitalAPI)
        self.toolBar.setObjectName("toolBar")
        CapitalAPI.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLogin = QtWidgets.QAction(CapitalAPI)
        self.actionLogin.setObjectName("actionLogin")
        self.SysDetail = QtWidgets.QAction(CapitalAPI)
        self.SysDetail.setObjectName("SysDetail")
        self.Connectbtn = QtWidgets.QAction(CapitalAPI)
        self.Connectbtn.setObjectName("Connectbtn")
        self.Disconnectbtn = QtWidgets.QAction(CapitalAPI)
        self.Disconnectbtn.setObjectName("Disconnectbtn")
        self.menu_3.addAction(self.actionLogin)
        self.menu_3.addSeparator()
        self.menu_4.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.toolBar.addAction(self.SysDetail)
        self.toolBar.addAction(self.Connectbtn)
        self.toolBar.addAction(self.Disconnectbtn)

        self.retranslateUi(CapitalAPI)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CapitalAPI)

    def retranslateUi(self, CapitalAPI):
        _translate = QtCore.QCoreApplication.translate
        CapitalAPI.setWindowTitle(_translate("CapitalAPI", "群益API"))
        self.commodityline.setText(_translate("CapitalAPI", "TX00"))
        self.commoditybtn.setText(_translate("CapitalAPI", "OK"))
        self.label.setText(_translate("CapitalAPI", "商品"))
        self.TDetailbtn.setText(_translate("CapitalAPI", "交易明細"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("CapitalAPI", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("CapitalAPI", "Tab 2"))
        self.menu.setTitle(_translate("CapitalAPI", "檔案"))
        self.menu_2.setTitle(_translate("CapitalAPI", "檢視"))
        self.menu_3.setTitle(_translate("CapitalAPI", "功能"))
        self.menu_4.setTitle(_translate("CapitalAPI", "說明"))
        self.toolBar.setWindowTitle(_translate("CapitalAPI", "toolBar"))
        self.actionLogin.setText(_translate("CapitalAPI", "登入"))
        self.SysDetail.setText(_translate("CapitalAPI", "系統訊息"))
        self.SysDetail.setToolTip(_translate("CapitalAPI", "API系統訊息"))
        self.Connectbtn.setText(_translate("CapitalAPI", "報價連線"))
        self.Connectbtn.setToolTip(_translate("CapitalAPI", "建立報價連線回報機制"))
        self.Disconnectbtn.setText(_translate("CapitalAPI", "報價清除"))
        self.Disconnectbtn.setToolTip(_translate("CapitalAPI", "斷開或情除報價連線狀態"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CapitalAPI = QtWidgets.QMainWindow()
    ui = Ui_CapitalAPI()
    ui.setupUi(CapitalAPI)
    CapitalAPI.show()
    sys.exit(app.exec_())

