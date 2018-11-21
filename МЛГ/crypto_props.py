import numpy as np

import main_class


def construct_mixing_matrix_MMLR(reg: main_class.MMLR, mf_mix_matr: np.ndarray):
    r, n = reg.r, reg.n
    size = n * r
    mix_matr = np.zeros((size, size), dtype=np.int)
    cell_shift_mix_matr = np.identity(r, dtype=np.int)
    for i in range(1, n):
        pos_x = i * r + r
        pos_y = i * r
        mix_matr[pos_x: pos_x + r, pos_y: pos_y + r] = cell_shift_mix_matr
    
    pos_y = (n - 1) * r
    for point in range(reg.pp):
        pos_x = point * r
        mix_matr[pos_x: pos_x + r, pos_y: pos_y + r] = mf_mix_matr

    return mix_matr


def construct_mixing_matrix_mf_Sbox(r: int):
    return np.fromfunction(lambda i, j: 1, (r, r), dtype=int)


def pow_matrix_gen(matr: np.ndarray):
    yield matr
    powed_matr = matr
    
