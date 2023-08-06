<h1 align="center">Devoud</h1>

![Скриншот](./screenshot.png)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)
![Arch](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=fff&style=for-the-badge)
![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Fedora](https://img.shields.io/badge/Fedora-294172?style=for-the-badge&logo=fedora&logoColor=white)
## О проекте 🎧
Данный проект является полностью открытым и свободнораспространяемым браузером, который каждый может перестроить по своему усмотрению. В разработке применяется новейший PySide6 с веб-движком QtWebEngine. Проект будет стремиться к простоте использования и разработке некоторых решений. Не требует повышенных прав для установки.
## Установка браузера 💿
### Системные требования
* ОС: Windows 10 и выше, GNU/Linux;
* [Python](https://www.python.org/): версии 3.8 и выше, а также пакетный менеджер <u>pip</u> (в Windows идет вместе с Python, но во время установки Python поставьте галочку "Add Python 3.x to PATH");
* Видеокарта: любая с поддержкой OpenGL
### Установка через pip (рекомендуется)
* Введите команду ```pip install devoud``` в терминале (cmd, powershell, bash) 
* После окончания установки, запустите его через команду ```devoud``` в терминале, он произведет начальную настройку, и создаст ярлык запуска в системе. В дальнейшем его можно будет запускать через ярлык.
### Запуск из исходников (другой способ установки)
* Скачайте архив с этой страницы
* Распакуйте в любом месте
* Перейдите в данный каталог
* Установите зависимости из pyproject.toml командой ```pip install -e .```
* Запустите браузер через start.py
## Обновление 🔧
* Для обновления программы используйте команду ```pip install devoud --upgrade```
## Для разработчиков
### Сборка пакета через [поэзию](https://python-poetry.org/) 📜
* ```poetry build```
### Сборка в исполняемый файл (.exe и тд)
* ```pyinstaller ./misc/devoud.spec```
## Вопросы ❓
* О всех найденных ошибках и предложениях по улучшению программы сообщайте во вкладке [Задачи](https://codeberg.org/OneEyedDancer/Devoud/issues) или пишите мне на почту [ooeyd@ya.ru](ooeyd@ya.ru)
* Случайно удалили ярлык? Нажмите на кнопку "Создать ярлык" на странице настроек или выполните команду ```devoud --shortcut```
* Все доступные команды для браузера можно узнать через ```devoud --help```
* Будут ли доступны расширения из других браузеров? Пока что маловероятно
* Как помочь проекту? Вы можете предложить свой вариант решение какой-либо проблемы через [Задачи](https://codeberg.org/OneEyedDancer/Devoud/issues)
* Могу ли я модифицировать эту программу и выпускать под своим названием? Да, можно, но с соблюдением требований лицензии
* Передаются ли мои данные? Автор гарантирует, что с его стороны все ваши данные хранятся только на вашем компьютере. Но помните, что мы живем в проклятом мире, а этот браузер основывается на двжике QtWebEngine, а значит этим могут заниматься Qt и Google 
## Лицензия 🄯
[![GPLv3](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)](https://www.gnu.org/licenses/gpl-3.0)
