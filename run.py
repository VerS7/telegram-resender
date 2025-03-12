#!/bin/python

import subprocess
import platform
import sys

from os import path


venv = path.join(path.dirname(__name__), ".venv")
venv_python = path.join(
    venv, "Scripts/python.exe" if platform.system() == "Windows" else "bin/python"
)


if not path.isdir(venv):
    print("Виртуальное окружение не найдено. Создание виртуального окружения...")
    subprocess.check_call([sys.executable, "-m", "venv", venv])
else:
    print("Виртуальное окружение найдено. Переходим к запуску...")

subprocess.check_call(
    [
        venv_python,
        "-m",
        "pip",
        "install",
        "-r",
        path.join(path.dirname(__name__), "requirements.txt"),
    ]
)

sys.stdout.write("\033c")

print(subprocess.check_call([venv_python, "src/main.py"]))
