import cv2, queue, threading, time
import os
import sys
from datetime import datetime
# from matplotlib import pyplot as plt
import pytesseract
import numpy as np
try:
  import Image
except ImportError:
  from PIL import Image
import pyocr
import pyocr.builders


def draw_bbox(imgs, bbox, colors, classes):
    img = imgs[int(bbox[0])]
    label = classes[int(bbox[-1])]
    p1 = tuple(bbox[1:3].int())
    p2 = tuple(bbox[3:5].int())
    color = random.choice(colors)
    cv2.rectangle(img, p1, p2, color, 2)
    text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0]
    p3 = (p1[0], p1[1] - text_size[1] - 4)
    p4 = (p1[0] + text_size[0] + 4, p1[1])
    cv2.rectangle(img, p3, p4, color, -1)
    cv2.putText(img, label, p1, cv2.FONT_HERSHEY_SIMPLEX, 1, [225, 255, 255], 1)


def load_classes(namesfile):
    fp = open(namesfile, "r")
    names = fp.read().split("\n")[:-1]
    return names


# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(0)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
            # print('discard previous (unprocessed) frame')
            self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
            # print('empty')
            pass
      self.q.put(frame)

  def read(self):
    return self.q.get()


def ColorDistance(rgb1,rgb2):
    '''d = {} distance between two colors(3)'''
    rm = np.int(0.5*(rgb1[0]+rgb2[0]))
    # print(rm, 'rm')
    # print('rgb1-rgb2', rgb1-rgb2)
    d = np.abs(sum((2+rm,4,3-rm)*(rgb1-rgb2)**2))**0.5
    return d


def colour_dist(fst, snd):

    rm = 0.5 * (fst[0] + snd[ 0])
    drgb = (fst - snd) ** 2
    t = np.array([2 + rm, 4 + 0 * rm, 3 - rm]).T
    return np.sqrt(np.sum(t * drgb, 1))


# Define the function to be called on mouse click
def on_click(event, x, y, flags, param):
    # Check if the mouse was actually clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        if setflop:
          flop.append({'x': x, 'y': y})
        elif setbet:
          bet.append({'x': x, 'y': y})


cap = VideoCapture(0)

color = (36,255,12)
setflop = False
dealer = False
setbet = False
bet = []
bet_rect = []
flop = []
flop_rect = []

folder = []
for i in os.walk('cards/suits'):
    folder.append(i)  
templates_suits = []
for address, dirs, files in folder:
    for file in files:
        templates_suits.append((address+'/'+file, os.path.splitext(file)[0]))

folder = []
for i in os.walk('cards/values'):
    folder.append(i)  
templates_values = []
for address, dirs, files in folder:
    for file in files:
        templates_values.append((address+'/'+file, os.path.splitext(file)[0]))

folder = []
for i in os.walk('cards/other'):
    folder.append(i)  
templates_other = []
for address, dirs, files in folder:
    for file in files:
        templates_other.append((address+'/'+file, os.path.splitext(file)[0]))

