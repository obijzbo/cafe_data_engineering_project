from configs.data_config import ROOT_PATH,DATA_PATH
from configs.chillox_config import DATA_Dir
from pytesseract import Output
import pytesseract
import cv2
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import os
import tkinter
from easyocr import Reader
from PIL import ImageDraw, Image
matplotlib.use('TkAgg')

def remove_lines(image):
  result = image.copy()
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

  # Remove horizontal lines
  horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
  remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
  cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

  # Remove vertical lines
  vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
  remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
  cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

  plt.imshow(result)
  plt.show()

  return result


image_path = f"{ROOT_PATH}/{DATA_PATH}/{DATA_Dir}/menu.png"
reader = Reader(['en'])
image = cv2.imread(image_path)
image = remove_lines(image)
results = reader.readtext(image)

low_precision = []
for text in results:
    if text[2]<0.45: # precision here
        low_precision.append(text)
for i in low_precision:
    results.remove(i) # remove low precision
print(results)


image2 = Image.fromarray(image)

draw = ImageDraw.Draw(image2)
for i in range(0, len(results)):
    p0, p1, p2, p3 = results[i][0]
    draw.line([*p0, *p1, *p2, *p3, *p0], fill='red', width=1)

plt.imshow(np.asarray(image2))
plt.show()
plt.savefig(f"{ROOT_PATH}/{DATA_PATH}/{DATA_Dir}/text_box.png")