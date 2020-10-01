import json
import urllib.request as request
from random import choice

from decouple import config as dconfig
from mongoengine import connect
from telegram import Update, BotCommand
from telegram.ext import CallbackContext, CommandHandler

from telebot import updater, config, log, dispatcher
# default reply strings
from telebot.db import get_words_for_user, clear_words_for_user, add_word_for_user

# curl --data "entry.360220839=aa&entry.2084162701=bb&entry.2023085564=cc&entry.1938153099=dd" {os.environ['FORM_URL]}
# mimic above in py to send formdata aa,bb,cc,dd to form db of form

START_TEXT = f"""
Hi there!
I'm `{updater.bot.first_name}`, a bot to handle your GRE words.
"""

HELP_TEXT = (
    START_TEXT
    + """
Use following commands to use me (*blush*):
- /random - Get a random word from your list
- /start - Turn me on
"""
)


def start(update: Update, context: CallbackContext):
    # start message
    log(update, func_name="start")
    update.message.reply_markdown(START_TEXT)


def help(update: Update, context: CallbackContext):
    # display help message
    log(update, func_name="help")

    text_blob = "Nou"
    update.message.reply_markdown(text_blob)


def clear(update: Update, context: CallbackContext):
    # clear cache
    log(update, func_name="clear")
    clear_words_for_user(update.effective_user.id)
    text_blob = f"""_Cleared cache_"""
    update.message.reply_markdown(text_blob)


def random(update: Update, context: CallbackContext):
    # get a word from your Sheets
    log(update, func_name="random")

    with request.urlopen(dconfig("SPREADSHEET_URL")) as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source)

            word_cache = get_words_for_user(update.effective_user.id)

            if len(word_cache) == len(data['values']):
                clear_words_for_user(update.effective_user.id)

            while True:
                chosen = choice(range(len(data['values'])))
                if data['values'][chosen][0] not in word_cache:
                    MESSAGE = f"""
*{data['values'][chosen][0]}*                  _{data['values'][chosen][2]}_
------------------------------------------------
`{data['values'][chosen][1]}`   

{data['values'][chosen][3]}

Hint=_{data['values'][chosen][4] if len(data['values'][chosen])==5 else ""}_
            
            """
                    if len(word_cache) == 0:
                        update.message.reply_markdown(f"[None in cache]")
                    else:
                        update.message.reply_markdown(f"_{word_cache}_")

                    update.message.reply_markdown(MESSAGE)
                    add_word_for_user(update.effective_user.id, data['values'][chosen][0])
                    break
                else:
                    continue
        else:
            MESSAGE = f"""Sheets API high or something..idk"""
            update.message.reply_markdown(MESSAGE)


def allWords(update: Update, context: CallbackContext):
    # get all words from Sheets
    log(update, func_name="all")
    with request.urlopen(dconfig('SPREADSHEET_URL')) as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source)
            for i in range(1, len(data['values'])):

                MESSAGE = f"""
{i}) *{data['values'][i][0]}*                  _{data['values'][i][2]}_
------------------------------------------------
`{data['values'][i][1]}`   

{data['values'][i][3]}

Hint=_{data['values'][i][4] if len(data['values'][i])==5 else ""}_
            
            """
                update.message.reply_markdown(MESSAGE)
        else:
            MESSAGE = f"""Sheets API high or something..idk"""
            update.message.reply_markdown(MESSAGE)


def search(update: Update, context: CallbackContext):
    # get substring matches from word / meaning field
    log(update, func_name="search")
    with request.urlopen(dconfig('SPREADSHEET_URL')) as response:
        if response.getcode() == 200:
            if context.args:
                count = 0
                source = response.read()
                data = json.loads(source)
                for i in range(1, len(data['values'])):
                    if (
                        data['values'][i][0].find(context.args[0]) != -1
                        or data['values'][i][1].find(context.args[0]) != -1
                    ):
                        MESSAGE = f"""
{i}) *{data['values'][i][0]}*                  _{data['values'][i][2]}_
------------------------------------------------
`{data['values'][i][1]}`   

{data['values'][i][3]}

Hint=_{data['values'][i][4] if len(data['values'][i])==5 else ""}_
            
                        """
                        count = count + 1
                        update.message.reply_markdown(MESSAGE)

                if count == 0:
                    MESSAGE = f"""_Could not find requested word_"""
                    update.message.reply_markdown(MESSAGE)
                else:
                    MESSAGE = f"""_{count} matches found_"""
                    update.message.reply_markdown(MESSAGE)
            else:
                MESSAGE = f"""Uhhh.... I could search, but what?"""
                update.message.reply_markdown(MESSAGE)
        else:
            MESSAGE = f"""Sheets API high or something..idk"""
            update.message.reply_markdown(MESSAGE)


# set bot commands
COMMANDS = [
    BotCommand(command='help', description="Display the help text to understand how to use this bot"),
    BotCommand(command='random', description="Get a random word"),
    BotCommand(command='all', description="Get all words in order"),
    BotCommand(command='search', description="Gets words with this substring in word or meaning fields."),
    BotCommand(command='clear', description="Clears word cache"),
]

if __name__ == "__main__":
    # create handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("random", random))
    dispatcher.add_handler(CommandHandler("all", allWords))
    dispatcher.add_handler(CommandHandler("search", search))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("clear", clear))

    if config.DB_NAME:
        connect(config.DB_NAME, 'default', host=config.DB_URI)

    updater.bot.set_my_commands(COMMANDS)

    updater.start_polling()

    print("WordBot thot")
    updater.idle()
