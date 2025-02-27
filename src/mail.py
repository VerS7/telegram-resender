"""
Работа с почтой
"""

import email
import imaplib

from email.header import decode_header
from time import sleep


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
        self._imap = imaplib.IMAP4_SSL(imap_server)
        try:
            self._imap.login(username, password)
        except Exception as e:
            raise e

    def get_last_message(self, mailbox_name: str) -> tuple[str, dict[str, str]] | None:
        """Возвращает последнее сообщение из определённого ящика"""
        self._imap.select(mailbox_name)

        if self._imap.state != "SELECTED":
            return

        _, mailbox = self._imap.search(None, "ALL")
        mailbox = mailbox[0].decode("utf-8").split(" ")

        _, msg = self._imap.fetch(mailbox[-1], "(RFC822)")

        return mailbox[-1], decode_message(msg)

    def poll(self, delay: int, callback, mailbox_name: str = "info") -> None:
        """Запрашивает сообщения раз в delay"""
        last_msg_id = 0

        while True:
            msgr = self.get_last_message(mailbox_name)
            mid = None
            msg = None

            if msgr is not None:
                mid = msgr[0]
                msg = msgr[1]

            if last_msg_id != mid:
                last_msg_id = mid
                callback(msg)

            sleep(delay)
