"""Реализация класса модифицированного аддитивного генератора и вспомогательных функций"""

import math
from typing import Callable, List


def bits_number(num):
    """Возвращает количество бит, необходимое для представления числа в двоичном виде"""
    return math.floor(math.log2(num)) + 1


def nums_add_mod(nums: List[int], r: int) -> int:
    """Сложение по модулю 2^r."""
    ret = nums[0]
    for n in nums[1:]:
        ret += n
    return ret & ((1 << r) - 1)


def form_nums_list(state: int, r: int, pickup_list: List[int]) -> List[int]:
    """Формирует список значений из ячеек state указанных в pickup_list"""

    # возвращаемый список
    ret = []

    # маска для получения значения ячейки, состоит из r единиц. Для получения значения i-ой ячейки
    # сдвигается на i*r влево. Далее производится операция AND со значением текущего состояния
    # and_mask = int('1' * r, base=2)
    and_mask = (1 << r) - 1

    # для каждой точки съема
    for point in pickup_list:
        # опреление необходимого сдвига для маски
        shift = r * point

        # вычисление значения ячейки под номером point
        point_val = ((and_mask << shift) & state) >> shift

        # добавление в массив
        ret.append(point_val)
    return ret


class MAG:
    """
    Класс для формирования модифицированного аддитивного генератора с одной обратной связью и имитации его работы.

    Атрибуты экземпляров:
        r: int
        n: int
        pp: List[int]
        mf: function
        state: int
    """

    def __init__(
            self,
            r: int,
            n: int,
            pickup_points: List[int],
            modifying_func: Callable,
            init_state: int = 0):
        """
        Конструктор модифицированного многомерного линейного генератора

        Параметры:

            r (int): размерность ячейки

            n (int): количество ячеек

            pickup_points (list): список номеров точек съема

            modifying_func (function): модифицирующее преобразование
                def modifying_func(x: int): int:
                    ...

            init_state (int): начальное заполнение регистра
        """
        #
        if r <= 0:
            raise Exception
        self.r = r
        #
        if n <= 0:
            raise Exception
        self.n = n

        #
        if len(pickup_points) <= 0 or len(pickup_points) > n:
            raise Exception
        if 0 not in pickup_points:
            raise Exception
        if set(pickup_points).difference(set(i for i in range(n))):
            # содержит элементы не из промежутка [0,n-1]
            raise Exception
        self.pp = pickup_points

        # добавить проверку аргументов функции
        self.mf = modifying_func

        #
        if init_state < 0:
            raise Exception
        if init_state != 0 and bits_number(init_state) > n * r:
            raise Exception
        self.state = init_state

    def form_pp_nums(self):
        """Формирует список чисел из ячеек, соответсвующих точкам съема"""
        return form_nums_list(self.state, self.r, self.pp)

    def do_shift(self, new_val: int):
        """Производит сдвиг регистра и записывает новое значение new_val в последнюю ячейку"""

        # сдвиг в сторону младшей ячейки
        self.state = self.state >> self.r

        # запись нового значения в старшую ячейку
        self.state = self.state | (new_val << (self.r * (self.n - 1)))

    def do_cycle(self):
        """Произвести один цикл работы генератора"""

        # формирование списка зачений из ячеек, соответсвующих точкам съема
        pp_nums = self.form_pp_nums()

        # сложение по модулю значений точек съема
        added_nums = nums_add_mod(pp_nums, self.r)

        # применение модифицирующего преобразования
        modified_val = self.mf(added_nums)

        # сдвиг регистра и запись нового значения
        self.do_shift(modified_val)

    def get_current_state_val(self) -> int:
        """Возвращает значение, соответсвующее текущему состояния генератора"""
        return self.state

    def get_current_output_val(self) -> int:
        """Возвращает значение ячейки с наименьшим порядковым номером"""
        return form_nums_list(self.state, self.r, [0])[0]

    def get_current_state(self) -> List[int]:
        """Возвращает список значений ячеек, соответсвующий текущему состоянию генератора"""
        return form_nums_list(self.state, self.r, [i for i in range(self.n)])

    def __iter__(self):
        return self

    def __next__(self):
        self.do_cycle()
        return self.get_current_output_val(), self.get_current_state_val()

    def do_idling(self, idling_rounds=0):
        '''
        Проделать idling_rounds холостых ходов генератора
        '''
        if idling_rounds < 0: raise Exception('Error: wrong idling_rounds value')
        if idling_rounds == 0:
            n = self.n
        else:
            n = idling_rounds
        for _ in range(n):
            next(self)
            # pass
