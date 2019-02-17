"""В модуле реализованы функции строящие перемешивающие матрицы для различных типов преобразований
Нумерация координат в матрицах следующая:
(0,n-1)    . . .   (0,0)

  .     .           .
  .        .        .
  .           .     .

(n-1,n-1)  . . .   (n-1,0)
"""

import numpy as np
from typing import List

from utils import cast_matrix_to_identity_format

def change_column_order(matr: np.ndarray) -> np.ndarray:
    shape = matr.shape
    ret_matr = np.ndarray(shape, dtype=np.int)
    for i in range(shape[1]):
        ret_matr[0: shape[0], i: i + 1] = matr[0: shape[0], shape[1] - i - 1: shape[1] - i]
    return ret_matr

def construct_mixing_matrix_MMLR(r: int, n: int, pp: List[int], mf_mix_matr: np.ndarray) -> np.ndarray:
    """Строит перемешивающую матрицу модифицированного многомерного линейного генератора."""

    # размер итоговой перемешивающей матрицы
    size = n * r

    # непроинициализированная итоговая матрица
    mix_matr = np.zeros((size, size), dtype=np.int)

    # подматрица итоговой перемешивающей матрицы размера r
    # соответствует зависимостям с 0 по n-2 ячеек регистра,
    # поэтому представляет из себя единичную матрицу
    cell_shift_mix_matr = np.eye(r, dtype=np.int)
    
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

# def construct_mixing_matrix_MMLR(r: int, n: int, pp: List[int], mf_mix_matr: np.ndarray) -> np.ndarray:
#     """Строит перемешивающую матрицу модифицированного многомерного линейного генератора.
    
#     Параметры:

#         reg (MMLR.MMLR): экземпляр генератора

#         mf_mix_matr (np.ndarray): перемешивающая матрица модифицирущего преобразования
#     """

#     # получение размера ячейки и количества ячеек для переданого регистра
#     # r, n = reg.r, reg.n

#     # размер итоговой перемешивающей матрицы
#     size = n * r

#     # непроинициализированная итоговая матрица
#     mix_matr = np.zeros((size, size), dtype=np.int)

#     # подматрица итоговой перемешивающей матрицы размера r
#     # соответствует зависимостям с 0 по n-2 ячеек регистра,
#     # поэтому представляет из себя единичную матрицу
#     cell_shift_mix_matr = np.identity(r, dtype=np.int)

    # # копирование единичной подматрицы в итоговую матрицу в позиции,
    # # расположенные под главной диагональю
    # for i in range(n - 1):
        
    #     # x-овая начальная позиция копируемого блока
    #     pos_x = i * r + r

    #     # y-овая начальная позиция копируемого блока
    #     pos_y = i * r

    #     # запись в итоговую матрицу подматрицы, отображающей зависимости от сдвига
    #     mix_matr[pos_x: pos_x + r, pos_y: pos_y + r] = cell_shift_mix_matr
    
#     # копирование перемешивающей подматрицы модифицирующего преобразования
#     # в итоговую матрицу в позиции, соответсвующие точкам съема
#     pos_y = (n - 1) * r
#     # for point in reg.pp:
#     for point in pp:
#         pos_x = point * r
#         mix_matr[pos_x: pos_x + r, pos_y: pos_y + r] = mf_mix_matr

#     return mix_matr


# def construct_mixing_matrix_mf_Sbox(r: int):
#     """Составляет матрицу заполненую единицами.
#     Именно так выглядит матрица для 'нормального' S-box
#     """
#     return np.fromfunction(lambda i, j: 1, (r, r), dtype=int)

def construct_mixing_matrix_SPECK(size: int):
    """Строит перемешивающую матрицу для SPECK
    
    size (int): задает размер блока SPECK в битах. Возможные значения соответсвуют ключам словаря:
    """
    if size not in [32, 48, 64, 96, 128]: 
        raise Exception("Ошибка: выбран неверный размер блока SPECK")
    half_size = size // 2

    alpha = 8
    betta = 3
    if size == 32:
        alpha = 7
        betta = 2

    left_betta_shift = np.zeros((half_size, half_size), dtype=np.int)
    for i in range(half_size):
        left_betta_shift[i, (-(i + 1) - betta + half_size) % half_size] = 1

    triangular = np.zeros((half_size, half_size), dtype=np.int)
    for i in range(half_size):
        for j in range(half_size - i):
            triangular[i, j] = 1

    top_left = triangular

    top_right = left_betta_shift + triangular
    cast_matrix_to_identity_format(top_right)

    right_alpha_shift = np.zeros((half_size, half_size), dtype=np.int)
    for i in range(half_size):
        right_alpha_shift[i, (-(i + 1) + alpha + half_size) % half_size] = 1

    bottom_left = bottom_right = right_alpha_shift @ triangular

    res_matr = np.zeros((half_size*2, half_size*2), dtype=np.int)

    res_matr[0: half_size, 0: half_size] = top_left
    res_matr[0: half_size, half_size: size] = top_right
    res_matr[half_size: size, 0: half_size] = bottom_left
    res_matr[half_size: size, half_size: size] = bottom_right

    return change_column_order(res_matr)

