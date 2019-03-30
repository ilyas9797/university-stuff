import os
from importlib import import_module
from inspect import (getmembers, isclass,
                     isfunction, signature, Parameter)
from json import load
from types import ModuleType
from typing import Any, Callable, Dict, List, Tuple, cast, Union


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

# определяет допустимые типы сложных (итерируемых) аргументов для API-методов,
# все остальные, подразумеваются, имеют базовые типы, например: int, str, ...
possible_API_arg_types = Union[List[int], List[str]]


def reading_settings(file_path: str, props: List[str] = None) -> Dict[str, Any]:
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


# считывание и сохранение настроек проекта
root_settings: Dict[str, Any] = reading_settings('settings.json')


# каталог с исходниками, в котором исходники разбиты по пакетам и модулям
src = root_settings['sources_dir']


def get_api_methods(api_class) -> List[Tuple[str, Callable]]:
    """Поиск всех API методов для класса API_class.
    Признаком API метода является постфик _api в названии."""
    members = getmembers(api_class, isfunction)
    api_methods = []
    for member in members:
        if member[0].endswith("_api"):
            api_methods.append(member)
    return api_methods


def check_args_types_of_method(class_obj: type, method_name: str) -> bool:
    """Проверка того, что все аргуметны API-метода имеют допустимый тип."""
    sig = signature(getattr(class_obj(), method_name))
    for param_name in sig.parameters:
        param = cast(Parameter, sig.parameters[param_name])
        param_type = param.annotation
        # проверка, что аннотация параметра присутствует
        if param_type == Parameter.empty:
            return False
        # проверка, что не базовый тип
        if type(param_type) != type:
            # проверка, что не составной тип
            if param_type not in possible_API_arg_types.__args__:
                return False
    return True


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

        # поиск API классов, указанных в файле настроек под свойством API
        for member in members:
            for API_name in pkg_settings["API"]:

                # если данный класс является API классом
                if member[0] == API_name:

                    # ищем все API методы данного класса
                    api_methods = get_api_methods(member[1])

                    if len(api_methods) == 0:
                        break

                    # проверка того, что типы аргументов API-методов допутимы
                    checked_api_methods = []
                    for api_method in api_methods:
                        if check_args_types_of_method(member[1], api_method[0]):
                            checked_api_methods.append(api_method)

                    pkg_api.pkgname = f'{src}.{pkg}.api'
                    pkg_api.settings = pkg_settings
                    pkg_api.module_obj = module_obj

                    pkg_api.classes.append(APIClass())
                    pkg_api.classes[-1].classname = member[0]
                    pkg_api.classes[-1].class_obj = member[1]
                    pkg_api.classes[-1].methods = checked_api_methods

                    imported_API_by_pkg.append(pkg_api)
                    break


class InteractiveCmd:
    """Класс реализует интерактивное взаимодействие с пользователем через командную строку."""

    class InteractiveCmdException (Exception):
        """Класс необходим для определения ошибок пользователя при взаимодействии с консолью."""
        pass

    def __init__(self, apis: List[ImportedPkgAPI]):
        self.API: List[ImportedPkgAPI] = apis

        # переменная хранит количество доступных пользователю API-методов
        self.options: int = 0

        # формирование подсказки с описанием доступного API, здесь же и обновляется self.options
        self.prompt = self.form_prompt()

        self.welcome()

    def welcome(self):
        """Приветствие при работе в командной строке."""
        version = root_settings['version']
        print(f'Исследование криптографических свойств, v. {version}.')

    def form_prompt(self) -> str:
        prompt: str = "Выберите желаемую операцию:\n\n"
        i = 0

        # цикл по всем API пакетам
        for pkg in self.API:
            prompt += f"Пакет '{pkg.settings['pkg_name']}':\n\n"

            # цикл по всем API классам в пакете
            for class_api in pkg.classes:

                # TODO: не все классы должны быть доступны в InteractiveCmd
                prompt += f"Класс '{class_api.classname}':\n\n"

                # по всем методам класса
                for method in class_api.methods:

                    # получение информации о параметрах метода
                    sig = signature(method[1])
                    prompt += f"[{i}] - {method[0]} - Параметры: {sig}\n"

                    # получение описания метода
                    prompt += method[1].__doc__ + "\n\n"
                    i += 1
        if i < 1:
            raise Exception("Ошибка: API не обнаружено.")
        self.options = i
        return prompt

    def choose_api(self, op: int) -> Tuple[APIClass, int]:
        """Установление соответствия между выбором пользователя и методом класса API."""
        #
        if op < 0 or op >= self.options:
            raise self.InteractiveCmdException("Ошибка: некорректный номер операции.")
        method_id = op
        for pkg in self.API:
            for class_api in pkg.classes:
                if (len(class_api.methods) - 1) > method_id:
                    method_id -= len(class_api.methods) - 1
                else:
                    return class_api, method_id

    def cast_api_method_arg_str_to_type(self, arg_in: str, arg_type: Any) -> possible_API_arg_types:
        """Приведение введенного пользователем аргумента API-функции к нужному типу."""
        # TODO: проверка того, что это пройстой тип, напрмер, int, str,... Возможно неправильная
        if type(arg_type) == type:
            return arg_type(arg_in)
        # иначе сложный тип, а именно list
        else:
            arg_str_list = map(lambda x: x.strip(), arg_in.split(','))
            # TODO: учесть что в сложных типах может быть задано несколько подтипов
            intype = arg_type.__args__[0]
            arg_list = []
            for arg_str in arg_str_list:
                arg_list.append(intype(arg_str))
            origin = arg_type.__origin__
            return origin(arg_list)

    def get_api_method_args(self, class_api: APIClass, method_name: str) -> List[Any]:
        """Считывает аргументы для вызова выбранного API-метода."""
        sig = signature(getattr(class_api.class_obj(), method_name))
        args = []
        for param_name in sig.parameters:
            param = cast(Parameter, sig.parameters[param_name])
            param_type = param.annotation
            arg_in = input(f"Введите {param.name}: ")
            arg = self.cast_api_method_arg_str_to_type(arg_in, param_type)
            args.append(arg)
        return args

    def interactive(self):

        while True:
            print(self.prompt)

            try:
                op = input(f"Введите номер [0-{self.options - 1}]: ")
                op = int(op)
            except Exception:
                print(f"Ошибка: выбрана некорректная опция.\nПопробуйте еще раз.")
                continue

            print()

            try:
                class_api, method_id = self.choose_api(op)
                self.get_api_method_args(class_api, class_api.methods[method_id][0])
            except self.InteractiveCmdException as e:
                print(e)
