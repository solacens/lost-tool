from pynput.keyboard import Listener, Controller

class KeyReleaser:
  keyboard = Controller()

  def __init__(self):
    def onPress(key):
      try:
        if key.char == 'g':
          print("Release G!")
          self.keyboard.release('g')
      except AttributeError:
        pass

    self.listener = Listener(on_press=onPress)
    self.listener.start()

    print("<Key Repeater> Initialized.")

if __name__ == "__main__":
  keyReleaser = KeyReleaser()

  # Any blocking function
  keyReleaser.listener.join()
