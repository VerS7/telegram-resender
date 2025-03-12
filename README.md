# Email -> Telegram Resender

Бот для отправки кастомных заявок из почты в **ТГ**.

Пример приходящего сообщения:

> **Новое сообщение**
>
> Тема: **Направлен запрос на обслуживание № `IM12345678`**
>
> От: `noreply@example.ru`
>
> Дата регистрации: **12/12/25 16:30:00**
>
> Крайний срок: **13/12/25 16:30:00**

## Настройка

Для настройки необходимо заполнить **src/config.py**

```python
# Mail
PASSWORD = "..."
USERNAME = "..."
IMAP_SERVER = "..."
DEFAULT_INBOX = "INBOX"
LISTEN_DELAY = 5  # Задержка на запрос в секундах

# Telegram
TELEGRAM_TOKEN = "..."
```

-   **PASSWORD**

    -   Пароль приложения от почтового сервиса (Зачастую пароль пользователя использовать нельзя). Пример с **mail.ru** можно посмотреть **[тут](https://help.mail.ru/mail/mailer/popsmtp/)**.

-   **USERNAME**

    -   Адрес электронной почты. Пример: **`example@mail.ru`**.

-   **IMAP_SERVER**

    -   **imap**-домен почтового сервиса.

-   **DEFAULT_INBOX**

    -   Почтовый ящик, из которого будут тянуться сообщения. По умолчанию **INBOX** - входящие.

-   **LISTEN_DELAY**

    -   Задержка запроса последнего сообщения в секундах.

-   **TELEGRAM_TOKEN**

    -   Токен приложения **Telegram**, полученный через **@BotFather**.

## Запуск

Есть несколько способов запуска

### Only Python

Для запуска используется только системный **python**

```sh
pip install -r requirements.txt
```

Windows

```sh
.venv/Scripts/python.exe src/main.py
```

Linux

```sh
.venv/bin/python src/main.py
```

### run.sh | run.bat

Для запуска используется скрипт

Windows

```sh
run.bat
```

Linux

```sh
source run.sh
```

### Кастомная система запуска

Для запуска используется **py**-скрипт. Устанавливать зависимости не нужно, всё установится само.

```sh
python run.py
```

### Альтернатива кастомной системе через batch | shell скрипты

Windows

```sh
run-py.bat
```

Linux

```sh
source run-py.sh
```
