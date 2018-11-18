import configparser
import logging

from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot: Bot, update: Update):
    update.message.reply_text('Добро пожаловать! Введите /new_game чтобы начать игру.')


def new_game(bot: Bot, update: Update):
    update.message.reply_text('Please choose:', reply_markup=ReplyKeyboardMarkup([['asdf']]))


def on_message(bot: Bot, update: Update):
    update.message.reply_text('Верно')


def help(bot: Bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot: Bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    api_key = config[config.default_section]['api_key']
    proxy_url = config[config.default_section]['proxy_url']

    updater = Updater(api_key,
                      request_kwargs={'proxy_url': proxy_url})

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('new_game', new_game))
    updater.dispatcher.add_handler(CommandHandler('help', help))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, on_message))

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
