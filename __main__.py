import telebot
import time
import cv2
from detector import get_detected_license_plate_number
from constants import BOT_TOKEN


CHAT_ID = "-919378243"

bot = telebot.TeleBot(BOT_TOKEN)
name, plate_number, lot_number, time_string = ""
text_format = f"""

!! [ VIP Parked ] !!                          
Name: {name}                     
Vehicle: {plate_number}
Lot no: {lot_number}                        
Time: {time_string}
"""
vid = cv2.VideoCapture(-1)

todays_vip_cars_ = ["HR26VM8771", "SDN0382X", "HR11VV9991"]
while True:
    ret, frame = vid.read()
    frame = cv2.imshow('frame', frame)
   
    x = get_detected_license_plate_number(frame, todays_vip_cars_)
    if len(x) > 0:
        print(x[0])
    elif len(x) == 0:
        print('no match')
    time.sleep(2)
    #bot.send_message(CHAT_ID, text_format)


#bot.infinity_polling(interval=0, timeout=20)

