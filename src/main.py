"""
Telegram bot
"""

from threading import Thread

import telebot
from telebot.types import Message

from loguru import logger

from config import TELEGRAM_TOKEN, USERNAME, PASSWORD, IMAP_SERVER, LISTEN_DELAY
from mail import Mailer
from utils import get_saved_chat_id, save_chat_id, parse_message_dates, parse_id


bot = telebot.TeleBot(TELEGRAM_TOKEN)
mailer = Mailer(USERNAME, PASSWORD, IMAP_SERVER)


def send_message_callback(bot: telebot.TeleBot, msg: dict[str, str]) -> None:
    try:
        id = parse_id(msg)
    except Exception as e:
        logger.error("Ошибка при парсинге ID обращения: ", e)

    try:
        rd, dd = parse_message_dates(msg)
    except Exception as e:
        logger.error("Ошибка при парсинге сроков: ", e)

    chat_id = get_saved_chat_id()
    if chat_id is None:
        return

    message = (
        f"**Новое сообщение**\n\nТема: **{msg['subject'].replace(id, f'`{id}`')}**\n\nДата регистрации: **{rd}**\nКрайний срок: **{dd}**"
        if (rd is not None and dd is not None)
        else f"**Новое сообщение**\n\nТема: **{msg['subject'].replace(id, f'`{id}`')}**"
    )

    bot.send_message(
        chat_id,
        message,
        parse_mode="Markdown",
    )
    logger.info("Отправлено оповещение.")


@bot.message_handler(commands=["help"])
def help(message: Message):
    bot.send_message(
        message.chat.id, "Для подключения бота к этому чату пропишите /connect"
    )


@bot.message_handler(commands=["connect"])
def connect(message: Message):
    chat_id = get_saved_chat_id()
    if chat_id is None:
        save_chat_id(message.chat.id)
        bot.send_message(message.chat.id, f"Чат с ID: {message.chat.id} подключён!")
        logger.info("Подключён чат с ID: ", message.chat.id)
        return

    bot.send_message(message.chat.id, "Чат уже подключён.")
    logger.warning("Попытка подключения чата: ", message.chat.id)


if __name__ == "__main__":
    bot_thread = Thread(target=lambda: bot.polling(non_stop=True, interval=0))
    mailer_thread = Thread(
        target=lambda: mailer.poll(
            LISTEN_DELAY, lambda msg: send_message_callback(bot, msg)
        )
    )

    logger.info("Запуск...")

    bot_thread.start()
    mailer_thread.start()

    bot_thread.join()
    mailer_thread.join()
