from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread

class Worker(QObject):
  toggleHideSingal = pyqtSignal()
  logSignal = pyqtSignal(str, str)

  def start(self, fn):
    Thread(target=self._execute, args=(fn,), daemon=True).start()

  def _execute(self, fn):
    fn(self)

  def toggleHide(self):
    self.toggleHideSingal.emit()

  def log(self, str1, str2):
    self.logSignal.emit(str1, str2)
