from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
import sys

class GuiWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    PREFERRED_DISPLAY = 0 # or 1, 2...
    PREFERRED_WIDTH = 300
    PREFERRED_HEIGHT = 300

    screen = QDesktopWidget.screenGeometry(QDesktopWidget(), PREFERRED_DISPLAY)

    self.setWindowTitle("LOST TOOL")
    self.setAttribute(Qt.WA_TranslucentBackground)
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    self.setGeometry((screen.width() + screen.left() - PREFERRED_WIDTH), screen.top(), PREFERRED_WIDTH, PREFERRED_HEIGHT)

    font = QFont()
    font.setPointSize(8)
    font.setFamily("Consolas")

    buttonFont = QFont()
    buttonFont.setPointSize(8)
    buttonFont.setWeight(2)
    buttonFont.setFamily("Consolas")

    STYLESHEET_TRANSPARENT = """
      QWidget{
        background-color: rgba(255,255,255,5%);
      }
      QTextEdit{
        background: rgba(255,255,255,10%);
        border: 1px solid rgba(125,125,125,30%);
      }
      QPushButton{
        background-color: rgba(255,255,255,35%)
      }
      QPushButton:hover{
        background-color: rgba(255,255,255,70%)
      }
    """
    STYLESHEET_OPAQUE = """
      QWidget{
        background-color: rgba(255,255,255,80%);
      }
      QTextEdit{
        background: rgba(240,240,240,80%);
        border: 1px solid rgba(125,125,125,30%);
      }
      QPushButton{
        background-color: rgba(240,240,240,35%)
      }
      QPushButton:hover{
        background-color: rgba(0,0,0,20%)
      }
    """

    bg = QWidget(self)
    bg.setStyleSheet(STYLESHEET_TRANSPARENT)
    bg.setMinimumSize(PREFERRED_WIDTH, PREFERRED_HEIGHT)

    layout = QGridLayout()
    layout.setContentsMargins(10, 10, 10, 10)

    textEdit = QTextEdit(self)
    textEdit.setReadOnly(True)
    textEdit.setFont(font)
    layout.addWidget(textEdit, 1, 0, 1, 3)
    cleanLog = lambda: textEdit.setPlainText("")
    def log(str, type = "INFO"):
      now = datetime.now()
      textEdit.setPlainText("[{1} {3}] {0}\n{2}".format(str, type, textEdit.toPlainText(), now.strftime("%H:%M:%S")))
    self.log = log

    self.transparency_state = True
    self.listeners = {}

    g_presser_button = QPushButton()
    g_presser_button.setText('Ctrl → G')
    g_presser_button.setFont(buttonFont)
    g_presser_button.clicked.connect(lambda: log("Toggling G Presser."))
    self.listeners["g_presser"] = g_presser_button.clicked.connect
    layout.addWidget(g_presser_button, 0, 0)

    fishing_button = QPushButton()
    fishing_button.setText('Fishing')
    fishing_button.setFont(buttonFont)
    fishing_button.clicked.connect(lambda: log("Start fishing."))
    self.listeners["fishing"] = fishing_button.clicked.connect
    layout.addWidget(fishing_button, 0, 1)

    chaos_button = QPushButton()
    chaos_button.setText('Chaos')
    chaos_button.setFont(buttonFont)
    chaos_button.clicked.connect(lambda: log("Start running on Chaos Dungeon."))
    self.listeners["chaos"] = chaos_button.clicked.connect
    layout.addWidget(chaos_button, 0, 2)

    close_button = QPushButton(self)
    close_button.setText('Quit')
    close_button.setFont(buttonFont)
    self.listeners["quit"] = close_button.clicked.connect
    layout.addWidget(close_button, 2, 2)

    transparency_button = QPushButton(self)
    transparency_button.setText('Lights ↑')
    transparency_button.setFont(buttonFont)
    def toggleTransparency():
      if self.transparency_state:
        transparency_button.setText('Lights ↓')
        bg.setStyleSheet(STYLESHEET_OPAQUE)
      else:
        transparency_button.setText('Lights ↑')
        bg.setStyleSheet(STYLESHEET_TRANSPARENT)
      self.transparency_state = not self.transparency_state
    transparency_button.clicked.connect(toggleTransparency)
    self.toggleTransparency = toggleTransparency
    layout.addWidget(transparency_button, 2, 1)

    clean_log_button = QPushButton()
    clean_log_button.setText('Clean logs')
    clean_log_button.setFont(buttonFont)
    clean_log_button.clicked.connect(lambda: cleanLog())
    layout.addWidget(clean_log_button, 2, 0)

    bg.setLayout(layout)
    self.show()

class Gui:
  def __init__(self):
    self.app = QApplication(sys.argv)
    self.window = GuiWindow()

    self.log = self.window.log
    self.listeners = self.window.listeners

    if "quit" in self.window.listeners:
      self.window.listeners["quit"](lambda: self.app.exit())
      self.window.listeners.pop("quit", None)

    self.toggleTransparency = self.window.toggleTransparency

    self.start = self.app.exec
    self.exit = self.app.exit

    print("GUI Initialized.")

if __name__ == "__main__":
  gui = Gui()

  gui.start()
