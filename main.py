import time
from datetime import datetime
from threading import Thread

import telebot
import transliterate
from classes import *
import re

token = '900930331:AAFVf9CDI-XVHV4Uk3wSFjbGwAMysrOfSY0'
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot(token=token)

counter = 0
# pars=['название события','дату','место']
events = dict()
last_event = ''


@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.send_message(message.chat.id, 'Чтобы начать создание события отправьте любое сообщение.')


@bot.message_handler(content_types=['text'])
def getmessage(message):
    global counter
    global events, last_event
    if message.chat.type == 'private':
        if counter == 0:
            bot.send_message(message.chat.id, 'Введите название события: ')
        if counter == 1:
            events[message.text] = Event(message.text, None, None, None)
            last_event = message.text
            bot.send_message(message.chat.id, 'Введите время события в формате ЧЧ:ММ')
        if counter == 2:
            time = message.text
            if len(time) == 5 and time[2] == ':' and re.fullmatch('[0-2]*', time[:1]) and \
                    re.fullmatch('[0-9]*', time[1:2]) and re.fullmatch('[0-5]*', time[3:4]) and \
                    re.fullmatch('[0-9]*', time[4:]) and int(time[0:2]) < 24:
                events[last_event].time = time
                bot.send_message(message.chat.id, 'Введите место события: ')
            else:
                bot.send_message(message.chat.id, 'Введите время события в формате ЧЧ:ММ')
                counter = 1
        if counter == 3:
            events[last_event].place = message.text
            bot.send_message(message.chat.id, 'Введите число участников: ')
        if counter == 4:
            events[last_event].num = int(message.text)
            bot.send_message(message.chat.id, events[last_event].get_description())
            bot.send_message(-369417918, events[last_event].get_description())

            event_inviting = '/' + '_'.join(
                (transliterate.translit(events[last_event].title, 'ru', reversed=True)).split())
            bot.send_message(-369417918, 'Чтобы присоединиться к событию введите ' + event_inviting)

        counter = (counter + 1) % 5

    if message.chat.type == 'group':
        if message.text[0] == '/':
            text = message.text
            ind1 = 1
            ind2 = text.find('@')
            if ind2 == -1:
                ind2 = len(text)
            event_title = ' '.join((transliterate.translit(text[ind1:ind2], 'ru')).split('_'))
            if events[event_title] is not None:
                if len(events[event_title].members) < events[event_title].num - 1:
                    if not events[event_title].contains_user(message.from_user.id):
                        events[event_title].add_member(
                            User(message.from_user.id, message.from_user.username, message.from_user.first_name,
                                 message.from_user.last_name))
                else:
                    if len(events[event_title].members) < events[event_title].num:
                        events[event_title].add_member(
                            User(message.from_user.id, message.from_user.username, message.from_user.first_name,
                                 message.from_user.last_name))
                    text = '@' + ' @'.join(events[event_title].get_usernames())
                    text = text + '\nВы присоединились к событию: \n' + events[event_title].get_description()
                    bot.send_message(message.chat.id, text)

            # print(events[event_title].get_usernames())


def sender():
    global events
    while True:
        # do
        currentTime = int(str(datetime.now())[11:13]) * 60 + int(str(datetime.now())[14:16])
        for key in events:
            if events[key].time is not None and events[key].is_announced == 0:
                eventTime = int(events[key].time[:2]) * 60 + int(events[key].time[3:])
                if currentTime >= eventTime - 1:
                    events[key].is_announced = 1
                    text = '@' + ' @'.join(events[key].get_usernames())
                    text = text + '\nЧерез 1 минуту начнется событие: \n' + events[key].get_description()
                    print(text)
                    bot.send_message(-369417918, text)
            if events[key].time is not None and events[key].is_announced == 1:
                eventTime = int(events[key].time[:2]) * 60 + int(events[key].time[3:])
                if eventTime <= currentTime:
                    events[key].is_announced = 2
                    text = '@' + ' @'.join(events[key].get_usernames())
                    text = text + '\nНачалось событие: \n' + events[key].get_description()
                    print(text)
                    bot.send_message(-369417918, text)
        time.sleep(1)
        print('Секунда')


t = Thread(target=sender)
t.start()

bot.polling(none_stop=True)
