"""В модуле реализованы функции строящие перемешивающие матрицы для различных типов преобразований"""

import numpy as np
from typing import List

import MMLR
from utils import cast_matrix_to_identity_format


def construct_mixing_matrix_MMLR(r: int, n: int, pp: List[int], mf_mix_matr: np.ndarray) -> np.ndarray:
    """Строит перемешивающую матрицу модифицированного многомерного линейного генератора.
    
    Параметры:

        reg (MMLR.MMLR): экземпляр генератора

        mf_mix_matr (np.ndarray): перемешивающая матрица модифицирущего преобразования
    """

    # получение размера ячейки и количества ячеек для переданого регистра
    # r, n = reg.r, reg.n

    # размер итоговой перемешивающей матрицы
    size = n * r

    # непроинициализированная итоговая матрица
    mix_matr = np.zeros((size, size), dtype=np.int)

    # подматрица итоговой перемешивающей матрицы размера r
    # соответствует зависимостям с 0 по n-2 ячеек регистра,
    # поэтому представляет из себя единичную матрицу
    cell_shift_mix_matr = np.identity(r, dtype=np.int)

    # копирование единичной подматрицы в итоговую матрицу в позиции,
    # расположенные под главной диагональю
    for i in range(n - 1):
        
        # x-овая начальная позиция копируемого блока
        pos_x = i * r + r

        # y-овая начальная позиция копируемого блока
        pos_y = i * r

        # запись в итоговую матрицу подматрицы, отображающей зависимости от сдвига
        mix_matr[pos_x: pos_x + r, pos_y: pos_y + r] = cell_shift_mix_matr
    
    # копирование перемешивающей подматрицы модифицирующего преобразования
    # в итоговую матрицу в позиции, соответсвующие точкам съема
    pos_y = (n - 1) * r
    # for point in reg.pp:
    for point in pp:
        pos_x = point * r
        mix_matr[pos_x: pos_x + r, pos_y: pos_y + r] = mf_mix_matr

    return mix_matr


def construct_mixing_matrix_mf_Sbox(r: int):
    """Составляет матрицу заполненую единицами.
    Именно так выглядит матрица для номального Sbox
    """
    return np.fromfunction(lambda i, j: 1, (r, r), dtype=int)


def construct_mixing_matrix_SPECK(size: int):
    """Строит перемешивающую матрицу для SPECK
    
    mode (int): задает размер блока SPECK в битах. Возможные значения соответсвуют ключам словаря:

        {
            1: 32,
            2: 48,
            3: 64,
            4: 96,
            5: 128
        }
    """
    if size not in [32, 48, 64, 96, 128]: 
        raise Exception
    half_size = size // 2

    shift1 = 8
    shift2 = 3
    if size == 32:
        shift1 = 7
        shift2 = 2

    # итоговая матрица состоит из четырех подматриц равного размера
    mix_matr = np.zeros((size, size), dtype=np.int)

    # заполнение верхней правой подматрицы
    tmp_add_matr = np.zeros((half_size, half_size), dtype=np.int)
    for x in range(half_size):
        for y in range(x, half_size):
            tmp_add_matr[x, y] = 1
    # mix_matr[0: half_size, half_size: size] = tmp_add_matr
    mix_matr[0: half_size, 0: half_size] = tmp_add_matr

    # заполнение верхней левой подматрицы
    tmp_matr = np.zeros((half_size, half_size), dtype=np.int)
    for i in range(half_size):
        # циклический сдвиг влево на shift2
        pos = (i + shift2) % half_size
        tmp_matr[i, pos] = 1
    tmp_matr = tmp_matr @ tmp_add_matr
    cast_matrix_to_identity_format(tmp_matr)
    # mix_matr[0: half_size, 0: half_size] = tmp_matr
    mix_matr[0: half_size, half_size: size] = tmp_matr
    
    # заполнение нижней левой подматрицы, соответсвующей сложению по модулю 2^half_size
    tmp_matr = np.zeros((half_size, half_size), dtype=np.int)
    for i in range(half_size):
        # циклический сдвиг вправо на shift1
        pos = (i - shift1 + half_size) % half_size
        tmp_matr[i, pos] = 1
    mix_matr[half_size: size, 0: half_size] = tmp_matr
    
    # заполнение нижней правой подматрицы, соответсвующей циклическому сдвигу влево на shift2
    mix_matr[half_size: size, half_size: size] = tmp_matr

    return mix_matr
