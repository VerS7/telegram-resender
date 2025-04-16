"""
Утилитарные функции
"""

import re
import os
from pathlib import Path

from config import STATE_PATH


def _get_state_from_fs(suffix: str) -> str | None:
    for filename in os.listdir(STATE_PATH):
        file_path = Path(os.path.join(STATE_PATH, filename))
        if file_path.is_file() and file_path.suffix == suffix:
            return file_path.stem


def _save_state_to_fs(state: str, suffix: str) -> None:
    for filename in os.listdir(STATE_PATH):
        file_path = Path(os.path.join(STATE_PATH, filename))

        if file_path.is_file() and file_path.suffix == suffix:
            os.remove(file_path)

    open(os.path.join(STATE_PATH, f"{state}{suffix}"), "w").close()


def get_saved_chat_id() -> str | None:
    """Возвращает название файла с chat id или None"""
    return _get_state_from_fs(".chatid")


def save_chat_id(chat_id: str) -> None:
    """Сохраняет chat id как файл в текущей директории"""
    _saved_chat_id = get_saved_chat_id()
    if _saved_chat_id is not None:
        os.remove(os.path.join(STATE_PATH, _saved_chat_id + ".chatid"))

    _save_state_to_fs(chat_id, ".chatid")


def get_saved_last_email_id() -> str | None:
    """Возвращает название файла с id последнего email или None"""
    return _get_state_from_fs(".emailid")


def save_last_email_id(email_id: str) -> None:
    """Сохраняет id последнего email как файл в текущей директории"""
    _saved_email_id = get_saved_last_email_id()
    if _saved_email_id is not None:
        os.remove(os.path.join(STATE_PATH, _saved_email_id + ".emailid"))

    _save_state_to_fs(email_id, ".emailid")


def parse_message_regdate(message: str) -> str:
    """Парсит дату регистрации из сообщения"""
    reg_str = re.search(
        r"<(BR|br)>Дата регистрации:\s*(<([bB]|strong)>)?(.*?)(<\/([bB]|strong)>)?<(BR|br)>",
        message["text"],
    ).group()

    return re.search(r"(\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})", reg_str).group()


def parse_message_deadline(message: str) -> str:
    """Парсит дедлайн из сообщения"""
    dln_str = re.search(
        r"<(BR|br)?>Крайний срок:\s*(<([bB]|strong)>)?(.*?)(<\/([bB]|strong)>)?<(BR|br)?>",
        message["text"],
    ).group()

    return re.search(r"(\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})", dln_str).group()


def parse_message_description(message: str) -> str:
    """Парсит краткое описание из сообщения"""
    raise NotImplementedError()


def parse_message_dates(message: str) -> tuple[str]:
    """Парсит даты из сообщения"""
    return parse_message_regdate(message), parse_message_deadline(message)


def parse_id(message: str) -> str:
    """Парсит ID обращения из сообщения"""
    id = re.search(r"(№)?\s*([A-Za-z]+\d+)", message["subject"])

    return id.group().strip().replace("№", "")
