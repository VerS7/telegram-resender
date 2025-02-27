#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

VENV_DIR="$SCRIPT_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
    echo "Виртуальное окружение найдено. Переходим к запуску..."
else
    echo "Виртуальное окружение не найдено. Создание виртуального окружения..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "Обновление библиотек..."
pip install --upgrade -r "$SCRIPT_DIR/requirements.txt"

echo "Запуск скрипта..."
python "$SCRIPT_DIR/src/main.py"

deactivate