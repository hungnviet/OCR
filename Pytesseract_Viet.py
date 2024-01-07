import cv2
import pytesseract
import os

# Read the images
img = cv2.imread("smalltest.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

boxes = pytesseract.image_to_data(img)
# print(boxes)

for x,b in enumerate(boxes.splitlines()):
    if x != 0:
        b = b.split()
        if len(b) == 12:
            print(b[11])