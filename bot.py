# -*- coding: utf-8 -*-
import telebot
from telebot import types
import time
import client
import config

bot = telebot.TeleBot(config.token)
show_status = 0


@bot.message_handler(commands=['start', 'help'])
def startup(message):
    bot.send_message(message.chat.id,
                     'Miner\'s Watchbot\n\n'
                     'Miner\'s Watchbot for "EWBF\'s cryptocurrency for CUDA miner" is created to help the miners '
                     'for exercising control over their rigs. The bot interacts with the API of "EWBF\'s '
                     'cryptocurrency for CUDA miner" version 0.3.4 b. It allows in real time to obtain the necessary '
                     'information about the condition of the rig and have feedback in critical situations directly '
                     'in the telegram chat.')

    bot.send_message(message.chat.id,
                     'Warning!\n\n'
                     'Do not rely on a bot to 100%, since it is possible critical situation in which the behavior '
                     'of the bot hasn\'t been tested.\n'
                     'The author disclaims all responsibility for any losses incurred as a result of using this bot. '
                     'Using this bot you agree to the above terms, otherwise, delete the bot.')

    bot.send_message(message.chat.id,
                     'Available commands:\n\n'
                     '/full_check - Get a full report on the current state of the GPU\'s\n'
                     '/quick_shot - Get a quick report on the current state of the GPU\'s\n'
                     '/watchdog - Run monitoring temperature and speed of the GPU\'s\n'
                     '/stopdog - Stop monitoring temperature and speed of the GPU\'s\n')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in [
        '/full_check', '/quick_shot', '/watchdog', '/stopdog']])

    bot.send_message(message.chat.id, 'Choose a command:', reply_markup=keyboard)

    if client.gpu_count(config.host) != config.amount_gpu:
        bot.send_message(message.chat.id,
                         'Warning!\n Identified ' + str(client.gpu_count(config.host)) +
                         ' cards out of ' + str(config.amount_gpu))


@bot.message_handler(commands=['full_check'])
def startup(message):
    for i in range(client.gpu_count(config.host)):
        bot.send_message(message.chat.id, client.complete_report(config.host, i))


@bot.message_handler(commands=['quick_shot'])
def temperature(message):
    bot.send_message(message.chat.id, 'Amount GPU: ' + str(client.gpu_count(config.host)))

    for key, value in config.param_measures.items():
        bot.send_message(message.chat.id, client.quick_report(config.host, key, value, client.gpu_count(config.host)))


@bot.message_handler(func=lambda message: show_status == 1, commands=['watchdog'])
def start_watching(message):
    bot.send_message(message.chat.id, 'Watchdog have been started earlier.')


@bot.message_handler(func=lambda message: show_status == 0, commands=['watchdog'])
def start_watching(message):
    global show_status
    show_status = 1
    count = 0

    bot.send_message(message.chat.id, 'Watchdog is started.')

    while show_status == 1 and count < config.repeat_val:
        time.sleep(config.time_interval)

        if client.watching(config.host, 'temperature', config.param_measures, config.temperature_hi):
            count += 1
            bot.send_message(message.chat.id, client.watching(
                config.host, 'temperature', config.param_measures, config.temperature_hi))

        elif client.watching(config.host, 'speed_sps', config.param_measures, config.speed_lo):
            count += 1
            bot.send_message(message.chat.id, client.watching(
                config.host, 'speed_sps', config.param_measures, config.speed_lo))
        else:
            count = 0

    if show_status == 1 and count >= config.repeat_val:
        show_status = 0
        bot.send_message(message.chat.id,
                         'Limit exceeded warnings!\nWatchdog was stopped. '
                         'Please check your rig and start Watchdog again.')


@bot.message_handler(commands=['stopdog'])
def stop_watching(message):
    global show_status
    if show_status == 1:
        show_status = 0
        bot.send_message(message.chat.id, 'Watchdog was stopped.')
    else:

        bot.send_message(message.chat.id, 'Watchdog hasn\'t been started.')


while True:
    try:
        bot.polling(none_stop=True)

    except Exception:
        print(config.current_time() + ' Polling error occurred!')

        time.sleep(config.time_interval)
