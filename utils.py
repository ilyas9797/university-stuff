import os
from importlib import import_module
from inspect import (formatargspec, getfullargspec, getmembers, isclass,
                     isfunction)
from json import load
from types import ModuleType
from typing import Any, Callable, Dict, List, Tuple, cast


class APIClass:
    classname: str
    class_obj: type
    methods: List[Tuple[str, Callable]] = []


class ImportedPkgAPI:
    pkgname: str
    settings: dict
    module_obj: ModuleType
    classes: List[APIClass] = []


# API классы, предоставляемые пакетами
# список кортежей вида
# (
#   полное имя API-модуля данного пакета,
#   содержимое файла настроек пакета,
#   объект API-модуля,
#   [ (название класса API, объект класса API, [(название API метода, объект API метода)]) ]
# )
imported_API_by_pkg: List[ImportedPkgAPI] = []


def reading_settings(file_path: str, props: List[str] = []) -> Dict[str, Any]:
    """Чтение содержимого указанного файла настроек. Если заданы названия требуемых свойств,
    будет возвращен словарь этих свойств, иначе все свойства."""
    # файл настроек не указан, или имеет некорректное имя
    if file_path == '' or not file_path.endswith('settings.json'):
        raise Exception(
            f'Ошибка: указан некорректный файл настроек {file_path}.')

    # считывание настроек модуля
    with open(file_path, 'r', encoding='utf-8') as settings_file:
        settings = load(settings_file, )

    # проверка того, что файл настроек имеет тип словаря
    if type(settings) != dict:
        raise Exception(
            f'Ошибка: неверный формат файла настроек {file_path}.')

    if props:
        return {prop: settings[prop] for prop in props}
    else:
        return settings


# каталог с исходниками, в котором исходники разбиты по пакетам и модулям
src = reading_settings('settings.json', ['sources_dir'])['sources_dir']


def get_api_methods(API_class) -> List[Tuple[str, Callable]]:
    """Поиск всех API методов для класса API_class.
    Признаком API метода является постфик _api в названии."""

    members = getmembers(API_class, isfunction)
    api_methods = []
    for member in members:
        if member[0].endswith("_api"):
            api_methods.append(member)
    return api_methods


def index_functionality():
    """Перечисление реализованных модулей и API, которое они предоставляют.
    Под пакетами подразумеваются подкаталоги каталога src, а под модулями файлы
    с исходными кодами в этих подкаталогах."""

    # получение имен подкаталогов каталога src
    packages = next(os.walk(src))[1]

    for pkg in packages:

        # получение имен файлов для данного каталога модулей
        pkg_files = next(os.walk(f'{src}/{pkg}'))[2]

        # если пакет не содержит файла api.py, значит в нем импортируемого API
        if 'api.py' not in pkg_files:
            continue

        # каждый пакет должен содержать файл settings.json
        if 'settings.json' not in pkg_files:
            raise Exception(f'Ошибка: пакет {pkg} не содержит файла настроек.')

        # считывание настроек пакета
        pkg_settings = reading_settings(f'{src}/{pkg}/settings.json')

        # если пакет не предоставляет API
        if len(pkg_settings["API"]) == 0:
            continue

        # импортирование модуля api
        module_obj = import_module(f'{src}.{pkg}.api')

        # итоговый список импортированных API классов пакета
        pkg_api = ImportedPkgAPI()

        # поиск по всем объектам модуля заданного типа
        # members - кортеж вида (название объекта API, объект API)
        members = getmembers(module_obj, isclass)

        # поиск API объектов, указанных в файле настроек под свойством API
        for member in members:
            for API_name in pkg_settings["API"]:

                # если данный класс является API классом
                if member[0] == API_name:

                    # ищем все API методы данного класса
                    api_methods = get_api_methods(member[1])

                    if len(api_methods) == 0:
                        break

                    pkg_api.pkgname = f'{src}.{pkg}.api'
                    pkg_api.settings = pkg_settings
                    pkg_api.module_obj = module_obj

                    pkg_api.classes.append(APIClass())
                    pkg_api.classes[-1].classname = member[0]
                    pkg_api.classes[-1].class_obj = member[1]
                    pkg_api.classes[-1].methods = api_methods

                    imported_API_by_pkg.append(pkg_api)
                    break


class InteractiveCmd:
    """Класс реализует интерактивное взаимодействие с пользователем через командную строку."""

    def __init__(self, API: List[ImportedPkgAPI]):
        self.API = API
        self.root_settings = reading_settings('settings.json')

    def welcome(self):
        """Приветствие при работе в командной строке"""
        version = self.root_settings['version']
        print(f'Исследование криптографических свойств, v. {version}')

    def display_promt(self):
        print("Выберите желаемую операцию:\n")
        i = 0
        for pkg in self.API:
            print(f"Пакет '{pkg.settings['pkg_name']}':")
            for api_class in cast(APIClass, pkg.classes):
                print(f"Класс '{api_class.classname}'")
                for method in api_class.methods:
                    params = formatargspec(*getfullargspec(method[1]))
                    print(f"[{i}] - {method[0]} - Параметры: {params}")
                    i += 1
            print()

    def interactive(self):
        self.welcome()
        while True:
            self.display_promt()

            input()
