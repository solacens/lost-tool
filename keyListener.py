from pynput.keyboard import Key, Listener, GlobalHotKeys
from keyPress import KeyPress

class KeyListener:
  def __init__(self, functions):
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

    ctrlListener = Listener(on_press=on_press, on_release=on_release)
    ctrlListener.start()

    self.toggleHolding = keyPress.toggle_holding

    self.quitListener = GlobalHotKeys({
      '<ctrl>+q': functions["quit"],
      '<ctrl>+t': functions["toggleTransparency"],
      '<ctrl>+h': functions["toggleHide"]
    })
    self.quitListener.start()

    print("Key Listener Initialized.")

if __name__ == "__main__":
  keyListener = KeyListener(lambda: exit(0)) # Should quit the blocking thread when using as module

  # Manually blocking
  keyListener.quitListener.join()
