import json
from pathlib import Path

from PySide6.QtCore import QDir, QObject, Signal
from PySide6.QtGui import QPalette, QColor

from devoud import rpath


class Styles(QObject):
    default_theme = 'night'
    theme_changed = Signal()

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.__themes_dirs = ['browser/styles/default_themes/', f'{window.FS.app_data_dir()}/themes/']
        self.themes = {}
        self.current_theme = self.default_theme
        self.import_themes()

        # Ссылки для ресурсов
        QDir.setSearchPaths('icons', [self.themes[self.current_theme].get('icons', ''), rpath('media/icons')])

    def import_themes(self):
        for themes_path in self.__themes_dirs:
            themes_path = Path(rpath(themes_path))
            for dir_ in themes_path.glob('*'):
                theme_name = dir_.name
                self.themes[theme_name] = {}
                for file in dir_.glob('*'):
                    name = file.name
                    if name == 'palette.json':
                        self.themes[theme_name]['palette'] = get_palette_from_file(str(file))
                    elif name == 'styles.css':
                        self.themes[theme_name]['styles'] = get_style_from_file(str(file))
                    elif name == 'icons':
                        self.themes[theme_name]['icons'] = str(file)

    def set_theme(self, theme: str):
        theme = theme if theme in self.themes else self.default_theme
        self.current_theme = theme
        QDir.setSearchPaths('icons', [self.themes[theme].get('icons', ''), rpath('media/icons')])
        print('[Стили]: Применена тема', theme)
        self.theme_changed.emit()

    def palette(self) -> QPalette:
        return self.themes[self.current_theme].get('palette', QPalette())

    def style(self) -> str:
        return self.themes[self.current_theme].get('styles', '')


def get_palette_from_file(palette_path: str) -> QPalette:
    with open(rpath(palette_path), encoding='utf-8') as palette_file:
        data = json.load(palette_file)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(data['Window']['Active']))
    palette.setColor(QPalette.WindowText, QColor(data['WindowText']['Active']))
    palette.setColor(QPalette.Base, QColor(data['Base']['Active']))
    palette.setColor(QPalette.AlternateBase, QColor(data['AlternateBase']['Active']))
    palette.setColor(QPalette.Button, QColor(data['Button']['Active']))
    palette.setColor(QPalette.ButtonText, QColor(data['ButtonText']['Active']))
    palette.setColor(QPalette.Text, QColor(data['Text']['Active']))
    palette.setColor(QPalette.Light, QColor(data['Light']['Active']))
    palette.setColor(QPalette.Link, QColor(data['Link']['Active']))
    palette.setColor(QPalette.Highlight, QColor(data['Highlight']['Active']))
    palette.setColor(QPalette.PlaceholderText, QColor(data['PlaceholderText']['Active']))
    return palette


def get_style_from_file(style_path: str) -> str:
    with open(rpath(style_path)) as style_file:
        return style_file.read()