# def construct_mixing_matrix_SPECK(size: int):
#     """Строит перемешивающую матрицу для SPECK
    
#     size (int): задает размер блока SPECK в битах. Возможные значения соответсвуют ключам словаря:
#     """
#     if size not in [32, 48, 64, 96, 128]: 
#         raise Exception("Ошибка: выбран неверный размер блока SPECK")
#     half_size = size // 2

#     alpha = 8
#     betta = 3
#     if size == 32:
#         alpha = 7
#         betta = 2

#     mix_matr1 = np.zeros((half_size, half_size), dtype=np.int)
#     for i in range(half_size):
#         mix_matr1[i, (-(i + 1) - betta + half_size) % half_size] = 1

#     mix_matr2 = np.zeros((half_size, half_size), dtype=np.int)
#     for i in range(half_size):
#         for j in range(half_size - i):
#             mix_matr2[i, j] = 1

#     top_left = mix_matr2

#     top_right = mix_matr1 + mix_matr2
#     cast_matrix_to_identity_format(top_right)

#     mix_matr3 = np.zeros((half_size, half_size), dtype=np.int)
#     for i in range(half_size):
#         mix_matr3[i, (-(i + 1) + alpha + half_size) % half_size] = 1

#     bottom_left = bottom_right = mix_matr3

#     res_matr = np.zeros((half_size*2, half_size*2), dtype=np.int)

#     res_matr[0: half_size, 0: half_size] = top_left
#     res_matr[0: half_size, half_size: size] = top_right
#     res_matr[half_size: size, 0: half_size] = bottom_left
#     res_matr[half_size: size, half_size: size] = bottom_right

#     return res_matr


def construct_mixing_matrix_pow_SPECK(pow: int, size: int):
    if pow < 1:
        raise Exception("Степень перемешивающей матрицы не должна быть меньше 1")

    mixing_matrix_SPECK = construct_mixing_matrix_SPECK(size)
    ret_mixing_matrix_SPECK = construct_mixing_matrix_SPECK(size)

    for _ in range(pow - 1):
        ret_mixing_matrix_SPECK = ret_mixing_matrix_SPECK @ mixing_matrix_SPECK
        cast_matrix_to_identity_format(ret_mixing_matrix_SPECK)

    return ret_mixing_matrix_SPECK




# def construct_mixing_matrix_SPECK(size: int):
#     """Строит перемешивающую матрицу для SPECK
    
#     size (int): задает размер блока SPECK в битах. Возможные значения соответсвуют ключам словаря:
#     """
#     if size not in [32, 48, 64, 96, 128]: 
#         raise Exception("Ошибка: выбран неверный размер блока SPECK")
#     half_size = size // 2

#     shift1 = 8
#     shift2 = 3
#     if size == 32:
#         shift1 = 7
#         shift2 = 2

#     # итоговая матрица состоит из четырех подматриц равного размера
#     mix_matr = np.zeros((size, size), dtype=np.int)

#     # заполнение верхней правой подматрицы
#     tmp_add_matr = np.zeros((half_size, half_size), dtype=np.int)
#     for x in range(half_size):
#         for y in range(x, half_size):
#             tmp_add_matr[x, y] = 1
#     # mix_matr[0: half_size, half_size: size] = tmp_add_matr
#     mix_matr[0: half_size, 0: half_size] = tmp_add_matr

#     # заполнение верхней левой подматрицы
#     tmp_matr = np.zeros((half_size, half_size), dtype=np.int)
#     for i in range(half_size):
#         # циклический сдвиг влево на shift2
#         pos = (i + shift2) % half_size
#         tmp_matr[i, pos] = 1
#     tmp_matr = tmp_matr @ tmp_add_matr
#     cast_matrix_to_identity_format(tmp_matr)
#     # mix_matr[0: half_size, 0: half_size] = tmp_matr
#     mix_matr[0: half_size, half_size: size] = tmp_matr
    
#     # заполнение нижней левой подматрицы, соответсвующей сложению по модулю 2^half_size
#     tmp_matr = np.zeros((half_size, half_size), dtype=np.int)
#     for i in range(half_size):
#         # циклический сдвиг вправо на shift1
#         pos = (i - shift1 + half_size) % half_size
#         tmp_matr[i, pos] = 1
#     mix_matr[half_size: size, 0: half_size] = tmp_matr
    
#     # заполнение нижней правой подматрицы, соответсвующей циклическому сдвигу влево на shift2
#     mix_matr[half_size: size, half_size: size] = tmp_matr

#     return mix_matr


# def construct_mixing_matrix_upper_triangular(size: int) -> np.ndarray:
    
#     mix_matr = np.zeros((size, size), dtype=np.int)
#     for x in range(size):
#         for y in range(x, size):
#             mix_matr[x, y] = 1
#     return mix_matr


