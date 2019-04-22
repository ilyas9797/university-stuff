"""В модуле реализованы функции для оценки перемешивающих свойств преобразований по их перемешивающим матрицам"""


import numpy as np
from src.mixing_matrixes.utils import cast_matrix_to_identity_format


def pow_matrix_gen(matrix: np.ndarray):
    """Питоновский генератор, последовательно возводящий матрицу в степень.
    На каждой итерации матрица приводится к единично-нормальной форме.
    """
    powed_matrix = matrix.copy()
    while True:
        powed_matrix = cast_matrix_to_identity_format(powed_matrix)
        yield powed_matrix
        powed_matrix = powed_matrix @ matrix


def check_full_mixing(matrix: np.ndarray) -> bool:
    """Проверка того, что полное перемешивание достигнуто"""
    size = matrix.shape[0]
    for i in range(size):
        for j in range(size):
            if matrix[i, j] == 0:
                return False
    else:
        return True


def get_exponent(mix_matr: np.ndarray, max_rounds: int) -> int:
    """Возвращает значение экспоненты для перемешивающей матрицы mix_matr,
    если число раундов превзошло max_rounds, вернет -1"""
    i = 1
    for m in pow_matrix_gen(mix_matr):
        if check_full_mixing(m):
            return i
        i += 1
        if i > max_rounds:
            break
    return -1


def check_local_full_mixing(matr: np.ndarray, local_start: int, local_end: int) -> bool:
    """Проверка того, что полное перемешивание достигнуто"""
    size = matr.shape[0]
    for i in range(size):
        for j in range(local_start, local_end):
            if matr[i, j] == 0:
                return False
    else:
        return True


def get_local_exponent(mix_matr: np.ndarray, max_rounds: int, local_start: int, local_end: int) -> int:
    """Возвращает значение экспоненты для перемешивающей матрицы mix_matr,
    если число раундов превзошло max_rounds, вернет -1"""
    i = 1
    for m in pow_matrix_gen(mix_matr):
        if check_local_full_mixing(m, local_start, local_end):
            return i
        i += 1
        if i > max_rounds:
            break
    return -1
