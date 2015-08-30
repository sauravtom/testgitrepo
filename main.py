#!/usr/bin/python
# -*- coding: utf-8 -*-

import telegram
import sqlite3
import sys
import os
from youtubeSearch import srch
import time


import telebot
import youtube_dl

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

TOKEN = '126017293:AAEMvYvXxqbP7ir0X7Amortph9sr71HUg60'
tb = telebot.TeleBot(TOKEN)

con = sqlite3.connect('queue.db')
bot = telegram.Bot(token='126017293:AAEMvYvXxqbP7ir0X7Amortph9sr71HUg60')

quality_arr=[13, 17, 5, 6, 18, 43, 34, 35, 45, 22, 37, 38]
   
def addToRepliedMessages(message):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Messages(Id TEXT PRIMARY KEY,\
        Content TEXT, User TEXT );")
    cur.execute("INSERT INTO Messages VALUES (?,?,?)",(message.message_id,message.text,message.from_user.first_name))
    con.commit()

def getAllRepliedMessages():
    cur = con.cursor()
    a = cur.execute("Select Id from Messages")
    b = [int(i[0]) for i in a]
    return b


def main():
    updates = bot.getUpdates()
    all_replied_messages = getAllRepliedMessages()
    all_messages = [u.message for u in updates if u.message.text != '/start' and u.message.message_id not in all_replied_messages]
    if len(all_messages)==0:
        print "No more messages in queue"
        return
    message = all_messages[0]
    print message.text
    bot.sendMessage(chat_id=message.chat_id, 
        text="YO %s, here's your video for '%s'"%(message.from_user.first_name,message.text)) 
    tb.send_chat_action(chat_id, 'typing')
    sendVideo(message.text,message.chat_id)
    addToRepliedMessages(message)

def sendVideo(query,chat_id='724255'):
    title,id=srch(query)
    epoch = str(int(time.time()*100))
    os.system("youtube-dl -f 13 %s  -o 'video%s.%%(ext)s'"%(id,epoch))
    video = open('/Users/saurav/Desktop/jalebiBot/video%s.3gp'%epoch, 'rb')
    tb.send_message(chat_id,"Title: '%s'"%title)
    tb.send_chat_action(chat_id, 'record_video')
    tb.send_video(chat_id, video)
    os.system("rm video%s.3gp"%epoch)

def test2():
    result = ydl.extract_info(
            'https://www.youtube.com/watch?v=g5qU7p7yOY8',
            download=False
        )
    print result['ext']

@tb.message_handler(commands=['download'])
def send_welcome(message):
    tb.send_message(message.chat.id, "YO %s, here's your video for '%s'"%(message.from_user.first_name,message.text[10:]))
    #tb.reply_to(message, "YO %s, here's your video for '%s'"%(message.from_user.first_name,message.text[10:]))
    print message.text
    #print dir(message.chat)
    sendVideo(message.text[10:],message.chat.id)

def start():
    tb.polling()
    while True:
        time.sleep(5000)

if __name__ == '__main__':
    start()
    #sendVideo("food")
    #test()
    #main()
