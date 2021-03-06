import operator

from algo.speck import one_round_SPECK_32
from mixing_matrixes import (construct_mixing_matrix_MMLR,
                             construct_mixing_matrix_SPECK,
                             construct_mixing_matrix_pow_SPECK)
from mixing_props import get_exponent, get_local_exponent
from perfection_props import get_MMLR_perfection_power
from utils import comb, write_exponents, write_matrix, write_perf_index, progress_info


from multiprocessing import Process


def research_mixing_props_MMLR_SPECK(r: int, n: int, ppnum_min: int, ppnum_max: int, max_rounds: int, pow: int):
    """
    Изучает перемешивающие свойства ММЛГ с модифицирующей функцией SPECK.
    Перебирает различные ММЛГ варьируя числом точек съема и их расположением.

    r: размерность ячейки

    n: длинна генератора

    ppnum_min: минимальное перебираемое кол-во точек съема

    ppnum_max: максимальное перебираемое число точек съема

    max_rounds: максимальная степень, до которой перемешивающая матрица генератора с определенным набором точек съема будет возводиться
    
    pow: степень матрицы SPECK
    """

    # перебор различного количества точек съема
    # ppnum_min - 1, ppnum_max - т.к. 0 точка съема всегда присутсвует
    for ppnum in range(ppnum_min - 1, ppnum_max):

        # results: [(ppnum, pp, power)]
        results = list()

        # перебор различный расстановок точек съема для заданного количества точек съема
        # n-1 - т.к. 0 точка съема всегда присутсвует
        for pp in comb(n - 1, ppnum):
            pickup_points = [0] + pp

            # формирование перемешивающей матрицы МЛГ, с учетом перемешивающей матрицы для модифицируюшего преобразования SPECK
            mix_matr = construct_mixing_matrix_MMLR(
                r,
                n,
                pickup_points,
                construct_mixing_matrix_pow_SPECK(pow, r))
                # construct_mixing_matrix_SPECK(r))

            # нахождение экспоненты рассматриваемой перемешивающей матрицы МЛГ
            power = get_exponent(mix_matr, max_rounds)

            # если экспонент найден, сохраняем информацию о данном варианте МЛГ
            # также сохраняем перемешивающую матрицу для данного МЛГ с точками съема pickup_points
            if power != -1:
                results.append((ppnum + 1, pickup_points, power))
                # write_matrix(
                #     f"./matrixes/MMLR_SPECK/ppnum_{ppnum}_pp_{pickup_points}.txt",
                #     mix_matr
                # )

        # сотрируем результаты для МЛГ с задданым ppnum числом точек съема со всеми воможными расположениями точек съема по значению экспонента (от меньшего к большему)
        results = list(sorted(results, key=operator.itemgetter(2)))

        write_exponents(
            f"./exponents/MMLR_SPECK_pow_{pow}/r_{r}_n_{n}_ppnum_{ppnum + 1}.txt",
            results
        )

        progress_info(f"ppnum={ppnum + 1} done")

def research_local_mixing_props_MMLR_SPECK(r: int, n: int, ppnum_min: int, ppnum_max: int, max_rounds: int, cell: int):
    local_start = r * cell
    local_end = local_start + r
    # перебор различного количества точек съема
    # ppnum_min - 1, ppnum_max - т.к. 0 точка съема всегда присутсвует
    for ppnum in range(ppnum_min - 1, ppnum_max):

        # results: [(ppnum, pp, power)]
        results = list()

        # перебор различный расстановок точек съема для заданного количества точек съема
        # n-1 - т.к. 0 точка съема всегда присутсвует
        for pp in comb(n - 1, ppnum):
            pickup_points = [0] + pp

            # формирование перемешивающей матрицы МЛГ, с учетом перемешивающей матрицы для модифицируюшего преобразования SPECK
            mix_matr = construct_mixing_matrix_MMLR(
                r,
                n,
                pickup_points,
                construct_mixing_matrix_SPECK(r))

            # нахождение экспоненты рассматриваемой перемешивающей матрицы МЛГ
            power = get_local_exponent(mix_matr, max_rounds, local_start, local_end)

            # если экспонент найден, сохраняем информацию о данном варианте МЛГ
            # также сохраняем перемешивающую матрицу для данного МЛГ с точками съема pickup_points
            if power != -1:
                results.append((ppnum + 1, pickup_points, power))
                # write_matrix(
                #     f"./matrixes/MMLR_SPECK/ppnum_{ppnum}_pp_{pickup_points}.txt",
                #     mix_matr
                # )

        # сотрируем результаты для МЛГ с задданым ppnum числом точек съема со всеми воможными расположениями точек съема по значению экспонента (от меньшего к большему)
        results = list(sorted(results, key=operator.itemgetter(2)))

        write_exponents(
            f"./local_exponents/MMLR_SPECK_cell_{cell}/r_{r}_n_{n}_ppnum_{ppnum + 1}.txt",
            results
        )
        progress_info(f"ppnum={ppnum + 1} done")

