import os
from importlib import import_module
from inspect import getmembers, isfunction, getfullargspec, formatargspec
from json import load
from types import ModuleType
from typing import Any, Callable, Dict, List, Tuple, cast

# виды API, предоставляемые модулями
API_types = {'API_functions': isfunction}

# API объекты, предоставляемые пакетами
# список кортежей вида
# (
#   полное имя API-модуля данного пакета,
#   содержимое файла настроек пакета,
#   объект API-модуля,
#   [ (название объекта API, объект API) ]
# )
imported_API_by_pkg = []
API_TYPING = Tuple[str, dict, ModuleType, List[Tuple[str, Any]]]


def reading_settings(file_path: str, props: List[str] = []) -> Dict[str, str]:
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

        # импортирование модуля api
        module_obj = import_module(f'{src}.{pkg}.api')

        # итоговый список импортированного API, разбитых по пакетам по пакетам
        imported_API_by_pkg.append(
            cast(API_TYPING,
                 (f'{src}.{pkg}.api',
                  pkg_settings,
                  module_obj,
                  [])
                 )
        )

        # поиск по типу предоставляемого API
        for API_type in (set(API_types.keys()) & set(pkg_settings.keys())):

            # поиск по всем объектам модуля заданного типа
            # members - кортеж вида (название объекта API, объект API)
            members = getmembers(module_obj, API_types[API_type])

            # поиск объектов API по допустимым названиям для данного типа API
            for member in members:
                for prefix in pkg_settings[API_type]:

                    if member[0].startswith(prefix):
                        imported_API_by_pkg[-1][-1].append(member)
                        break

        # если модуль не содержит объектов API (функции, классы...), то он удаляется
        if len(imported_API_by_pkg[-1][-1]) == 0:
            imported_API_by_pkg.pop()


def welcome() -> None:
    version = reading_settings('settings.json', ['version'])['version']
    print(f'Исследование криптографических свойств, v. {version}')


def writing_experiments_data(
        writing_func_info: Tuple[Callable[[str, Any], None]],
        filename: str,
        data: Any) -> None:
    pass


class InteractiveCmd:
    """Класс реализует интерактивное взаимодействие с пользователем через командную строку."""

    def __init__(self, API: List[API_TYPING]):
        self.API = API

        self.interactive()
        pass

    def display_promt(self):
        print("Выберите желаемую операцию:\n")
        i = 0
        for _, settings, _, api in self.API:
            print(f"Пакет '{settings['pkg_name']}':")
            for api_obj in api:
                params = formatargspec(*getfullargspec(api_obj[1]))
                print(f"[{i}] - {api_obj[0]} - Параметры: {params}")
                i += 1
            print()



    def interactive(self):
        while True:
            self.display_promt()
            
            input()
