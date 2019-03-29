"""Вспомогательные функции для построения перемешивающих матриц."""
import numpy as np


def change_column_order(matrix: np.ndarray) -> np.ndarray:
    """Изменение порядка столбцов в матрице"""
    shape = matrix.shape
    new_matrix = np.zeros(shape, dtype=np.int)

    for i in range(shape[1]):
        new_matrix[0: shape[0], i: i + 1] = matrix[0: shape[0],
                                               shape[1] - i - 1: shape[1] - i]
    
    return new_matrix


def cast_matrix_to_identity_format(matrix: np.ndarray) -> np.ndarray:
    """Заменяет все элементы матрицы большие нуля на 1."""
    shape = matrix.shape
    new_matrix = np.zeros(shape, dtype=np.int)

    for i in range(shape[0]):
        for j in range(shape[1]):
            if matrix[i, j] > 0:
                matrix[i, j] = 1

    return new_matrix
