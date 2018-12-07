import numpy as np
from typing import List, Generator
from random import randint


def gen_random_samples(n: int, num: int) -> List[int]:
    """
    Формирует список длины num случайных n-битных чисел чисел

    return: списки 
    """
    samples_ret = []
    Max = 2**n - 1
    for i in range(num):
        samples_ret.append(randint(0, Max))
    return samples_ret


def get_neighbor_numbers(x: int, i: int) -> (int, int):
    """
    Возвращает два соседних числа для x по i-ой переменной
    """
    # 1 на i-ой позиции
    first  =     x | (1 << i)
    second = first ^ (1 << i)
    return (first, second)


def get_encryptions_gens(n: int, cipher_gen: Generator, samples: List[int], key: int) -> List[List[(Generator, Generator)]]:
    """
    Сформируем samples*2*n генераторов соответствующих соседним числам из samples по всем возможным координатам

    cipher_gen должен принимать следующие аргументы: (block, key)
    
    Сгруппированны следующим образом:

        ret[соседний по i-ой координате][для такого-то sample][с 0-ем или с 1-ей на i-ой позиции]
                            
        ret[n][len(samples)][2]

    """
    gens_ret = [[] for j in range(n)]

    # перебираем различные координаты
    for i in range(n):

        # формируем список пар генераторов заведенных для пар чисел из samples соседних по i-ой координате чисел
        # все на ключе key
        for sample in samples:

            # соседние числа
            first, second = get_neighbor_numbers(sample, i)

            # формирование двух генераторов для пары соседних по i-ой координате чисел, соответсвующих sample 
            gens_ret[i].append((cipher_gen(first, key), cipher_gen(second, key)))
    
    return gens_ret


def get_next_gens_states(n: int, samples_num: int, gens: List[List[(Generator, Generator)]]) -> List[List[(int, int)]]:
    """
    Получает выходные значения для переданных генераторов шифров для следующего раунда
    """
    states_ret = [[] for j in range(n)]
    for i in range(n):
        for sample_num in range(samples_num):
            first_gen, second_gen = gens[i][sample_num]
            states_ret[i].append((next(first_gen), next(second_gen)))
    return states_ret


def check_current_round(n: int, samples_num:int, states: List[List[(int, int)]]) -> bool:
    """
    
    """
    resulted_vect = 2**n - 1
    for i in range(n):
        i_resulted_vect = 0
        for sample_num in range(samples_num):
            first, second = states[i][sample_num]
            sample_num_resulted_vect = first ^ second
            i_resulted_vect |= sample_num_resulted_vect

        # если текущая координатная функция несовершенна, то выходим из функции
        if i_resulted_vect != resulted_vect:
            return False
    return True


def get_perfection_power(
    n: int, 
    key_n: int, 
    cipher_gen: Generator, 
    samples_num: int,
    max_rounds: int, 
    key: int=0
    ) -> int:
    """
    Определяет показатель совершенности для переданного алгоритма
    
    n: размер блока

    key_n: размер ключа

    cipher_gen: генератор реализующий шифр, принимающий аргументы (block, key)

    samples_num: количество пар соседних векторов, на которых будет происходить проверка

    max_rounds: максимальная степень, до которой стоит пытаться определить показатель

    key: ключ
    """

    # сформируем samples_num случайных чисел для формирования из них пар соседних векторов
    samples = gen_random_samples(n, samples_num)

    # сформируем всевозможные необходимые генераторы в количестве n*samples_num*2
    gens = get_encryptions_gens(n, cipher_gen, samples, key)
    
    for round in range(max_rounds):

        round_states = get_next_gens_states(n, samples_num, gens)

        if check_current_round(n, samples_num, round_states):
            return round + 1
    return -1


