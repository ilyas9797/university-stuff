"""В модуле реализованы функции для оценки перемешивающих свойств преобразований по их перемешивающим матрицам"""

import operator

import numpy as np

import mixing_matrixes
import MMLR
from utils import cast_matrix_to_identity_format, comb


def pow_matrix_gen(matr: np.ndarray):
    """Питоновский генератор, последовательно возводящий матрицу в степень.
    На каждой итерации матрица приводится к единично-нормальной форме.
    """
    powed_matr = matr.copy()
    while True:
        cast_matrix_to_identity_format(powed_matr)
        yield powed_matr
        powed_matr = powed_matr @ matr


def check_full_mixing(matr: np.ndarray) -> bool:
    """Проверка того, что полное перемешивание достигнуто"""
    size = matr.shape[0]
    for i in range(size):
        for j in range(size):
            if matr[i, j] == 0: 
                return False
    else:
        return True


def get_exponent(mix_matr: np.ndarray, max_rounds: int) -> int:
    """Возвращает значение экспоненты, если число раундов превзошло max_rounds, вернет -1"""
    i = 0
    for m in pow_matrix_gen(mix_matr):
        if check_full_mixing(m):
            return i
        i += 1
        if i > max_rounds:
            break
    return -1
        

if __name__ == '__main__':
    np.set_printoptions(threshold=np.nan)
    r = 32
    n = 8
    mf = None
    for ppnum in range(1, n):
        results = list()
        for pp in comb(n - 1, ppnum):
            pickup_points = [0] + pp
            # reg1 = MMLR.MMLR(r, n, pickup_points, mf)
            # mix_matr = mixing_matrixes.construct_mixing_matrix_MMLR(reg1, mixing_matrixes.construct_mixing_matrix_SPECK(reg1.r))
            mix_matr = mixing_matrixes.construct_mixing_matrix_MMLR(r, n, pickup_points, mixing_matrixes.construct_mixing_matrix_SPECK(r))
            power = 1
            for m in pow_matrix_gen(mix_matr):
                if check_full_mixing(m):
                    results.append((power, f"Register: r={r}, n={n}, pickup_points={pickup_points}, power="))
                    break
                power += 1
                if power > 25:
                    break
        results = list(sorted(results, key=operator.itemgetter(0)))
        with open(f"samples/register_r_{r}_n_{n}_ppnum_{ppnum+1}(with_SPECK).txt", 'w') as file:
            file.write('\n'.join(f"{r[1]}{r[0]}" for r in results))
        
    # np.set_printoptions(threshold=np.nan, linewidth=np.nan)
    # with open('speck.txt','w') as file:
    #     m = mixing_matrixes.construct_mixing_matrix_SPECK(1)
    #     file.write(str(m))
    #     print(get_exponent(m, 20))
    # pass
