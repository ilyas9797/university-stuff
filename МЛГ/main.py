import operator


from mixing_matrixes import (construct_mixing_matrix_MMLR,
                             construct_mixing_matrix_SPECK)
from mixing_props import get_exponent
from utils import comb, write_exponents


def research_mixing_props_MMLR_SPECK(r: int, n: int, ppnum_b: int, ppnum_e: int, max_rounds: int):
    """
    Изучает перемешивающие свойства ММЛГ с модифицирующей функцией SPECK.
    Перебирает различные ММЛГ варьируя числом точек съема и их расположением.

    r: размерность ячейки

    n: длинна генератора

    ppnum_b: начальное кол-во точек съема

    ppnum_e: конечное число точек съема

    max_rounds: максимальная степень, до которой перемешивающая матрица генератора с определенным набором точек съема будет возводиться
    """

    # перебор различного количества точек съема
    # ppnum_b - 1, ppnum_e - т.к. 0 точка съема всегда присутсвует
    for ppnum in range(ppnum_b - 1, ppnum_e):

        # results: [(ppnum, pp, power)]
        results = list()

        # перебор различный расстановок точек съема для заданного количества точек съема
        # n-1 - т.к. 0 точка съема всегда присутсвует
        for pp in comb(n - 1, ppnum):
            pickup_points = [0] + pp
            mix_matr = construct_mixing_matrix_MMLR(r, n, pickup_points, construct_mixing_matrix_SPECK(r))
            power = get_exponent(mix_matr, max_rounds)
            if power != -1:
                results.append((ppnum + 1, pickup_points, power))
        
        results = list(sorted(results, key=operator.itemgetter(2)))

        write_exponents(
            f"./samples/MMLR_SPECK/r_{r}_n_{n}_ppnum_{ppnum + 1}.txt",
            results
        )


if __name__ == '__main__':
    research_mixing_props_MMLR_SPECK(r=32, n=8, ppnum_b=2, ppnum_e=8, max_rounds=25)
