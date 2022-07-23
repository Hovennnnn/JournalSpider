import sys
import os

if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
elif __file__:
        base_path = os.path.dirname(__file__)

os.chdir(base_path)

from flush.edgedriver_manager import check_driver_new_version
check_driver_new_version(where="main")

from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # 不加上这一行，显示结果不一样
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    print(base_path)
    main()