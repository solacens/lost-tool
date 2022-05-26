from actions import Actions
from gui import Gui
from keyReleaser import KeyReleaser

# Init modules
gui = Gui()
keyReleaser = KeyReleaser()
actions = Actions(gui)

# Blocking
gui.start()
