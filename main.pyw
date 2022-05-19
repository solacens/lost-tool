from gui import Gui
from keyListener import KeyListener

# Init modules
gui = Gui()
keyListener = KeyListener(gui.exit, gui.toggleTransparency)

# Toggle G presser
def toggleGPresser():
  keyListener.toggleHolding = not keyListener.toggleHolding
  gui.log("State is now: {0}".format(keyListener.toggleHolding))
gui.listeners["g_presser"](toggleGPresser)

# Blocking
gui.start()
