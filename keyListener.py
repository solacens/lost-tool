from pynput.keyboard import GlobalHotKeys

class KeyListener:
  def __init__(self, config):
    self.listener = GlobalHotKeys(config)
    self.listener.start()

    print("<Key Listener> Initialized.")

if __name__ == "__main__":
  keyListener = KeyListener({
    "<ctrl>+<shift>+q": lambda: print("Quit") or exit(0)
  })

  # Manually blocking
  keyListener.listener.join()