def research_perfection_props_MMLR_SPECK(
    n: int,
    r: int,
    ppnum_min: int, 
    ppnum_max: int,
    samples_num: int,
    max_rounds: int
):

    # перебор различного количества точек съема
    # ppnum_min - 1, ppnum_max - т.к. 0 точка съема всегда присутсвует
    for ppnum in range(ppnum_min - 1, ppnum_max):

        # results: [(ppnum, pp, perf_index)]
        results = list()

        # перебор различный расстановок точек съема для заданного количества точек съема
        # n-1 - т.к. 0 точка съема всегда присутсвует
        for pp in comb(n - 1, ppnum):
            pickup_points = [0] + pp

            perf_index = get_MMLR_perfection_power(n, r, pickup_points, one_round_SPECK_32, samples_num, max_rounds)
            if perf_index != -1:
                results.append((ppnum + 1, pickup_points, perf_index))
        
        # сотрируем результаты для МЛГ с задданым ppnum числом точек съема со всеми воможными расположениями точек съема по значению экспонента (от меньшего к большему)
        results = list(sorted(results, key=operator.itemgetter(2)))

        write_perf_index(
            f"./perf_index/MMLR_SPECK_samples_num_{samples_num}/r_{r}_n_{n}_ppnum_{ppnum + 1}.txt",
            results
        )
        progress_info(f"ppnum={ppnum + 1} done")


if __name__ == '__main__':

    p1_args_set = dict(
        r=32,
        n=8,
        ppnum_min=2,
        ppnum_max=8,
        max_rounds=25,
        pow=1
    )
    p1 = Process(target=research_mixing_props_MMLR_SPECK, kwargs=p1_args_set)

    p2_args_set = dict(
        r=32,
        n=8,
        ppnum_min=2,
        ppnum_max=8,
        max_rounds=25,
        cell=0
    )
    p2 = Process(target=research_local_mixing_props_MMLR_SPECK, kwargs=p2_args_set)

    p3_args_set = dict(
        r=32,
        n=8,
        ppnum_min=2,
        ppnum_max=8,
        samples_num=100,
        max_rounds=25
    )
    p3 = Process(target=research_perfection_props_MMLR_SPECK, kwargs=p3_args_set)

    p4_args_set = dict(
        r=32,
        n=8,
        ppnum_min=2,
        ppnum_max=8,
        max_rounds=25,
        pow=2
    )
    p4 = Process(target=research_mixing_props_MMLR_SPECK, kwargs=p4_args_set)

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    # research_mixing_props_MMLR_SPECK(
    #     r=32,
    #     n=8,
    #     ppnum_min=2,
    #     ppnum_max=8,
    #     max_rounds=25,
    #     pow=1
    # )
    # research_local_mixing_props_MMLR_SPECK(
    #     r=32,
    #     n=8,
    #     ppnum_min=2,
    #     ppnum_max=8,
    #     max_rounds=25,
    #     cell=0
    # )
    # research_perfection_props_MMLR_SPECK(
    #     r=32,
    #     n=8,
    #     ppnum_min=2,
    #     ppnum_max=8,
    #     samples_num=100,
    #     max_rounds=25
    # )
    # research_mixing_props_MMLR_SPECK(
    #     r=32,
    #     n=8,
    #     ppnum_min=2,
    #     ppnum_max=8,
    #     max_rounds=25,
    #     pow=2
    # )
