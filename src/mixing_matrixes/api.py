from typing import List

from src.mixing_matrixes.matrixes_generation import (construct_matrix_MMLR,
                                                     construct_matrix_MAG,
                                                     construct_mixing_matrix_pow_SPECK)
from src.mixing_matrixes.utils import write_matrix_pretty
from src.mixing_matrixes.mixing_properties import (get_exponent,
                                                   get_local_exponent)


class MixingMatrixesCmdAPI:

    def consruct_matrix_pow_SPECK_api(
            self,
            r: int,
            power: int,
            filename: str) -> None:
        """Построение перемешивающей матрицы SPECK и запись ее в файл.
        Параметры:
            r:              размер блока SPECK в битах.
            pow:            степень преобразования SPECK.
            filename:       имя файла для записи матрицы.
        """
        matrix = construct_mixing_matrix_pow_SPECK(power, r)
        write_matrix_pretty(filename, matrix) 

    def consruct_matrix_MMLR_with_pow_SPECK_api(
            self,
            r: int,
            n: int,
            pickup_points: List[int],
            power: int,
            filename: str) -> None:
        """Построение перемешивающей матрицы ММЛГ с модифицирующим преобразованием power-раундовым SPECK и запись ее в файл.
        Параметры:
            r:              размер ячейки ММЛГ в битах.
            n:              количество ячеек ММЛГ.
            pickup_points:  список точек съема, допустимый диапазон - 0 <= x < n.
            pow:            степень преобразования SPECK.
            filename:       имя файла для записи матрицы.
        """
        mt_matrix = construct_mixing_matrix_pow_SPECK(power, r)
        matrix = construct_matrix_MMLR(r, n, pickup_points, mt_matrix)
        write_matrix_pretty(filename, matrix)
    
    def consruct_matrix_MAG_with_pow_SPECK_api(
            self,
            r: int,
            n: int,
            pickup_points: List[int],
            power: int,
            filename: str) -> None:
        """Построение перемешивающей матрицы МАГ с модифицирующим преобразованием power-раундовым SPECK и запись ее в файл.
        Параметры:
            r:              размер ячейки МАГ в битах.
            n:              количество ячеек МАГ.
            pickup_points:  список точек съема, допустимый диапазон - 0 <= x < n.
            pow:            степень преобразования SPECK.
            filename:       имя файла для записи матрицы.
        """
        mt_matrix = construct_mixing_matrix_pow_SPECK(power, r)
        matrix = construct_matrix_MAG(r, n, pickup_points, mt_matrix)
        write_matrix_pretty(filename, matrix)

    def calculate_exponent_for_MMLR_with_pow_SPECK_api(
            self,
            r: int,
            n: int,
            pickup_points: List[int],
            power: int,
            max_rounds: int) -> None:
        """Расчет экспонента для перемешивающей матрицы ММЛГ с модифицирующим преобразованием power-раундовым SPECK и вывод на экран.
        Параметры:
            r:              размер ячейки ММЛГ в битах.
            n:              количество ячеек ММЛГ.
            pickup_points:  список точек съема, допустимый диапазон - 0 <= x < n.
            pow:            степень преобразования SPECK.
            max_rounds:     максимальое число раундов, до которого искать экспонент."""
        mt_matrix = construct_mixing_matrix_pow_SPECK(power, r)
        matrix = construct_matrix_MMLR(r, n, pickup_points, mt_matrix)
        exp = get_exponent(matrix, max_rounds)
        print(f'Экспонент = {exp}')

    def calculate_local_exponent_for_MMLR_with_pow_SPECK_api(
            self,
            r: int,
            n: int,
            pickup_points: List[int],
            power: int,
            max_rounds: int,
            local_start: int,
            local_end: int) -> None:
        """Расчет локального экспонента для перемешивающей матрицы ММЛГ с модифицирующим преобразованием power-раундовым SPECK и вывод на экран.
        Параметры:
            r:              размер ячейки ММЛГ в битах.
            n:              количество ячеек ММЛГ.
            pickup_points:  список точек съема, допустимый диапазон - 0 <= x < n.
            pow:            степень преобразования SPECK.
            max_rounds:     максимальое число раундов, до которого искать экспонент.
            local_start:    позиция начального столбца.
            local_end:      позиция конечного столбца."""
        mt_matrix = construct_mixing_matrix_pow_SPECK(power, r)
        matrix = construct_matrix_MMLR(r, n, pickup_points, mt_matrix)
        exp = get_local_exponent(matrix, max_rounds, local_start, local_end)
        print(f'Локальный экспонент = {exp}')

    def calculate_exponent_for_MAG_with_pow_SPECK_api(
            self,
            r: int,
            n: int,
            pickup_points: List[int],
            power: int,
            max_rounds: int) -> None:
        """Расчет экспонента для перемешивающей матрицы МАГ с модифицирующим преобразованием power-раундовым SPECK и вывод на экран.
        Параметры:
            r:              размер ячейки МАГ в битах.
            n:              количество ячеек МАГ.
            pickup_points:  список точек съема, допустимый диапазон - 0 <= x < n.
            pow:            степень преобразования SPECK.
            max_rounds:     максимальое число раундов, до которого искать экспонент."""
        mt_matrix = construct_mixing_matrix_pow_SPECK(power, r)
        matrix = construct_matrix_MAG(r, n, pickup_points, mt_matrix)
        exp = get_exponent(matrix, max_rounds)
        print(f'Экспонент = {exp}')

    def calculate_local_exponent_for_MAG_with_pow_SPECK_api(
            self,
            r: int,
            n: int,
            pickup_points: List[int],
            power: int,
            max_rounds: int,
            local_start: int,
            local_end: int) -> None:
        """Расчет локального экспонента для перемешивающей матрицы МАГ с модифицирующим преобразованием power-раундовым SPECK и вывод на экран.
        Параметры:
            r:              размер ячейки МАГ в битах.
            n:              количество ячеек МАГ.
            pickup_points:  список точек съема, допустимый диапазон - 0 <= x < n.
            pow:            степень преобразования SPECK.
            max_rounds:     максимальое число раундов, до которого искать экспонент.
            local_start:    позиция начального столбца.
            local_end:      позиция конечного столбца."""
        mt_matrix = construct_mixing_matrix_pow_SPECK(power, r)
        matrix = construct_matrix_MAG(r, n, pickup_points, mt_matrix)
        exp = get_local_exponent(matrix, max_rounds, local_start, local_end)
        print(f'Локальный экспонент = {exp}')
