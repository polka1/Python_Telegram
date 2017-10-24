import telebot
import time
import requests
import traceback
import datetime as dt
#from methods import command
#import configparser

TOKEN = "389787796:AAFYpBhLBA6LYk08YudRQxqRdg6Ps1yxc0E"
URL_WNOW = "http://api.openweathermap.org/data/2.5/weather"
URL_W24 = "http://api.openweathermap.org/data/2.5/forecast"
TOKEN_W = "82a710f3434ff0d39d66605caa9e49e8"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
MAKET_24 = "{0} | {1} °C {3} {2} м/с\n"
text_help = "Бог доопоможе!"
try:
    bot = telebot.TeleBot(TOKEN)
except:
    print("---Error: Failed to implement [telebot.TeleBot(TOKEN)]")
print("...")

def write_logs(ex, tb, is_print):
    with open('logs.txt', 'a') as f:
        time_now = str(dt.datetime.now()) + " --- "
        f.write("\n"+time_now+"\n"+str(tb.format_exc())+"###\n")
        if(is_print):print(tb.format_exc())


def chat_logs(msg):
    with open('chatLogs.txt', 'a') as f:
        time_now = str(dt.datetime.now()) + " --- "
        f.write(time_now + msg + "\n")


def formattime(unixtime):
    utftime = dt.datetime.fromtimestamp(
        int(unixtime)
    ).strftime("%Y-%m-%d %H:%M:%S")
    return utftime 

# Commands
@bot.message_handler(commands=["help", "h"])
def attach_command(cmd):
    bot.send_message(chat_id=cmd.chat.id, text=text_help)
    text = "-- {0} id: {1}| user: {2}| msg: {3}".format(
        formattime(cmd.date), cmd.from_user.id, 
        cmd.from_user.first_name, cmd.text)
    print(text)

# Daily weather
#TODO
@bot.message_handler(commands=['wKyiv', 'kyiv'])
def w_kyiv(cmd):
    weather_bot = Weather(TOKEN_W)
    bot.send_message(chat_id=cmd.chat.id, text=weather_bot.weather_now('Kyiv'))
    text = "-- {0} id: {1}| user: {2}| msg: {3}".format(
        formattime(cmd.date), cmd.from_user.id, 
        cmd.from_user.first_name, cmd.text)
    print(text)

@bot.message_handler(commands=['wKharkiv', 'kharkiv'])
def w_kharkiv(cmd):
    weather_bot = Weather(TOKEN_W)
    bot.send_message(chat_id=cmd.chat.id, text=weather_bot.weather_now('Kharkiv'))
    text = "-- {0} id: {1}| user: {2}| msg: {3}".format(
        formattime(cmd.date), cmd.from_user.id, 
        cmd.from_user.first_name, cmd.text)
    print(text)

@bot.message_handler(commands=['wPoltava', 'poltava'])
def w_poltava(cmd):
    weather_bot = Weather(TOKEN_W)
    bot.send_message(chat_id=cmd.chat.id, text=weather_bot.weather_now('Poltava'))
    text = "-- {0} id: {1}| user: {2}| msg: {3}".format(
        formattime(cmd.date), cmd.from_user.id, 
        cmd.from_user.first_name, cmd.text)
    print(text)

@bot.message_handler(commands=['wIvano-Frankivsk', 'ivano_frankivsk'])
def w_frankivsk(cmd):
    weather_bot = Weather(TOKEN_W)
    bot.send_message(chat_id=cmd.chat.id, text=weather_bot.weather_now('Ivano-Frankivsk'))
    text = "-- {0} id: {1}| user: {2}| msg: {3}".format(
        formattime(cmd.date), cmd.from_user.id, 
        cmd.from_user.first_name, cmd.text)
    print(text)

# 24 weather
@bot.message_handler(commands=['w24Kyiv', 'kyiv24'])
def w24_kyiv(cmd):
    weather_bot = Weather(TOKEN_W)
    bot.send_message(chat_id=cmd.chat.id, text=weather_bot.weather_24('Kyiv'))
    text = "-- {0} id: {1}| user: {2}| msg: {3}".format(
        formattime(cmd.date), cmd.from_user.id, 
        cmd.from_user.first_name, cmd.text)
    print(text)

@bot.message_handler(commands=['w24kharkiv', 'kharkiv24'])
def w24_kharkiv(cmd):
    weather_bot = Weather(TOKEN_W)
    bot.send_message(chat_id=cmd.chat.id, text=weather_bot.weather_24('Kharkiv'))
    text = "-- {0} id: {1}| user: {2}| msg: {3}".format(
        formattime(cmd.date), cmd.from_user.id, 
        cmd.from_user.first_name, cmd.text)
    print(text)

