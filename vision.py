# from time import sleep, time
import ctypes
import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import pyautogui

class VisionCore:
    # Desktop hwnd
    hwnd = None
    # Window info
    width = 0
    height = 0
    pos_x = 0
    pos_y = 0
    # Images
    mount_img = None

    # Constructor
    def __init__(self):
      window_rect = self.getWindowRect()

      self.width = window_rect[2] - window_rect[0]
      self.height = window_rect[3] - window_rect[1]
      self.pos_x = window_rect[0]
      self.pos_y = window_rect[1]

      # self.mount_img = cv2.imread("img/mount.jpg", cv2.IMREAD_UNCHANGED)

      self.hwnd = win32gui.GetDesktopWindow()

      # print("Window size x{} y{}".format(self.width, self.height))
      # print("Window position x{} y{}".format(self.pos_x, self.pos_y))

    def getWindowRect(focus = False):
      WINDOW_TITLE = "LOST ARK"
      fullWindowTitle = WINDOW_TITLE
      for x in pyautogui.getAllWindows():
        if WINDOW_TITLE in x.title:
          fullWindowTitle = x.title
          break
      hwnd = win32gui.FindWindow(None, fullWindowTitle)
      if not hwnd:
        ctypes.windll.user32.MessageBoxW(0, "Lost Ark client not found.", "Error", 0)
        raise Exception("Window not found: {}".format(fullWindowTitle))
      elif focus:
        win32gui.SetForegroundWindow(hwnd)

      return win32gui.GetWindowRect(hwnd)

    def imshow(self, data):
      cv2.imshow("Imshow", data)

    def matchTemplateLocation(self, img, threshold, untilFound=False):
      result = cv2.matchTemplate(
        self.getScreenshot(), img, cv2.TM_CCOEFF_NORMED)

      locations = np.where(result >= threshold)
      locations = list(zip(*locations[::-1]))

      if len(locations) >= 1:
        return self.normalizePosition(locations[0], img.shape)
      else:
        if untilFound:
          return self.matchTemplateLocation(img, threshold-0.05, untilFound=True)
        else:
          return None

    def normalizePosition(self, tuple, shape):
      return (tuple[0] + self.pos_x + shape[1] / 2, tuple[1] + self.pos_y + shape[0] / 2)

    def getScreenshot(self, debugFileName=None):
      # Create a device context
      desktopDc = win32gui.GetWindowDC(self.hwnd)
      imgDc = win32ui.CreateDCFromHandle(desktopDc)

      # Create a memory device context
      memDc = imgDc.CreateCompatibleDC()

      # Create a bitmap object
      screenshot = win32ui.CreateBitmap()
      screenshot.CreateCompatibleBitmap(imgDc, self.width, self.height)
      memDc.SelectObject(screenshot)

      # Memory device context to the theme
      memDc.BitBlt((0, 0), (self.width, self.height), imgDc,
                    (self.pos_x, self.pos_y), win32con.SRCCOPY)

      # Convert the raw data into a format opencv can read
      if debugFileName:
          screenshot.SaveBitmapFile(memDc, debugFileName)
      signedIntsArray = screenshot.GetBitmapBits(True)
      img = np.fromstring(signedIntsArray, dtype="uint8")
      img.shape = (self.height, self.width, 4)

      # Memory release
      imgDc.DeleteDC()
      memDc.DeleteDC()
      win32gui.ReleaseDC(self.hwnd, desktopDc)
      win32gui.DeleteObject(screenshot.GetHandle())

      img = img[..., :3]

      img = np.ascontiguousarray(img)

      return img

    def locateMapPointer(self):
      image = self.getScreenshot()
      pointer_color = np.array([255, 179, 97])
      mask = cv2.inRange(image, pointer_color, pointer_color)

      cnt = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)
      cnt = cnt[0] if len(cnt) == 2 else cnt[1]
      largestCnt = None
      maxArea = -1
      for i in range(len(cnt)):
        area = cv2.contourArea(cnt[i])
        if area > maxArea:
          largestCnt = cnt[i]
          maxArea = area
      center = cv2.moments(largestCnt)
      cX = int(center["m10"] / center["m00"])
      cY = int(center["m01"] / center["m00"])

      # debugImg = cv2.circle(image.copy(), (cX, cY), radius=0,
      #                 color=(0, 0, 255), thickness=4)
      # self.imshow(debugImg)

      return (cX, cY)