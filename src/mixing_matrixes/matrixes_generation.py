"""Функции построения перемешивающих матриц для различных преобразований."""
from typing import List

import numpy as np

from src.mixing_matrixes.utils import cast_matrix_to_identity_format, change_column_order, write_matrix_pretty


def construct_matrix_MMLR(r: int, n: int, pickup_points: List[int], mt_matrix: np.ndarray, filename: str=None) -> np.ndarray:
    """Строит перемешивающую матрицу модифицированного многомерного линейного генератора."""

    # проверка того, что размер ячейки генератора равен размеру матрицы модифицирующего преобразования
    if r != mt_matrix.shape[0] or r != mt_matrix.shape[1]:
        raise Exception(
            'Ошибка: размер ячейки генератора не равен размеру матрицы модифицирующего преобразования')

    # размер итоговой перемешивающей матрицы
    size = n * r

    # незаполненная итоговая матрица
    matrix = np.zeros((size, size), dtype=np.int)

    # подматрица итоговой перемешивающей матрицы размера r
    # соответствует зависимостям с 0 по n-2 ячеек регистра,
    # поэтому представляет из себя единичную матрицу
    shift_matrix = np.eye(r, dtype=np.int)

    # копирование единичной подматрицы в итоговую матрицу в позиции,
    # расположенные под главной диагональю
    for i in range(n - 1):

        # x-овая начальная позиция копируемого блока
        pos_x = i * r + r

        # y-овая начальная позиция копируемого блока
        pos_y = i * r

        # запись в итоговую матрицу подматрицы, отображающей зависимости от сдвига
        matrix[pos_x: pos_x + r, pos_y: pos_y + r] = shift_matrix

    # копирование перемешивающей подматрицы модифицирующего преобразования
    # в итоговую матрицу в позиции, соответсвующие точкам съема
    pos_y = (n - 1) * r
    for point in pickup_points:
        pos_x = point * r
        matrix[pos_x: pos_x + r, pos_y: pos_y + r] = mt_matrix

    if filename:
        write_matrix_pretty(filename, matrix)

    return matrix


def construct_matrix_SPECK(size: int, filename: str=None) -> np.ndarray:
    """Строит перемешивающую матрицу для пробразования однораундового SPECK.

    size (int): задает размер блока SPECK в битах. Возможные значения: [32, 48, 64, 96, 128]
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
    top_right = cast_matrix_to_identity_format(top_right)

    right_alpha_shift = np.zeros((half_size, half_size), dtype=np.int)
    for i in range(half_size):
        right_alpha_shift[i, (-(i + 1) + alpha + half_size) % half_size] = 1

    bottom_left = bottom_right = change_column_order(
        change_column_order(right_alpha_shift) @ change_column_order(triangular))

    matrix_SPECK = np.zeros((half_size*2, half_size*2), dtype=np.int)

    matrix_SPECK[0: half_size, 0: half_size] = top_left
    matrix_SPECK[0: half_size, half_size: size] = top_right
    matrix_SPECK[half_size: size, 0: half_size] = bottom_left
    matrix_SPECK[half_size: size, half_size: size] = bottom_right

    if filename:
        write_matrix_pretty(filename, change_column_order(matrix_SPECK))

    return change_column_order(matrix_SPECK)


def construct_mixing_matrix_pow_SPECK(pow: int, size: int, filename: str=None) -> np.ndarray:
    if pow < 1:
        raise Exception(
            'Ошибка: степень перемешивающей матрицы не должна быть меньше 1')

    matrix_SPECK_one_round = construct_matrix_SPECK(size)
    matrix_SPECK_powed = construct_matrix_SPECK(size)

    for _ in range(pow - 1):
        matrix_SPECK_powed = matrix_SPECK_powed @ matrix_SPECK_one_round
        matrix_SPECK_powed = cast_matrix_to_identity_format(matrix_SPECK_powed)

    if filename:
        write_matrix_pretty(filename, matrix_SPECK_powed)

    return matrix_SPECK_powed
