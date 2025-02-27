"""
Утилитарные функции
"""

import re
import os
from pathlib import Path


def get_saved_chat_id() -> str | None:
    """Возвращает название файла с chat id или None"""
    for filename in os.listdir("./src"):
        file_path = Path(os.path.join("./src", filename))
        if file_path.is_file() and file_path.suffix == ".chatid":
            return file_path.stem


def save_chat_id(chat_id: str) -> None:
    """Сохраняет chat id как файл в текущей директории"""
    for filename in os.listdir("./src"):
        file_path = Path(os.path.join("./src", filename))

        if file_path.is_file() and file_path.suffix == ".chatid":
            os.remove(file_path)

    open(f"./src/{chat_id}.chatid", "w").close()


def parse_message_dates(message) -> tuple[str]:
    """Парсит даты из сообщения"""
    reg_date = re.search(r"Дата регистрации:\s*<b>(.*?)<\/b>", message["text"]).group(1)
    dln_date = re.search(r"Крайний срок:\s*<b>(.*?)<\/b>", message["text"]).group(1)

    return reg_date, dln_date
