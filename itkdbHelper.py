# import necessary libraries
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
### api libraries
import requests
import json
###
import itkdb
import itkdb.exceptions as itkX
import myDetails

#####################
### itkdb
#####################
def AuthenticateUser(ac1,ac2):
    user = itkdb.core.User(accessCode1=ac1, accessCode2=ac2)
    user.authenticate()
    client = itkdb.Client(user=user)
    return client

def DbGet(client, myAction, inData, listFlag=False):
    outData=None
    if listFlag:
        try:
            outData = list(client.get(myAction, json=inData ) )
        except itkX.BadRequest as b: # catch double registrations
            return str(myAction+": went wrong for "+str(inData)+'\n**'+str(b)[str(b).find('"message": ')+len('"message": '):str(b).find('"paramMap"')-8]+'**') # sucks
    else:
        try:
            outData = client.get(myAction, json=inData)
        except itkX.BadRequest as b: # catch double registrations
            return str(myAction+": went wrong for "+str(inData)+'\n**'+str(b)[str(b).find('"message": ')+len('"message": '):str(b).find('"paramMap"')-8]+'**') # sucks
    return outData

# set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# input our telegram bot unique api token
myDeets=myDetails.SetITk()
botDeets=myDetails.SetItkdbApiBot()
TOKEN = botDeets.ac1

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

### Easter egg
# dima pic
def dima(update, context):
    contents = "teethShut_original.jpeg"
    update.message.reply_photo(photo=open(contents, 'rb'))

### useful part
def helpMsg():
    msg = "use '^' to mark command\n"
    msg += "use '>' to mark filter keyword:value pair\n"
    msg += "use '&' to mark filter keyword\n"
    msg += "example:\n"
    msg += "/itkdb ^getComponent >component:20USBSS0000070 &alternativeIdentifier"
    return msg

def help(update, context):
    update.message.reply_text('Help info:\n'+helpMsg())

def GetDict(argArr):
    argDict={}
    for x in [a[1::] for a in argArr if ">" in a]:
        if len(x.split(':'))!=2:
            continue
        argDict[x.split(':')[0]]=x.split(':')[1]
    return argDict

def itkdbHelp(update, context):
    if "help" in context.args:
        update.message.reply_text('Help info:\n'+helpMsg())
        return 0
    command = [a[1::] for a in context.args if "^" in a]
    filtDict = GetDict(list(context.args))
    dictKey = [a[1::] for a in context.args if "&" in a]
    if len(command)!=1 or len(dictKey)!=1 or len(filtDict)<1:
        update.message.reply_text('Problem with format:\n'+helpMsg())
        return 0
    # else:
    #     print("### inputs")
    #     print(command)
    #     print(filtDict)
    #     print(dictKey)
    try:
        client=AuthenticateUser(myDeets.ac1,myDeets.ac2)
    except:
        update.message.reply_text('authentication issue')
    try:
        val=DbGet(client,command[0],filtDict)[dictKey[0]]
        if type(val) == type({}):
            update.message.reply_text('returned:\n'+json.dumps(val))
        else:
            update.message.reply_text('returned:\n'+str(val))
    except KeyError:
        update.message.reply_text('no matching key')
    except:
        update.message.reply_text('DbGet issue (maybe too long)')

# to start the bot
def main():
    # setup updating together with our telegram api token
    updater = Updater(TOKEN, use_context=True)
# get the dispatcher to register handlers
    dp = updater.dispatcher
# add command handlers for different command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hello", hello))
    dp.add_handler(CommandHandler("dima", dima))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("itkdb", itkdbHelp))
# error logging
    dp.add_error_handler(error)
# start the bot
    updater.start_polling()
# set the bot to run until you force it to stop
    updater.idle()
if __name__ == '__main__':
    main()
