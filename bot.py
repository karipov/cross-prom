import telebot
import config


bot = telebot.TeleBot(token=config.token) # initialize bot

def write_results(channel):
    """ Writes channel names to a file """
    with open('base.txt', 'a') as list:
        list.write("{} \n".format(channel))

def is_admin(message):
    """ Checks if a user is within the list of admins (i.e. my id) """
    if message.from_user.id == config.CHAT_ID or message.chat.id == config.CHAT_ID:
        return True
    else:
        return False

def is_length(message):
    """ Checks if message is of set length """
    if len(message) <= 25:
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def send_start(message):
    """ Sends start message"""
    bot.reply_to(message, 'Hi, send me some channels with the <code>/add</code> command. For \
example:\n\n<code>/add @techmind</code>', parse_mode='HTML')

@bot.message_handler(commands=['help'])
def send_help(message):
    """ Sends help message """
    bot.reply_to(message, "Check me out; I'm \
<a href='https://github.com/karipov/cross-prom'>open-source</a>.", parse_mode='HTML', disable_web_page_preview=True)

@bot.message_handler(commands=['add'])
def start_message(message):
    """ Appends channels to document base.txt """
    channel = ' '.join(message.text.split()[1:])

    if is_length(channel) and channel: # only if message is of certain length and not empty
        bot.reply_to(message, '{} was successfully added to the list!'.format(channel))
        write_results(channel)
    elif not channel: # if empty
        bot.reply_to(message, 'Please enter a channel')
    else:
        bot.reply_to(message, 'The name is too long :(')

@bot.message_handler(commands=['list'])
def show_list(message):
    """ Sends the document base.txt as a telegram message"""

    if is_admin(message):
        with open('base.txt', 'r') as list:
            ready_list = list.read() # save the contents of file in a variable

            if ready_list: # if the text file is not empty...
                bot.reply_to(message, ready_list)
            else:
                bot.reply_to(message, 'No channels are available')

    else:
        bot.reply_to(message, 'This is an admin-only command')

@bot.message_handler(commands=['clear'])
def clear_list(message):
    """ Truncates the document base.txt """

    with open('base.txt', 'w') as list:
        list.seek(0) # goes to the beginning of the file to truncate it
        list.truncate()
    bot.reply_to(message, 'The list has been truncated')

@bot.message_handler(commands=['stop'])
def stop_polling(message):
    """ Stops polling when an admin types /stop """

    if is_admin:
        bot.reply_to(message, 'Bot has been terminated')
        bot.stop_polling()
    else:
        bot.reply_to(message, "This is an admin-only command")
bot.polling(none_stop=True, timeout=20)
