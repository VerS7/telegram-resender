#!/bin/python


import subprocess
import platform
import zipfile
import shutil
import sys
import os

from urllib import request
from os import path


venv = path.join(path.dirname(__name__), ".venv")
venv_python = path.join(
    venv, "Scripts/python.exe" if platform.system() == "Windows" else "bin/python"
)


def run():
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

    input("Нажмите Enter чтобы закрыть это окно.")


def update():
    def ignore_file(_, files):
        return ["config.py"] if "config.py" in files else []

    archive = "update.zip"
    extracted = "telegram-resender-master"

    print("Обновление...")
    print("Загружаем с github...")
    request.urlretrieve(
        "https://github.com/VerS7/telegram-resender/archive/refs/heads/master.zip",
        archive,
    )

    print("Распаковываем архив...")
    with zipfile.ZipFile(archive, "r") as zfile:
        zfile.extractall(path.dirname(__name__))

    print("Заменяем...")
    shutil.copytree(
        path.join(extracted, "src"), "src", dirs_exist_ok=True, ignore=ignore_file
    )
    shutil.copy(path.join(extracted, "requirements.txt"), "requirements.txt")

    print("Удаляем лишнее...")
    shutil.rmtree(extracted)
    os.remove(archive)

    print("Готово!")
    input("Нажмите Enter чтобы закрыть это окно.")


if __name__ == "__main__":
    mode = sys.argv[1]

    match mode:
        case "app":
            run()
        case "update":
            update()
        case _:
            print("Неизвестная команда: ", mode)
            input("Нажмите Enter чтобы закрыть это окно.")
