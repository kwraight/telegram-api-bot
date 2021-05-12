# import necessary libraries
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# input our telegram bot unique api token
TOKEN = '1864091493:AAFTRdnZ4tec7TctRwWn176DJ0fMHQ-mft4'

def start(update, context):
    # send a message once the bot is started/start command is ran
    update.message.reply_text('Testing 123')

def hello(update, context):
    # send a message once the command /hello is keyed
    update.message.reply_text('Hello World! \U0001F600')
# for error debugging
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# button display
def question(update, context: CallbackContext)-> None:
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='yes'),
        InlineKeyboardButton("No", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('What\'s the answer?', reply_markup=reply_markup)



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
# error logging
    dp.add_error_handler(error)
# start the bot
    updater.start_polling()
# set the bot to run until you force it to stop
    updater.idle()
if __name__ == '__main__':
    main()
