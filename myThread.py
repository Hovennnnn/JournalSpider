from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.Qt import QMutex
import sys
from flush import Flush


class MyThread(QThread):
    progress_trigger = pyqtSignal(int, str) # 此处输入待传送数据类型
    end_trigger = pyqtSignal()
    q_lock = QMutex()
 
    def __init__(self, target=None, which=None, *args, **keywords):
        QThread.__init__(self)
        self.target = target
        self.which = which
 
    def run(self):
       # 该线程要干嘛
       self.q_lock.lock()
       self.target(self.which, self.progress_trigger.emit)
       self.end_trigger.emit()
       self.q_lock.unlock()

# # data处理函数（一般在另一个线程中）
# def receive_data():
#     # 怎么处理data
 
# # 线程1实例化
# threadone = ThreadOne()
# # 设定线程1传出数据data的接收函数receive
# threadone.trigger.connect(receive_data)
# # 开启线程1            
# threadone.start()    
