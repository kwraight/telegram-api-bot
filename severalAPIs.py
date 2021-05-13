# import necessary libraries
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
### api libraries
import requests

# set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# input our telegram bot unique api token
TOKEN = '1864091493:AAFTRdnZ4tec7TctRwWn176DJ0fMHQ-mft4'

### basic functions
def start(update, context):
    # send a message once the bot is started/start command is ran
    update.message.reply_text('Testing 123')

def hello(update, context):
    # send a message once the command /hello is keyed
    update.message.reply_text('Hello World! \U0001F600')

# for error debugging
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

###

# button display
def question(update, context: CallbackContext)-> None:
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='yes'),
        InlineKeyboardButton("No", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('What\'s the answer?', reply_markup=reply_markup)

# button reply
def question_reply(update, context):
    query = update.callback_query
    if query.data == 'yes':
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text='\U0001F46B\U0001F49D', disable_web_page_preview = 0)
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text='Please try again, we make typing errors sometimes \U0001F624' , disable_web_page_preview = 0)

# motivational quote
def motivate(update, context):
    quote = requests.request(url='https://api.quotable.io/random',method='get')
    update.message.reply_text(quote.json()['content'])

# dog pics
def dog(update, context):
    contents = requests.get('https://random.dog/woof.json').json()
    update.message.reply_text(contents['url'])

# unsplash wallpaper
def wallpaper(update, context):
    url = 'https://api.unsplash.com/photos/random/?client_id=...'
    response = requests.get(url)
    wall_pic = response.json()['urls']['regular']
    update.message.reply_text(wall_pic)

# dima pics
def dima(update, context):
    contents = "teethShut_original.jpeg"
    update.message.reply_photo(photo=open(contents, 'rb'))


# weather
# https://openweathermap.org/api
# api_key = "..."
# base_url = "http://api.openweathermap.org/data/2.5/weather?"
# complete_url = base_url + "appid=" + api_key + "&q=" + "singapore"
# response = requests.get(complete_url)
# x = response.json()
# current_temperature = x['main']['temp']-273.15
# feels_like = x['main']['feels_like']-273.15
# weather_description = x['weather'][0]['description']
# ###
# def weather(update, context):
#     weather_stats = "\U0001F324 Singapore Weather \U0001F327" + "\n\nWeather Description = " + str(weather_description) + \
#       "\nCurrent Temperature (in degree celsius) = " + str(round(current_temperature,1)) + \
#       "\nFeels like (in degree celsius) = " + str(round(feels_like,1))
#     update.message.reply_text(weather_stats)
#
# # business news
# newsapi = NewsApiClient(api_key='...')
# business_news = newsapi.get_top_headlines(category='business', language='en', country='sg', page_size=3)
# ###
# def business(update, context):
#     business1 = list(business_news.values())[2][0]['title'] + '\n\n' + list(business_news.values())[2][0]['url']
#     business2 = list(business_news.values())[2][1]['title'] + '\n\n' + list(business_news.values())[2][1]['url']
#     business3 = list(business_news.values())[2][2]['title'] + '\n\n' + list(business_news.values())[2][2]['url']
#     update.message.reply_text(business1)
#     update.message.reply_text(business2)
#     update.message.reply_text(business3)

def sum(update, context):
    try:
        number1 = int(context.args[0])
        number2 = int(context.args[1])
        result = number1+number2
        update.message.reply_text('The sum is: '+str(result))
    except (IndexError, ValueError):
        update.message.reply_text('There are not enough numbers')

# to start the bot
def main():
    # setup updating together with our telegram api token
    updater = Updater(TOKEN, use_context=True)
# get the dispatcher to register handlers
    dp = updater.dispatcher
# add command handlers for different command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hello", hello))
    dp.add_handler(CommandHandler("question", question))
    dp.add_handler(CallbackQueryHandler(question_reply))
    dp.add_handler(CommandHandler("motivate", motivate))
    dp.add_handler(CommandHandler("dog", dog))
    dp.add_handler(CommandHandler("wallpaper", wallpaper))
    dp.add_handler(CommandHandler("dima", dima))
    dp.add_handler(CommandHandler("sum", sum))
# error logging
    dp.add_error_handler(error)
# start the bot
    updater.start_polling()
# set the bot to run until you force it to stop
    updater.idle()
if __name__ == '__main__':
    main()