# fr = 0
cards = []
while True:
    frame = cap.read()
    frameflop = None
    
    # if len(bet) == 2:
    #   tools = pyocr.get_available_tools()
    #   tool = tools[0]
    #   img = frame[bet[0]['y']:bet[1]['y'], bet[0]['x']:bet[1]['x']]
    #   img = cv2.bitwise_not(img)
    #   ret, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    #   kernel = np.ones((5, 5), np.uint8)
    #   erode = cv2.erode(thresh, kernel, iterations = 1)
    #   result = cv2.bitwise_or(img, erode)
    #   cv2.imwrite('bet.png', result)
    #   digits = tool.image_to_string(
    #       Image.open('bet.png'),
    #       builder=pyocr.tesseract.DigitBuilder()
    #   ) 
    # frame = cv2.rectangle(frame, (bet[0]['x'], bet[0]['y']), (bet[1]['x'], bet[1]['y']), color, 1)

    # Распознование цифр
    # if len(bet) == 2:
    #   hh = int((bet[1]['y'] - bet[0]['y'])*0.85)
    #   frame = cv2.rectangle(frame, (bet[0]['x'],bet[0]['y']), (bet[1]['x'],bet[1]['y']), (36,255,12), 1)
    #   img = frame[bet[0]['y']:bet[1]['y'], bet[0]['x']:bet[1]['x']]
    #   digits = []
    #   for i in templates_other:
    #     if i[1] == '.DS_Store':
    #       continue

    #     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     template = cv2.imread(i[0],0)
    #     # if i[1] == 'BB':
    #     #   template = cv2.resize(template,(int(hh/1.8),int(hh/2)))
    #     # else:
    #     #   template = cv2.resize(template,(int(hh),int(hh/2)))

    #     w, h = template.shape[::-1]
    #     res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    #     loc = np.where(res >= 0.65)
    #     for pt in zip(*loc[::-1]):
    #       coord1 = (pt[0]+bet[0]['x'], pt[1]+bet[0]['y'])
    #       coord2 = (pt[0]+bet[0]['x']+w, pt[1]+bet[0]['y']+h)
    #       digits.append({'text':i[1], 'coord1': coord1, 'coord2': coord2, 'coord3': (coord1[0] , coord1[1]-10)})
      
    #   unique_digit = []
    #   for digit in digits:
    #     itIsUnique = True
    #     for i in unique_digit:
    #       quantile1 = int(digit['coord1'][0] + (digit['coord2'][0] - digit['coord1'][0]) * 0.8)
    #       quantile2 = int(digit['coord2'][0] - (digit['coord2'][0] - digit['coord1'][0]) * 0.8)
          
    #       if quantile1 > i['coord2'][0] or quantile2 < i['coord1'][0]:
    #         pass
    #       else:
    #         itIsUnique = False
    #     if itIsUnique:
    #       unique_digit.append(digit)

    #   print('unique_digit')
    #   print(unique_digit)
    #   left1 = {'x1':0,'x2':0,'value':''}
    #   left2 = {'x1':0,'x2':0,'value':''}
    #   for digit in unique_digit:
    #     print('digit[coord1][0]', digit['coord1'][0])
    #     print('left1[x1]', left1['x1'])
    #     if left1['x1'] == 0:
    #       left1['x1'] = digit['coord1'][0]
    #       left1['x2'] = digit['coord2'][0]
    #       left1['value'] = digit['text']
    #     elif digit['coord1'][0] < left1['x1']:
    #       left2['x1'] = left1['x1']
    #       left1['x2'] = left1['x2']
    #       left2['value'] = left1['value']
          
    #       left1['x1'] = digit['coord1'][0]
    #       left1['value'] = digit['text']
    #       left1['x2'] = digit['coord2'][0]
    #     else:
    #       left2['x1'] = digit['coord1'][0]
    #       left2['value'] = digit['text']
    #       left2['x2'] = digit['coord2'][0]

    #     frame = cv2.rectangle(frame, digit['coord1'], digit['coord2'], (36,255,12), 1)
    #     # cv2.putText(frame, digit['text'], digit['coord3'], cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    #   print('left1', left1)
    #   print('left2', left2)
    #   bet_text = ''
    #   v1 = left1['value']
    #   v2 = left2['value']
    #   if v2 != '':
    #     if left2['x1'] - left1['x2'] < -2:
    #       bet_text = f'{v1} {v2}'
    #     else:
    #       bet_text = f'{v1} - {v2}'
    #     cv2.putText(frame, bet_text, (bet[0]['x'], bet[0]['y'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    if len(flop_rect) == 5:
      cards_frames = []
      cards_frames.append(frame[flop_rect[0]['y1']:flop_rect[0]['y2'], flop_rect[0]['x1']:flop_rect[0]['x2']])
      cards_frames.append(frame[flop_rect[1]['y1']:flop_rect[1]['y2'], flop_rect[1]['x1']:flop_rect[1]['x2']])
      cards_frames.append(frame[flop_rect[2]['y1']:flop_rect[2]['y2'], flop_rect[2]['x1']:flop_rect[2]['x2']])
      cards_frames.append(frame[flop_rect[3]['y1']:flop_rect[3]['y2'], flop_rect[3]['x1']:flop_rect[3]['x2']])
      cards_frames.append(frame[flop_rect[4]['y1']:flop_rect[4]['y2'], flop_rect[4]['x1']:flop_rect[4]['x2']])

      card = ['','','','','']
      suit = ['','','','','']
      maxcard = [0,0,0,0,0]
      maxsuit = [0,0,0,0,0]
      left_corners = [[],[],[],[],[]]
      for cr in range(5):
        for i in templates_values:
          img_gray = cv2.cvtColor(cards_frames[cr], cv2.COLOR_BGR2GRAY)
          template = cv2.imread(i[0],0)
          w, h = template.shape[::-1]
          res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
          loc = np.where(res >= 0.60)
          for pt in zip(*loc[::-1]):
            if res[pt[1]][pt[0]] > maxcard[cr]:
              card[cr] = i[1]
              maxcard[cr] = res[pt[1]][pt[0]]
              left_corners[cr] = [pt[0],pt[1],pt[0]+w,pt[1]+h]

      print('flop ',card[0],suit[0],card[1],suit[1],card[2],suit[2],card[3],suit[3],card[4],suit[4])
      if len(left_corners) > 0 and len(left_corners[0]) > 0:
        x1 = flop_rect[0]['x1'] + left_corners[0][0]
        y1 = flop_rect[0]['y1']+left_corners[0][1]
        x2 = flop_rect[0]['x1'] + left_corners[0][2]
        y2 = flop_rect[0]['y1']+left_corners[0][3]
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)
        frame = cv2.rectangle(frame, (int((x1+x2)/2)-2, y2+10), (int((x1+x2)/2)+2, y2+12), color, 1)
        colorf = frame[y2+11,int((x1+x2)/2)]
        pcol = ''
        if colorf[1] > colorf[0] and colorf[1] > colorf[2]:
          pcol = 'clubs'
        if colorf[0] > colorf[1] and colorf[0] > colorf[2]:
          pcol = 'diamonds'
        if colorf[2] > colorf[1] and colorf[2] > colorf[0]:
          pcol = 'heart'
        if colorf[0] < 150 and colorf[1] < 150 and colorf[2] < 150:
          pcol = 'space'
        cv2.putText(frame, pcol, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    
    if len(flop) == 2:
      w = flop[1]['x'] - flop[0]['x']
      for i in range(5):
        new_rect = {'x1':int(flop[0]['x']+w*(i)), 'x2':int(flop[0]['x']+(w)*(i+1)), 'y1':flop[0]['y'], 'y2':flop[1]['y']}
        frame = cv2.rectangle(frame, (new_rect['x1'], new_rect['y1']), (new_rect['x2'], new_rect['y2']), color, 1)
        if len(flop_rect) != 5:
          flop_rect.append(new_rect)

    if setflop:
      center = (int(len(frame[0])/2), 20)
      cv2.putText(frame, 'Set flop', center, cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)  
    elif setbet:
      # print('setbet')
      center = (int(len(frame[0])/2), 20)
      cv2.putText(frame, 'Set bet', center, cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)  

    cards = []
    cv2.imshow("frame", frame)
    # Listen to mouse events
    cv2.setMouseCallback("frame", on_click)
    # Wait for action

    k = chr(cv2.waitKey(1)&255)
    if k == 'q':
        break
    if k == 'd':
        dealer = True
    if k == 'b':
      setbet = not setbet
      if setflop:
        bet = []
        bet_rect = []  
    if k == 'f':
      setflop = not setflop
      if setflop:
        flop = []
        flop_rect = []

        





# Определить рамеры стола
# Определить свои карты
# Перекрытие найденных площадей чтобы выбрать более вероятную
# Какие площади рядом чтобы понять какая карта + масть
# Определить положение диллера (вхождение найденного прямоугольника в какие то определенные зоны от всего размера стола)
# Определить сколько противников в игре и в какой они позиции
# Определить карты стола и какая улица сейчас

# Парсер диапазонов по скриншоту

# Определить банк


# s = 0 # площадь области пересечения

# x1, y1 = 2, 2 #координаты левого нижнего угла первого прямоугольника
# x2, y2 = 4, 4 #координаты правого верхнего угла первого прямоугольника
# x3, y3 = 3, 1 #координаты левого нижнего угла второго прямоугольника
# x4, y4 = 6, 3 #координаты правого верхнего угла второго прямоугольника

# # границы области пересечения
# left = max(x1, x3) # левая
# bottom = max(y1, y3) # нижняя
# right = min(x2, x4) # правая
# top = min(y2, y4) # верхняя

# width = right — left # ширина пересечения
# height = top — bottom # высота пересечения

# # если ширина и высота области пересечения меньше или равны 0
# if width <= 0 or height <= 0:
# # то его площадь 0
# ____print(0)
# else:
# # если больше 0, то выводим площадь
# ____print(width * height)

# _ нужно заменить на пробелы