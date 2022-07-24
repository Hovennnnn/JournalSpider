from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.Qt import QMutex
import time

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
        if self.which != None: # 爬虫线程
            self.target(self.which, self.progress_trigger.emit)
        else:   # 更新驱动线程
            self.target(progress_bar=self.progress_trigger.emit)
    #   time.sleep(3) # 阻塞3秒，便于看到结果
        self.end_trigger.emit()
        self.q_lock.unlock()
