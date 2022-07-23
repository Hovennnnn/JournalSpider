import sys
import os

if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
elif __file__:
        base_path = os.path.dirname(__file__)

os.chdir(base_path)     # 设置工作目录，这一步主要是解决打包后工作路径不一致的问题

from flush.edgedriver_manager import check_driver_new_version
check_driver_new_version(where="main")  #放在前面check是因为flush包中使用selenium的两个模块在导入时就设置了driverpath

from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # 不加上这一行，显示结果和QTdesigner的不一样
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    print(base_path)
    main()