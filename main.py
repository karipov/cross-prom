from os import environ
import telebot
from flask import Flask, request
import config
import replies

bot = telebot.TeleBot(config.TOKEN)
server = Flask(__name__)

min_channel_size = 0 # global variabl

@server.route('/' + config.TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='NAME OF HEROKU APP' + config.TOKEN)
    return "!", 200





def write_results(channel):
    """ Writes channel names to a file """
    with open('base.txt', 'a') as list:
        list.write("{} \n".format(channel))

def is_admin(message):
    """ Checks if a user is within the list of admins (i.e. my id) """

    if (message.from_user.id in config.CHAT_ID) or (message.chat.id in config.CHAT_ID):
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


def gen_response(channel, description, message_words):
    if not channel:
        return replies.enter_addmessage_error

    if not description:
        return replies.enter_desc_error

    if description[0] != '-':
        return replies.enter_addmessage_error

    if not (is_channel(channel) and is_length(description)):
        return replies.enter_chan

    if not channel_is_size(channel):
        return replies.small_chan.format(min_channel_size)

    write_results(' '.join(message_words[1:]))
    return replies.success_add.format(channel)



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
    bot.reply_to(message, replies.help_reply, parse_mode='HTML')


@bot.message_handler(commands=['add'])
def start_message(message):
    """ Appends channels to document base.txt """
    message_words = message.text.split()

    channel = ' '.join(message_words[1:2])
    description = ' '.join(message_words[2:])

    bot.reply_to(message, gen_response(channel, description, message_words))



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


# @bot.message_handler(commands=['ban'])
# def ban_user(message):
#     """ Bans users """
#
#     user_id = message.reply_to_message.from_user.id
#     username = message.reply_to_message.from_user.username
#
#     if is_admin(message):
#         bot.kick_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, until_date=1)
#         bot.reply_to(message, replies.ban_member.format(username))
#     else:
#         bot.reply_to(replies.admin_only)



if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))
