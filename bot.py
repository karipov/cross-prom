import telebot
import config
import replies

min_channel_size = 0 # global variable


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

def is_channel(message):
    """Checks if message is a channel name """
    try:
        # because 'message' argument is passed as a string without the @ sign, we
        # add this sign with .format()
        name_or_not = bot.get_chat("@{}".format(message)).type
    except Exception:
        return False

    if name_or_not == "channel":
        return True
    else:
        return False


def channel_is_size(channel):
    """Checks if a channel is of set size (see: /setsize handler)"""
    channel_number = bot.get_chat_members_count(channel)

    if channel_number >= min_channel_size:
        return True
    else:
        return False


@bot.message_handler(commands=['setsize'])
def set_size(message):
    """ Sets minimum size for channels to enter """
    global min_channel_size
    # just to check in if statements
    temp_min_channel_size = ' '.join(message.text.split()[1:])

    if is_admin(message) and temp_min_channel_size:
        min_channel_size = int(temp_min_channel_size)
        bot.reply_to(message, replies.size_set.format(min_channel_size))
    elif not temp_min_channel_size:
        bot.reply_to(message, replies.size_set_error)
    else:
        bot.reply_to(message, replies.admin_only)

@bot.message_handler(commands=['start'])
def send_start(message):
    """ Sends start message"""
    bot.reply_to(message, replies.start_reply, parse_mode='HTML')


@bot.message_handler(commands=['help'])
def send_help(message):
    """ Sends help message """
    bot.reply_to(message, replies.help_reply, parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=['add'])
def start_message(message):
    """ Appends channels to document base.txt """
    message_words = message.text.split()

    channel = ' '.join(message_words[1:2])
    description = ' '.join(message_words[2:])

    # only if messages are not empty and description has a hyphen
    if channel and (description and description[0] == '-'):

        if is_channel(channel) and is_length(description):

            if channel_is_size(channel):
                bot.reply_to(message, replies.success_add.format(channel))
                write_results(' '.join(message_words[1:]))
            else:
                bot.reply_to(message, replies.small_chan.format(min_channel_size))

        else:
            bot.reply_to(message, replies.enter_chan)

    elif not description and channel:
        bot.reply_to(message, replies.enter_desc_error)
    else:
        bot.reply_to(message, replies.enter_addmessage_error) # if empty



@bot.message_handler(commands=['list'])
def show_list(message):
    """ Sends the document base.txt as a telegram message"""

    if is_admin(message):
        with open('base.txt', 'r') as list:
            ready_list = list.read() # save the contents of file in a variable

            if ready_list: # if the text file is not empty...
                bot.reply_to(message, ready_list)
            else:
                bot.reply_to(message, replies.no_chans)

    else:
        bot.reply_to(message, replies.admin_only)


@bot.message_handler(commands=['clear'])
def clear_list(message):
    """ Truncates the document base.txt """

    if is_admin(message):
        with open('base.txt', 'w') as list:
            list.seek(0) # goes to the beginning of the file to truncate it
            list.truncate()
        bot.reply_to(message, replies.trunc_list)
    else:
        bot.reply_to(message, replies.admin_only)


@bot.message_handler(commands=['stop'])
def stop_polling(message):
    """ Stops polling when an admin types /stop """

    if is_admin(message):
        bot.reply_to(message, replies.terminate_bot)
        bot.stop_polling()
    else:
        bot.reply_to(message, replies.admin_only)



bot.polling(none_stop=True, timeout=20)
