# cross-prom
cross-prom is a service for cross-promotions in telegram. It can collect channels into a list, and output all of them into one message. It has a system of filtering.
IN DEVELOPMENT


## Installation
Install all of the required dependencies for this project by running:  
`pip install -r requirements.txt`


## Deploy your bot
Start a chat with [BotFather](https://t.me/BotFather) in Telegram and get an API token. Once you've done that, input both the API token and your user ID (double check, because the person with this ID will have all administrative privileges) and put them into the `config.py` file.


## Bot commands
This is a list of commands that can be used with the bot
### Default:
`/start` - display helpful message  
`/help` - display link to source code

### User:
`/add @CHANNELNAME - DESCRIPTION` - add a channel

### Administrator
`/list` - display the channel list  
`/clear` - truncate the list  
`/setsize INTEGER` - set the minimum limit for the number of channels  
`/stop` - stop polling the bot
