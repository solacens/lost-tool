from actions import Actions
from gui import Gui
from keyRepeater import KeyRepeater

# Init modules
gui = Gui()
keyRepeter = KeyRepeater(gui)
actions = Actions(gui)

# Blocking
gui.start()
