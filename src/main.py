"""
Telegram bot
"""

from threading import Thread

import telebot
from telebot.types import Message

from config import TELEGRAM_TOKEN, USERNAME, PASSWORD, IMAP_SERVER, LISTEN_DELAY
from mail import Mailer
from utils import get_saved_chat_id, save_chat_id, parse_message_dates


bot = telebot.TeleBot(TELEGRAM_TOKEN)
mailer = Mailer(USERNAME, PASSWORD, IMAP_SERVER)


def send_message_callback(bot: telebot.TeleBot, msg: dict[str, str]) -> None:
    try:
        rd, dd = parse_message_dates(msg)
    except Exception as e:
        print(e)
        return

    bot.send_message(
        get_saved_chat_id(),
        f"Новое сообщение\n\nТема: {msg['subject']}\nОт: {msg['from']}\n\nДата регистрации: {rd}\nКрайний срок: {dd}",
    )


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
        return

    bot.send_message(message.chat.id, "Чат уже подключён.")


if __name__ == "__main__":
    bot_thread = Thread(target=lambda: bot.polling(non_stop=True, interval=0))
    mailer_thread = Thread(
        target=lambda: mailer.poll(
            LISTEN_DELAY, lambda msg: send_message_callback(bot, msg)
        )
    )

    bot_thread.start()
    mailer_thread.start()

    bot_thread.join()
    mailer_thread.join()
