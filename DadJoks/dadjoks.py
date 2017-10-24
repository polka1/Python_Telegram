#440648404:AAHFGa78si7apcmpIWRtawSZCn5LTN4WGLo
#https://icanhazdadjoke.com/
import traceback

import requests
import time
from datetime import datetime as dt
import telegram
from telegram.error import TimedOut

TOKEN = "telegram_key"
DAD_ADR = "https://icanhazdadjoke.com/slack"
cmd_joke = "/joke"
cmd_help = "/help"
cmd_tnx = "tnx u!"
help_text = "God to the rescue"
tnxu_text = "ILY bro 🤘 "




def writeLogs(ex, tb, is_print):
    with open('logs.txt', 'a') as f:
        time_now = str(dt.now()) + " -+- "
        f.write("\n"+time_now+"\n"+str(tb.format_exc())+"###\n")
        if(is_print):print(tb.format_exc())


def chatLogs(msg):
    with open('chatLogs.txt', 'a') as f:
        time_now = str(dt.now()) + " --- "
        f.write(time_now + msg + "\n")

class BotHandler:
    def __init__(self, TOKEN):
        self.last_msg_time = dt.now()
        self.token = TOKEN
        self.api_url = DAD_ADR

    def request_to_user(self):
        last_offset = 0
        while True:
            last_offset = self.get_updates(last_offset)

    def get_updates(self, offset):
        try:
            update = telegram.Bot(self.token)
            pkg = update.get_updates(offset=offset, timeout=30)[0]
            offset = pkg.update_id
            new_msg_time = pkg.message.date
            if new_msg_time != self.last_msg_time:
                self.last_msg_time = new_msg_time
                pkg_msg = pkg.message.text
                pkg_user_name = pkg.message.from_user.first_name
                pkg_chat_id = pkg.message.chat_id
                pkg_user_id = pkg.message.from_user.id
                self.user_msg(new_msg_time, pkg_user_id, pkg_user_name, pkg_msg)
                answer = self.choose_answer(pkg_msg)
                if answer:
                    update.send_message(chat_id=pkg_chat_id, text=answer, reply_markup=self.create_buttons())
        except TimedOut as t_er:
            writeLogs(t_er, traceback, False)
            #print(str(dt.now()) + " " + "Telegram TimedOut error:\n", t_er)
            time.sleep(3)
        except IndexError:
            pass                #30 сек сервак пытается забрать адпейты. если их нет, вываливается ошибка. так идолжно быть

        except Exception as ex:
            #print(ex)
            #print(str(dt.now()) + " " +"You start second [server]! At the moment only one server can work. " +
            #      "Shutdown this [server]")
            writeLogs(ex, traceback, False)
            time.sleep(3)
        return offset + 1

    def get_jokes(self):
        resp = requests.get(self.api_url)
        joke = resp.json()['attachments'][0]['text']
        #print(joke)
        return joke

    def choose_answer(self, pkg_msg):
        if str(pkg_msg).lower() == cmd_joke:
            result = self.get_jokes()
        elif str(pkg_msg).lower() == cmd_help:
            result = help_text
        elif str(pkg_msg).lower() == cmd_tnx:
            result = tnxu_text
        else:
            result = False
        return result

    def create_buttons(self):
        # update = telegram.Bot(TOKEN)
        #TODO вставить сюда переменные объявленные сверху.
        keyboard = [['/JOKE'], ['/help', 'tnx u!']]
        reply_mark = telegram.replykeyboardmarkup.ReplyKeyboardMarkup(keyboard, True, True)
        # update.send_message(chat_id=update.get_updates()[0].message.chat_id, text="KURVA:", reply_markup=repl_mark)
        return reply_mark

    def user_msg(self, time, usr_id, user, msg):
        tmpl = "{0} {1} {2}".format(usr_id, user, msg)
        chatLogs(tmpl)
        print(str(dt.now())+ " " + tmpl)


def main():
    print("Telegram bot starting:  icanhazdadjoke\nCheck for updates..")
    bot_handler = BotHandler(TOKEN)
    bot_handler.request_to_user()


if __name__ == '__main__':
    main()
