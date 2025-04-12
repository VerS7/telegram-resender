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

Для настройки необходимо заполнить **template.env** и переименовать в **.env** в директории **state**

```python
# Mail
TGRS_PASSWORD = "..."
TGRS_USERNAME = "..."
TGRS_IMAP_SERVER = "..."
TGRS_DEFAULT_INBOX = "INBOX"
TGRS_LISTEN_DELAY = 5  # Задержка на запрос в секундах

# Telegram
TGRS_TOKEN = "..."

```

-   **TGRS_PASSWORD**

    -   Пароль приложения от почтового сервиса (Зачастую пароль пользователя использовать нельзя). Пример с **mail.ru** можно посмотреть **[тут](https://help.mail.ru/mail/mailer/popsmtp/)**.

-   **TGRS_USERNAME**

    -   Адрес электронной почты. Пример: **`example@mail.ru`**.

-   **TGRS_IMAP_SERVER**

    -   **imap**-домен почтового сервиса.

-   **TGRS_DEFAULT_INBOX**

    -   Почтовый ящик, из которого будут тянуться сообщения. По умолчанию **INBOX** - входящие.

-   **TGRS_LISTEN_DELAY**

    -   Задержка запроса последнего сообщения в секундах.

-   **TGRS_TOKEN**

    -   Токен приложения **Telegram**, полученный через **@BotFather**.

## Запуск

### Docker compose

```sh
docker compose up -d
```

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

### Кастомная система запуска

Для запуска используется **py**-скрипт. Устанавливать зависимости не нужно, всё установится само.

Запуск приложения

```sh
python run.py app
```

Обновление приложения с **github**

```sh
python run.py update
```

### Альтернатива кастомной системе через batch | shell скрипты

Windows

Запуск приложения

```sh
run.bat
```

Обновление приложения с **github**

```sh
update.bat
```

Linux

Запуск приложения

```sh
source run.sh
```

Обновление приложения с **github**

```sh
source update.sh
```
