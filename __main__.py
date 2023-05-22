import telebot
import time
import cv2
from detector import get_detected_license_plate_number
from constants import BOT_TOKEN, CHAT_ID
from database_functions import get_data_from_database, get_relatives_of_license_plate

bot = telebot.TeleBot(BOT_TOKEN)
vid = cv2.VideoCapture(0)

todays_vip_cars_ = get_data_from_database('vehicle')
plate_number = ''
name = ''
time_string = ''
while True:
    print('looping...')
    ret, frame = vid.read()
    try:
        plate_number = get_detected_license_plate_number(frame, todays_vip_cars_)
        name = get_relatives_of_license_plate(plate_number, 'vip_name')
        time_string = get_relatives_of_license_plate(plate_number, 'arrival')
    except IndexError:
        pass
    if name is not None:
        text_format = f"""
        !! [ VIP Parked ] !!                          
        Name: {name}                     
        Vehicle: {plate_number}                       
        Time: {time_string}
        """
    frame = cv2.imshow('frame', frame)
    if len(plate_number) > 0:
        print(plate_number[0])
        bot.send_message(CHAT_ID, text_format)
    elif len(plate_number) == 0:
        print('no match')
    


#bot.infinity_polling(interval=0, timeout=20)

