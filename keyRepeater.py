from pynput.keyboard import Key, Listener
from keyPress import KeyPress

class KeyRepeater:
  def __init__(self, gui):
    self.gui = gui
    self.log = gui.log
    self.log = print

    keyPress = KeyPress()

    def on_press(key):
      if key == keyPress.KEY_FOR_HOLD:
          keyPress.holding = True

    def on_release(key):
      if key == keyPress.KEY_FOR_HOLD:
        keyPress.holding = False
      elif key == Key.insert:
        # Stop listener
        return False

    self.listener = Listener(on_press=on_press, on_release=on_release)
    self.listener.start()

    self.toggleHolding = keyPress.toggle_holding

    self.gui.connect("key_repeater", self.toggleGPresser)

    print("<Key Repeater> Initialized.")

  def toggleGPresser(self):
    self.toggleHolding = not self.toggleHolding
    self.log("Toggling.", "Key Repeater")
    self.log("Status now: {0}".format("On" if self.toggleHolding else "Off"), "Key Repeater")

if __name__ == "__main__":
  keyRepeater = KeyRepeater()

  # Any blocking function
