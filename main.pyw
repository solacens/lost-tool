from gui import Gui
from keyListener import KeyListener

# Init modules
gui = Gui()
keyListener = KeyListener({
  "quit": gui.exit,
  "toggleHide": gui.toggleHide
})

# Toggle G presser
def toggleGPresser():
  keyListener.toggleHolding = not keyListener.toggleHolding
  gui.log("Status now: {0}".format("On" if keyListener.toggleHolding else "Off"))
gui.listeners["g_presser"](toggleGPresser)

# Blocking
gui.start()
