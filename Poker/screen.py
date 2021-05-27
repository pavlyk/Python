import numpy as np
import cv2
from mss.linux import MSS as mss
from PIL import Image
import time
import pyautogui as pg

template = cv2.imread("Screen.png", cv2.IMREAD_GRAYSCALE)
# print(template)
w, h = template.shape[::-1]

# with mss.mss() as sct:
#     monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

#     while "Screen capturing":
#         last_time = time.time()
#         img = numpy.array(sct.grab(monitor))
#         cv2.imshow("OpenCV/Numpy normal", img)
#         print("fps: {}".format(1 / (time.time() - last_time)))
#         gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
#         loc = np.where(res >= 0.7)
#         for pt in zip(*loc[::-1]):
#             cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
#         cv2.imshow("Frame", img)
#         key = cv2.waitKey(1)
#         if cv2.waitKey(25) & 0xFF == ord("q"):
#             cv2.destroyAllWindows()
#             break