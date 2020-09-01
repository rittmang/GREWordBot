from decouple import config
from telegram import Update
from telegram.ext import Updater


# class for configuration of a bot
class Config:
    def __init__(self, token, db_uri, webhook_url, port=False, load=None, no_load=None):
        """
        Initialize bot config values
        :param token: telegram bot token that you get from botfather
        :param db_uri: URI connection string to the database
        :param webhook_url:
        :param port:
        :param load:
        :param no_load:
        """

        self.TOKEN = token
        self.DB_URI = db_uri
        self.WEBHOOK_URL = webhook_url
        self.PORT = port

        self.LOAD = load
        self.NO_LOAD = no_load


def log(update: Update, func_name: str, extra_text: str = ""):
    """
    Function to log bot activity
    :param update: Update object to retrieve info from
    :param func_name: name of the function being called
    :param extra_text: any extra text to be logged
    :return: None
    """
    chat = "private chat"
    if update.effective_chat.type != "private":
        chat = update.effective_chat.title

    print(update.effective_user.username, "called function", func_name, "from", chat)
    if extra_text:
        print(extra_text)


# create config object
config = Config(
    token=config('TOKEN'),
    db_uri=config('DATABASE_URL', default=False),
    webhook_url=config('WEBHOOK_URL', default=False),
    port=config('PORT', default=False),
    load=config('LOAD', default=False, cast=lambda x: x.split(" ") if x else False),
    no_load=config('NO_LOAD', default=False, cast=lambda x: x.split(" ") if x else False),
)

# create updater and dispatcher
updater = Updater(config.TOKEN, use_context=True)
dispatcher = updater.dispatcher
