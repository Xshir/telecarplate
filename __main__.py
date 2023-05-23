import telebot
import time
import cv2
from detector import get_detected_license_plate_number
from constants import BOT_TOKEN, CHAT_ID
from database_functions import list_all_values, list_vip_names, list_license_plates

bot = telebot.TeleBot(BOT_TOKEN)
vid = cv2.VideoCapture(1)

todays_vip_cars_ = list_license_plates

while True:
    print('looping...')
    ret, frame = vid.read()
    if ret is True:
        plate_number = get_detected_license_plate_number(frame, todays_vip_cars=todays_vip_cars_)
        if plate_number != []:
            print(plate_number[0])
    else: print('no frame')
    #if name is not None:
       # text_format = f"""
       # !! [ VIP Parked ] !!                          
       # Name: {name}                     
       # Vehicle: {plate_number}                       
       # Time: {time_string}
       # """
    cv2.imshow('frame', frame)
    if plate_number is not None:
        if len(plate_number) > 0:
            print(plate_number[0])
            bot.send_message(CHAT_ID, plate_number[0])
        elif len(plate_number) == 0:
            print('no match')
    if cv2.waitKey(1) == ord('q'):
        break
    


#bot.infinity_polling(interval=0, timeout=20)

