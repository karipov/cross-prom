start_reply = "Hi, send me some channels with the <code>/add</code> command. For example:\n\n<code>/add @techmind - all about tech</code>"
help_reply = """These are the commands you can use:

<code>/start</code> - display start message
<code>/help</code> - display helpful message
<code>/add @channel - description</code> - add a channel
"""

#SERVICE RESPONSES
success_add = "{0} was successfully added to the list!"
trunc_list = "The list has been truncated."
terminate_bot = "Bot has been terminated."
size_set = "Minimum channel size has been set to {0} members."
ban_member = "@{0} has been banned."

#ERRORS
enter_chan = "Please enter a channel."
long_name = "The name is too long."
no_chans = "No channels are available."
admin_only = "This is an admin-only command."
small_chan = "Your channel is too small. The minimum size is {0}."
size_set_error = "Please enter a number after this command."
enter_desc_error = "Please enter a description after this command."
enter_addmessage_error = "Please enter a channel name and description after this command. Click /start for an example."
