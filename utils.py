import os
from importlib import import_module
from inspect import getmembers, isfunction
from json import load

with open('settings.json', 'r') as settings_file:
    settings = load(settings_file)

src = settings["sources"]

# виды API, предоставляемые модулями
API_types = {'API_functions': isfunction}

# все найденные модули
imported_modules_by_packages = {}

# API объекты, предоставляемые модулями
imported_API_by_modules = {}


def index_functionality():
    """Перечисление реализованных модулей и API, которое они предоставляют."""

    # получение имен подкаталогов каталога src
    packages = next(os.walk(src))[1]

    for pkg in packages:

        # получение имен файлов для данного каталога модулей
        pkg_files = next(os.walk(f'{src}/{pkg}'))[2]

        # каждый пакет должен содержать файл settings.json
        if 'settings.json' not in pkg_files:
            raise Exception(f'Ошибка: пакет {pkg} не содержит файла настроек.')

        # считывание настроек модуля
        with open(f'{src}/{pkg}/settings.json', 'r') as settings_file:
            pkg_settings = load(settings_file)

        # проверка того, что файл настроек имеет тип словаря
        if type(pkg_settings) != dict:
            raise Exception(
                f'Ошибка: неверный формат файла настроек пакета {pkg}')

        # поиск во всех модулях пакета, предоставляющих API
        for module in pkg_settings["API_modules"]:

            imported_modules_by_packages[f'{pkg}'] = {}
            imported_modules_by_packages[f'{pkg}'][f'{module}'] = import_module(
                f'{src}.{pkg}.{module}')
            imported_API_by_modules[imported_modules_by_packages[f'{pkg}'][f'{module}']] = []

            # поиск по типу предоставляемого API
            for API_type in (set(API_types.keys()) & set(pkg_settings.keys())):

                # поиск по всем объектам модуля заданного типа
                members = getmembers(
                    imported_modules_by_packages[f'{pkg}'][f'{module}'], API_types[API_type])

                # поиск объектов API по допустимым названиям для данного типа API
                for member in members:
                    for prefix in pkg_settings[API_type]:

                        if member[0].startswith(prefix):
                            imported_API_by_modules[imported_modules_by_packages[f'{pkg}'][f'{module}']].append(member)
                            break
