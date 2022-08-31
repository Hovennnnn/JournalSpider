# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
import sys
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from flush import Flush, edgedriver_manager
from flush.data_mgr import DataManager
from mini_ui import Ui_Form
from myThread import MyThread


class myQWidget(QtWidgets.QWidget):
    close_sub_window_signal = pyqtSignal()
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_sub_window_signal.emit()
        return super().closeEvent(a0)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(628, 602)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("font: 16pt \"Adobe 黑体 Std R\";")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 19))
        self.comboBox.setMaximumSize(QtCore.QSize(512, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(self.frame)
        self.comboBox_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMaximumSize(QtCore.QSize(401, 16777215))
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_2.addWidget(self.comboBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tableView = QtWidgets.QTableView(self.frame)
        self.tableView.setObjectName("tableView")
        self.player_model = QtGui.QStandardItemModel()                 # 建立数据模型实例
        self.verticalLayout_2.addWidget(self.tableView)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 628, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.renew_driver = QtWidgets.QAction(MainWindow)
        self.renew_driver.setObjectName("actiongengxinqudong")
        self.menu.addAction(self.renew_driver)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.mytranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # self.mini_thread_pool = QThreadPool()
        # self.mini_thread_pool.globalInstance()
        # self.mini_thread_pool.setMaxThreadCount(5) # 设置最大线程数


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">文献采集工具</span></p></body></html>"))
        self.comboBox.setItemText(0, _translate("MainWindow", "(综合顶刊) Annals of the Association of American Geographers"))
        self.comboBox.setItemText(1, _translate("MainWindow", "(综合期刊、短小文章、教育) The Professional Geographer"))
        self.comboBox.setItemText(2, _translate("MainWindow", "(自然生态) Geoforum"))
        self.comboBox.setItemText(3, _translate("MainWindow", "(综合顶刊) Transaction of the Institute of British Geographers"))
        self.comboBox.setItemText(4, _translate("MainWindow", "(综合期刊、短小文章) The Geographical Journal"))
        self.comboBox.setItemText(5, _translate("MainWindow", "(综合期刊、短小文章、教育) Area"))
        self.pushButton.setText(_translate("MainWindow", "更新"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">期刊序号：</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "导出"))
        self.menu.setTitle(_translate("MainWindow", "选项"))
        self.renew_driver.setText(_translate("MainWindow", "更新驱动"))

    def mytranslateUi(self, MainWindow):
        self.datapath = [r"data\Annals_of_the_Association_of_American_Geographers.db",
                         r"data\The_Professional_Geographer.db",
                         r"data\Geoforum.db",
                         r"data\Transaction_of_the_Institute_of_British_Geographers.db",
                         r"data\The_Geographical_Journal.db",
                         r"data\Area.db"]
        self.pushButton.clicked.connect(self.click_flush)
        self.pushButton_2.clicked.connect(lambda: self.export(MainWindow))
        self.comboBox.currentIndexChanged.connect(self.comboBox_2_refresh)
        self.comboBox_2.currentIndexChanged.connect(self.table_show)
        self.renew_driver.triggered.connect(self.renew_driver_version)
        self.comboBox_2_refresh()

    def renew_driver_version(self):
        '''更新驱动'''
        # 函数中connect 使用lambda函数传参，直接传递函数对象好像不起作用？？？
        self.Form = myQWidget() # 重载了窗口关闭事件
        mini_ui = Ui_Form()
        thread_i = MyThread(target=edgedriver_manager.check_driver_new_version)

        thread_i.progress_trigger.connect(mini_ui.refresh_progressbar)

        thread_i.end_trigger.connect(lambda: self.Form.close())   # 请求结束时关闭子窗口
        thread_i.end_trigger.connect(lambda: self.comboBox_2_refresh())   # 请求结束时刷新数据

        mini_ui.setupUi(self.Form, thread_i, journal=self.comboBox.currentText())
        print(self.comboBox.currentIndex())

        self.Form.close_sub_window_signal.connect(lambda: mini_ui.close_request()) # 关闭子窗口时关闭线程
        
        thread_i.start()
        self.thread = thread_i
        self.Form.show()


    def click_flush(self):
        # 函数中connect 使用lambda函数传参，直接传递函数对象好像不起作用？？？
        self.Form = myQWidget() # 重载了窗口关闭事件
        mini_ui = Ui_Form()
        thread_i = MyThread(target=Flush.Flushing, which=self.comboBox.currentIndex())

        thread_i.progress_trigger.connect(mini_ui.refresh_progressbar)

        thread_i.end_trigger.connect(lambda: self.Form.close())   # 请求结束时关闭子窗口
        thread_i.end_trigger.connect(lambda: self.comboBox_2_refresh())   # 请求结束时刷新数据

        mini_ui.setupUi(self.Form, thread_i, journal=self.comboBox.currentText())
        print(self.comboBox.currentIndex())

        self.Form.close_sub_window_signal.connect(lambda: mini_ui.close_request()) # 关闭子窗口时关闭线程
        
        thread_i.start()
        self.thread = thread_i
        self.Form.show()
        

    def comboBox_2_refresh(self):
        _translate = QtCore.QCoreApplication.translate
        mydata_mgr = DataManager(self.datapath[self.comboBox.currentIndex()])
        table_names = mydata_mgr.get_all_table_name()
        self.comboBox_2.clear()
        for idx, table_name in enumerate(table_names):
            self.comboBox_2.addItem( _translate("MainWindow", table_name))
        # self.table_show()

    def table_show(self):
        table_header = ["序号", "标题", "中文标题", "作者", "发表单位", "发表日期"]
        self.player_model = QtGui.QStandardItemModel()
        self.player_model.setHorizontalHeaderLabels(table_header)
        # for c, cell in enumerate(table_header):
        #     it = QtGui.QStandardItem(str(cell))
        #     self.player_model.setItem(0, c, it)
        if self.comboBox_2.currentText():
            mydata_mgr = DataManager(self.datapath[self.comboBox.currentIndex()])
            table_data = mydata_mgr.get_table_data(table=self.comboBox_2.currentText())
            # print(table_data)
            if table_data:
                max_r,max_c = len(table_data),len(table_data[0])
                for r,rdata in enumerate(table_data):
                    for c,cell in enumerate(rdata):
                        it = QtGui.QStandardItem(str(cell))
                        # it.setEditable(False)                      # 设置单元不可编辑
                        self.player_model.setItem(max_r - 1 - r, c, it)
        self.tableView.setModel(self.player_model)

    def export(self, MainWindow):
        mydata_mgr = DataManager(self.datapath[self.comboBox.currentIndex()])
        filename = f"{self.comboBox.currentText()}-{self.comboBox_2.currentText()}"
        filepath, file_type = QtWidgets.QFileDialog.getSaveFileName(MainWindow, "export_data", os.path.join(os.path.dirname(os.path.realpath(sys.executable)), filename), 'Word文档 (*.docx);;Text files (*.txt)')
        print(filepath)
        if filepath:
            threading.Thread(target=mydata_mgr.export, args=(self.comboBox_2.currentText(), filepath, file_type)).start()
            # mydata_mgr.export(table=self.comboBox_2.currentText(), filepath=filepath)




if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # 不加上这一行，显示结果不一样
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
