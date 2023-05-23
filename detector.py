
import cv2
import imutils
import numpy as np
import pytesseract
import easyocr
import random
import os
import difflib
from alt_ocr import ocr

reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

#file = f"./images/{random.choice(os.listdir('./images'))}"
#file = "./images/HSRP-NUMBER-Plate.jpg"
#print(file)

def difflib_filter(text, possible):
    #print(text, possible)
    cutoff=0.5
    close = difflib.get_close_matches(text, possible, cutoff=cutoff)
    #print(f"close: {close}")
    return close

def filtering(text_):
        strings_found = []
        for index in range(0, len(text_)):
            for x in text_[index]:
                if isinstance(x, str):
                    strings_found.append(x)
        ret = "".join(strings_found).replace(" ", "")
        #print(ret)
        return ret


def get_detected_license_plate_number(img, todays_vip_cars):
    if isinstance(img, str):
        img = cv2.imread(img, cv2.IMREAD_COLOR)

    img = cv2.resize(img, (600, 400))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    
    edged = cv2.Canny(gray, 30, 200)
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in contours:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

    mask = np.zeros(gray.shape, np.uint8)
    try:
        new_image = cv2.drawContours(
            mask,
            [screenCnt],
            0,
            255,
            -1,
        )
        new_image = cv2.bitwise_and(img, img, mask=mask)
    

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx : bottomx + 1, topy : bottomy + 1]
    except: pass
    
    text_1 = reader.readtext(img)
    #alt_ocr_text_1 = ocr(opencv_frame=Cropped) # get text from camera frame
    #filter_ = filtering(alt_ocr_text_1)
    #if alt_ocr_text_1 is False:
        #print('no license detected')
        #return
    
    difflib_filtering = difflib_filter(filtering(text_1), todays_vip_cars)
    return difflib_filtering


