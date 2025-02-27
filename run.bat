@echo off

chcp 65001

setlocal

set "SCRIPT_DIR=%~dp0"

if exist "%SCRIPT_DIR%\.venv\" (
    echo Виртуальное окружение найдено. Переходим к запуску...
) else (
    echo Виртуальное окружение не найдено. Создание виртуального окружения...
    python -m venv .venv
)

echo Обновление библиотек...
%SCRIPT_DIR%\.venv\Scripts\python.exe -m pip install --upgrade -r requirements.txt

echo Запуск скрипта...
%SCRIPT_DIR%\.venv\Scripts\python.exe src\main.py

endlocal

pause