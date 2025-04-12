"""
Работа с почтой
"""

import email
import imaplib

from email.header import decode_header
from time import sleep

from loguru import logger

from config import DEFAULT_INBOX
from utils import get_saved_last_email_id, save_last_email_id


def decode_message(message_raw: list) -> dict[str, str]:
    """Декодирует сообщение"""
    msg = email.message_from_bytes(message_raw[0][1])

    msg_date = email.utils.parsedate_tz(msg["Date"])
    msg_from = msg["Return-path"]
    msg_subject = decode_header(msg["Subject"])[0][0].decode()

    for part in msg.walk():
        if part.get_content_type() == "text/html":
            text = part.get_payload(decode=True).decode()

    return {
        "date": msg_date,
        "from": msg_from,
        "subject": msg_subject,
        "text": text,
    }


class Mailer:
    """Класс для работы с почтой"""

    def __init__(self, username: str, password: str, imap_server: str) -> None:
        self._imap_server = imap_server
        self._username = username
        self._password = password
        self._imap = None
        self.is_active = False
        try:
            self.login()
            logger.info("Успешное подключение к imap")
        except Exception as e:
            logger.error("Не удалось подключится к imap: ", e)
            self.stop()
            raise e

    def stop(self):
        """Останавливает бота"""
        self.is_active = False
        self._imap.logout()

    def login(self):
        self._imap = imaplib.IMAP4_SSL(self._imap_server)
        status, _ = self._imap.login(self._username, self._password)
        if status != "OK":
            raise ConnectionError("Не удалось подключиться к imap.")

    def get_last_message(self, mailbox_name: str) -> tuple[str, dict[str, str]] | None:
        """Возвращает последнее сообщение из определённого ящика"""
        status, _ = self._imap.select(mailbox_name, readonly=True)

        if status != "OK" or self._imap.state != "SELECTED":
            logger.error("Не удалось получить последнее сообщение.")
            return

        _, mailbox = self._imap.search(None, "ALL")
        mailbox = mailbox[0].decode("utf-8").split(" ")

        _, msg = self._imap.fetch(mailbox[-1], "(RFC822)")

        return mailbox[-1], decode_message(msg)

    def poll(
        self, delay: int, callback: callable, mailbox_name: str = DEFAULT_INBOX
    ) -> None:
        """Запрашивает сообщения раз в delay"""
        self.is_active = True

        last_msg_id = get_saved_last_email_id()

        logger.debug(
            f"Номер последнего сообщения: {self.get_last_message(mailbox_name)[0]}"
        )

        while self.is_active:
            msgr = self.get_last_message(mailbox_name)
            mid = None
            msg = None

            if msgr is not None:
                mid = msgr[0]
                msg = msgr[1]

            if last_msg_id != mid:
                save_last_email_id(mid)
                last_msg_id = mid
                callback(msg)

            sleep(delay)
