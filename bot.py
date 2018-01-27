import telebot
import config


bot = telebot.TeleBot(token=config.token)

def write_results(channel):
    with open('base.txt', 'a') as list:
        list.write("{} \n".format(channel))


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, 'Hi, send me some channels with the /add command')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Check me out, I'm open-source")

@bot.message_handler(commands=['add'])
def start_message(message):
    channel = ' '.join(message.text.split()[1:])
    bot.reply_to(message, '{} was successfully added to the list!'.format(channel))
    write_results(channel)

@bot.message_handler(commands=['list'])
def show_list(message):
    if message.from_user.id == config.CHAT_ID or message.chat.id == config.CHAT_ID:
        with open('base.txt', 'r') as list:
            crossmega = list.read()
            if crossmega:
                bot.reply_to(message, crossmega)
            else:
                bot.reply_to(message, 'No channels are available')
    else:
        bot.reply_to(message, 'This is an admin only command')

@bot.message_handler(commands=['clear'])
def clear_list(message):
    with open('base.txt', 'w') as list:
        list.seek(0)
        list.truncate()
    bot.reply_to(message, 'The list has been truncated')

bot.polling()
