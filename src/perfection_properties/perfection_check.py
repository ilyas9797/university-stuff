from random import randint
from typing import Generator, List, Callable, Tuple, Union
from src.generators.mmlr import MMLR
from src.generators.mag import MAG


def gen_random_samples(n: int, num: int) -> List[int]:
    """Формирует список длины num случайных n-битных чисел чисел.
    """
    samples_ret = []
    Max = (1 << n) - 1
    for _ in range(num):
        samples_ret.append(randint(0, Max))
    return samples_ret


def get_neighbor_numbers(x: int, i: int) -> Tuple[int, int]:
    """Возвращает два соседних числа для x по i-ой переменной.
    """
    # 1 на i-ой позиции
    first = x | (1 << i)

    # 0 на i-ой позиции
    second = first ^ (1 << i)

    return first, second


def get_GEN_class_generators(
    n: int,
    r: int,
    pp: List[int],
    mf: Callable,
    samples: List[int],
    GEN_class: Union[MAG, MMLR]
) -> List[List[Tuple[Generator]]]:
    """Формирование len(samples)*2*n python-генераторов соответствующих соседним числам из samples по всем возможным координатам.
    Параметры:
        n:           длина ячейки для исследуемого генератора
        r:
        pp:
        mf:
        samples:     входной блок, для которого будет сформирован python-генераторы
        GEN_class:
    Возвращаемые генераторы сгруппированны следующим образом:
        ret[соседний по i-ой координате][для такого-то sample][с 0-ем или с 1-ей на i-ой позиции]
        ret[n][len(samples)][2]
    """
    length = n*r

    gens_ret = [[] for j in range(length)]

    # перебираем различные координаты
    for i in range(length):

        # формируем список пар генераторов заведенных для пар чисел из samples соседних по i-ой координате чисел
        # все на ключе key
        for sample in samples:

            # соседние векторы по i координате, для вектра sample
            first, second = get_neighbor_numbers(sample, i)

            gen_first = GEN_class(r, n, pp, mf, first)
            gen_second = GEN_class(r, n, pp, mf, second)

            # формирование двух генераторов для пары соседних по i-ой координате чисел, соответсвующих sample
            gens_ret[i].append(
                # (cipher_gen(first, key), cipher_gen(second, key))
                # (cipher_gen(first), cipher_gen(second))
                (gen_first, gen_second)
            )

    return gens_ret


def get_next_gens_states(
    n: int, 
    samples_num: int, 
    gens: List[List[Tuple[Generator]]]
) -> List[List[Tuple[int, int]]]:
    """
    Получает выходные значения для переданных генераторов шифров для следующего раунда.
    Генераторы должны быть предварительно сформированы вызовом get_GEN_class_generators.
    Параметры:
        n:            длина блока для исследуемого алгоритма
        samples_num:  длинна списка передаваемого в get_GEN_class_generators через параметр samples
        gens:         генераторы, полученные вызовом get_GEN_class_generators
    """
    states_ret = [[] for j in range(n)]
    for i in range(n):
        for sample_num in range(samples_num):
            first_gen, second_gen = gens[i][sample_num]
            states_ret[i].append(
                (
                    next(first_gen)[1], 
                    next(second_gen)[1]
                )
            )
    return states_ret


def check_current_round(
    n: int, 
    samples_num: int, 
    states: List[List[Tuple[int, int]]]
) -> bool:
    """Проверка того что для данного раунда шифрования преобразование совершенно. (описание и комментарии плохие)
    Параметры:
        n:             длина блока для исследуемого алгоритма
        samples_num:   длинна списка передаваемого в get_MMLR_generators через параметр samples
        states:
    """

    # результирующий проверочный вектор должен состоять только из единиц
    resulted_vect = 2**n - 1

    # по всем координатам блока
    for i in range(n):
        i_resulted_vect = 0

        # для каждого sample
        for sample_num in range(samples_num):
            first, second = states[i][sample_num]

            # проверяем сколько различных выходных координат изменилось при изменении i-ой входной координаты в значении states[i][sample_num]
            sample_num_resulted_vect = first ^ second

            # добавляем зависимости i-ой координатной функции вычисленной для другой пары соседних samples
            i_resulted_vect |= sample_num_resulted_vect

        # если текущая координатная функция несовершенна, то выходим из функции
        if i_resulted_vect != resulted_vect:
            return False

    # если каждая координатная функция совершенна, то преобразование совершенно
    return True


def get_GEN_class_perfection_power(
    n: int,
    r: int,
    pp: List[int],
    mf: Callable[[int], int],
    samples_num: int,
    max_rounds: int,
    GEN_class: Union[MAG, MMLR]
) -> int:
    """
    Определяет показатель совершенности для переданного алгоритма.
    Параметры:
        n: размер блока
        r:
        pp:
        mf: 
        samples_num: количество пар соседних векторов, на которых будет происходить проверка
        max_rounds: максимальная число раундов зашифрования, до которой стоит пытаться определить показатель
    """
    length = n * r

    # сформируем samples_num случайных чисел для формирования из них пар соседних векторов
    samples = gen_random_samples(length, samples_num)

    # сформируем всевозможные необходимые генераторы в количестве n*samples_num*2
    gens = get_GEN_class_generators(
        n,
        r,
        pp,
        mf,
        samples,
        GEN_class
    )

    for round in range(max_rounds):

        round_states = get_next_gens_states(length, samples_num, gens)

        if check_current_round(length, samples_num, round_states):
            return round + 1
    return -1