@bot.message_handler(commands=['w24Poltava', 'poltava24'])
def w24_poltava(cmd):
    weather_bot = Weather(TOKEN_W)
    bot.send_message(chat_id=cmd.chat.id, text=weather_bot.weather_24('Poltava'))
    text = "-- {0} id: {1}| user: {2}| msg: {3}".format(
        formattime(cmd.date), cmd.from_user.id, 
        cmd.from_user.first_name, cmd.text)
    print(text)

@bot.message_handler(commands=['w24Ivano-Frankivsk', 'ivano_frankivsk24'])
def w24_frankivsk(cmd):
    weather_bot = Weather(TOKEN_W)
    bot.send_message(chat_id=cmd.chat.id, text=weather_bot.weather_24('Ivano-Frankivsk'))
    text = "-- {0} id: {1}| user: {2}| msg: {3}".format(
        formattime(cmd.date), cmd.from_user.id, 
        cmd.from_user.first_name, cmd.text)
    print(text)

#
#@bot.message_handler(content_types=["text"])
def repeat_msg(message):
    print(message)
    bot.send_message(message.chat.id, message.text)

# Weather API
CITY_LIST = {'Kyiv': 703448, 'Poltava': 696643, 'Ivano-Frankivsk': '707471', 'Kharkiv': '706483'}


class Weather:
    def __init__(self, token):
        self.token = token

    def weather_now(self, city):
        try:
            params = {'id': CITY_LIST[city], 'units': 'metric', 'lang': 'ua', 'APPID': self.token}
            resp = requests.get(URL_WNOW, params=params)
            data = resp.json()
            text_data = (data['weather'][0]['description'], data['main']['temp'],
                         data['main']['temp_min'], data['main']['temp_max'],
                         data['wind']['speed'])
            text_info = "За вікном {0}\nТемпература {1}\nМінімальна {2}\nМаксимальна {3}\nВітер {4} м/с"\
                .format(*text_data)
        except Exception as ex:
            text_info = ex
            write_logs(ex, traceback, False)
        return text_info

    def weather_24(self, city):
        try:
            params = {'id': CITY_LIST[city], 'units': 'metric', 'lang': 'ua', 'APPID': self.token}
            resp = requests.get(URL_W24, params=params)
            data = resp.json()
            count = 0
            info_24 = ""
            day_of_week = ()
            flag = True
            for i in data['list']:
                day_now = i['dt_txt']
                # print(i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']),
                #       i['wind']['speed'], i['weather'][0]['description'])
                if count == 0:
                    date1 = dt.datetime.strptime(day_now, TIME_FORMAT).date().strftime("%A, %m")
                    day_of_week = date1.split(',')[0]
                    dt_str_numb = date1.split(',')

                    info_24 = "{0}, {1}\n".format(translate(dt_str_numb[0]), int(dt_str_numb[1]))

                if dt.datetime.strptime(day_now, TIME_FORMAT).date().strftime("%A, %m").split(',')[0] \
                        != day_of_week and flag:
                    day_next = dt.datetime.strptime(day_now, TIME_FORMAT).date().strftime("%A, %m")
                    # print(day_next)
                    dt_str_numb = day_next.split(',')
                    info_24 = info_24 + "{0}, {1}\n".format(translate(dt_str_numb[0]), int(dt_str_numb[1]))
                    flag = False
                every_third = MAKET_24.format(dt.datetime.strptime(i['dt_txt'], TIME_FORMAT).time().strftime("%H:%M"),
                                              '{0:+3.0f}'.format(i['main']['temp']),
                                              round(i['wind']['speed']), i['weather'][0]['description'])
                info_24 = info_24 + every_third
                count += 1
                if count == 9:
                    break

        except Exception as ex:
            info_24 = ex
            write_logs(ex, traceback, False)
        # print(info_24)
        return info_24


def translate(value):
    daysOfWeek = {'Sunday': 'Вс', 'Monday': 'Пн', 'Tuesday': 'Вт', 'Wednesday': 'Ср',
                  'Thursday': 'Чт', 'Friday': 'Пт', 'Saturday': 'Сб'}
    return daysOfWeek[value]


if __name__ == '__main__':
    print("Weather bot is started")
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            print("Process: [bot.polling] returned error")
            time.sleep(15)
            bot.polling(none_stop=True)

