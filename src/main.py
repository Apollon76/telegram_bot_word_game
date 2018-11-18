import configparser
import logging
from typing import List

from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from src.question import Question
from src.user_info_db import UserInfoDatabase

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


questions: List[Question] = []
user_db: UserInfoDatabase = None


def start(bot: Bot, update: Update):
    update.message.reply_text('Добро пожаловать! Введите /new_game чтобы начать игру.')


def get_user_id(update: Update) -> int:
    return update.message.chat.id


def make_markup(question: Question) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([question.options])


def new_game(bot: Bot, update: Update):
    user_id = get_user_id(update)
    user_db.update_user(user_id)

    update.message.reply_text(
        questions[0].text,
        reply_markup=make_markup(questions[0])
    )


def on_message(bot: Bot, update: Update):
    global questions

    user_id = get_user_id(update)
    question_id = user_db.get(user_id)
    question = questions[question_id]

    answer = update.message.text

    try:
        ind = question.options.index(answer)
        if ind == question.correct:
            update.message.reply_text('Верно!')
        else:
            update.message.reply_text('Неверно.')
    except ValueError:
        update.message.reply_text('Выберите вариант из предложенных.')


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

    global user_db
    user_db = UserInfoDatabase('../users.db')

    global questions
    questions = [
        Question('Hueschion', ['hui', 'Djigurda'], 0)
    ]

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
