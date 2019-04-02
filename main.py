"""
Точка входа в программу. Реализует интерактивное взаимодействие с пользователем через командную строку.
"""
import utils


def main():
    """
    Перечисление реализованного функционала.
    Интерактивное взаимодействие с пользователем.
    Запуск экспериментов, выбранных пользователем.
    """
    utils.index_functionality()
    console = utils.InteractiveCmd(utils.imported_API_by_pkg)
    console.interactive()


if __name__ == '__main__':
    main()
