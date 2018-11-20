import configparser
import logging
from typing import List

import pandas as pd
from telegram import Bot, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from src import utils
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
    user_db.create_user(user_id)

    update.message.reply_text(
        questions[0].text,
        reply_markup=make_markup(questions[0])
    )


def on_message(bot: Bot, update: Update):
    global questions

    user_id = get_user_id(update)

    question_id = user_db.get_user(user_id).question_id
    if question_id == len(questions):
        start(bot, update)
        return
    question = questions[question_id]

    answer = update.message.text

    try:
        ind = question.options.index(answer)
        if ind == question.correct:
            user_db.update_points(user_id, 1)
            update.message.reply_text('Верно!')
        else:
            user_db.update_points(user_id, 0)
            update.message.reply_text('Неверно.')
    except ValueError:
        update.message.reply_text('Выберите вариант из предложенных.')
        return

    user_db.next_question(user_id)

    if question_id + 1 == len(questions):
        update.message.reply_text(
            f'Вы набрали {user_db.get_user(user_id).points} балла(ов)!',
            reply_markup=ReplyKeyboardRemove())
        start(bot, update)
        return

    update.message.reply_text(
        questions[question_id + 1].text,
        reply_markup=make_markup(questions[question_id + 1])
    )


def help(bot: Bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot: Bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def init_questions(path: str):
    global questions

    data = pd.read_csv(path, header=None, delimiter='|')
    all_definitions = data[1].tolist()
    for i, row in data.iterrows():
        options = utils.random_definitions(all_definitions, row[1], 4)
        questions.append(Question(row[0], options, options.index(row[1])))


def main():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    api_key = config[config.default_section]['api_key']
    proxy_url = config[config.default_section]['proxy_url']

    global user_db
    user_db = UserInfoDatabase(config['DATABASE']['path'])

    init_questions(config[config.default_section]['questions'])

    updater = Updater(
        api_key,
        request_kwargs={'proxy_url': proxy_url}
    )

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('new_game', new_game))
    updater.dispatcher.add_handler(CommandHandler('help', help))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, on_message))

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
