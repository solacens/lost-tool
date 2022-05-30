from constants import *

import ctypes
import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import pyautogui
import pytesseract
import time
import re
import os

pytesseract.pytesseract.tesseract_cmd = os.path.dirname(os.path.realpath(__file__)) + r"/tesseract/tesseract.exe"

class VisionCore:
  # OpenCV
  cv2 = cv2
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
    if True:
      window_rect = self.getWindowRect()

      self.width = window_rect[2] - window_rect[0]
      self.height = window_rect[3] - window_rect[1]
      self.pos_x = window_rect[0]
      self.pos_y = window_rect[1]

      # self.mount_img = cv2.imread("img/mount.jpg", cv2.IMREAD_UNCHANGED)

      self.hwnd = win32gui.GetDesktopWindow()

    # print("Window size x{} y{}".format(self.width, self.height))
    # print("Window position x{} y{}".format(self.pos_x, self.pos_y))

  @staticmethod
  def getWindowRect(focus = False):
    fullWindowTitle = LT_SEARCH_WINDOW_TITLE
    for x in pyautogui.getAllWindows():
      if LT_SEARCH_WINDOW_TITLE in x.title:
        fullWindowTitle = x.title
        break
    hwnd = win32gui.FindWindow(None, fullWindowTitle)
    if not hwnd:
      ctypes.windll.user32.MessageBoxW(0, "Lost Ark client not found.", "Error", 0)
      raise Exception("Window not found: {}".format(fullWindowTitle))
    elif focus:
      win32gui.SetForegroundWindow(hwnd)

    return win32gui.GetWindowRect(hwnd)

  @staticmethod
  def focus():
    VisionCore.getWindowRect(True)

  def imshow(self, data):
    cv2.imshow("Imshow", data)
    cv2.waitKey()

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

  def getScreenshot(self, relativeCoordinates=None, debugFileName=None):
    # Create a device context
    desktopDc = win32gui.GetWindowDC(self.hwnd)
    imgDc = win32ui.CreateDCFromHandle(desktopDc)

    # Create a memory device context
    memDc = imgDc.CreateCompatibleDC()

    # Get position and size
    width = self.width
    height = self.height
    pos_x = self.pos_x
    pos_y = self.pos_y
    if relativeCoordinates is not None:
      width = relativeCoordinates[2] - relativeCoordinates[0]
      height = relativeCoordinates[3] - relativeCoordinates[1]
      pos_x = relativeCoordinates[0] + pos_x
      pos_y = relativeCoordinates[1] + pos_y

    # Create a bitmap object
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(imgDc, width, height)
    memDc.SelectObject(screenshot)

    # Memory device context to the theme
    memDc.BitBlt((0, 0), (width, height), imgDc, (pos_x, pos_y), win32con.SRCCOPY)

    # Convert the raw data into a format opencv can read
    if debugFileName:
        screenshot.SaveBitmapFile(memDc, debugFileName)
    signedIntsArray = screenshot.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype="uint8")
    img.shape = (height, width, 4)

    # Memory release
    imgDc.DeleteDC()
    memDc.DeleteDC()
    win32gui.ReleaseDC(self.hwnd, desktopDc)
    win32gui.DeleteObject(screenshot.GetHandle())

    img = img[..., :3]

    img = np.ascontiguousarray(img)

    return img

  def getExcavatingScreenshot(self):
    return self.getScreenshot(relativeCoordinates=[956, 465, 964, 500])

  def getFishingPromptAvagerColor(self):
    image = self.getScreenshot(relativeCoordinates=[956, 465, 964, 500])
    return image.mean(axis=0).mean(axis=0)

  def handleTextGrayscaleTransform(self, image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0,0,0], dtype=np.uint8)
    upper_white = np.array([100,100,255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    filtered = cv2.bitwise_and(image, image, mask= mask)
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    return gray

  def getHealthBarScreenshot(self):
    image = self.getScreenshot(relativeCoordinates=[627, 956, 857, 972])
    return self.handleTextGrayscaleTransform(image)

  def getLifeEnergyBarScreenshot(self):
    image = self.getScreenshot(relativeCoordinates=[906, 916, 1036, 932])
    return self.handleTextGrayscaleTransform(image)

  def cleanText(self, text):
    allowedText = re.sub(r"[^0-9(/+]", "", text)
    return re.sub(r"(\(\+[0-9]+)?", "", allowedText)

  def convertTextPair(self, text):
    m = re.match(r"([0-9]+)/([0-9]+)", text)
    if m is not None:
      return (m.group(1), m.group(2))
    return None

  def getHealth(self):
    image = self.getHealthBarScreenshot()
    return self.convertTextPair(self.cleanText(pytesseract.image_to_string(image)))

  def getLifeEnergy(self):
    image = self.getLifeEnergyBarScreenshot()
    return self.convertTextPair(self.cleanText(pytesseract.image_to_string(image)))

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

class Vision:
  def __init__(self):
    self.core = VisionCore()

    # excavating
    # img = cv2.imread("opencv/Screenshot_2022-05-21_131745.png")
    # crop_img = img[718:748, 739:1172]
    # cv2.imshow("cropped", crop_img)

    # print(self.core.getLifeEnergy())
    # print(self.core.getHealth())

    print("<Vision> Initialized.")

  def detectRapidColorChange(self, colorNew, colorOld = None, threshold = 0.9):
    if colorOld is None:
      return False
    change = not np.all([(abs(colorNew[0] / colorOld[0]) > threshold), (abs(colorNew[1] / colorOld[1]) > threshold), (abs(colorNew[2] / colorOld[2]) > threshold)])
    # print(change)
    return change

  def waitTillFishingNotification(self):
    colorOld = None
    colorNew = None
    while True:
      colorOld = colorNew
      colorNew = self.core.getFishingPromptAvagerColor()
      if self.detectRapidColorChange(colorNew, colorOld):
        break
      time.sleep(0.025)

if __name__ == "__main__":
  Vision()
