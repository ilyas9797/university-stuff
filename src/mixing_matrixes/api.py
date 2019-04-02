from typing import List

from src.mixing_matrixes.matrixes_generation import (construct_matrix_MMLR,
                                                     construct_matrix_SPECK,
                                                     construct_mixing_matrix_pow_SPECK)
from src.mixing_matrixes.utils import write_matrix_pretty


class MixingMatrixesCmdAPI:

    def construct_matrix_MMLR_with_SPECK_api(self, r: int, n: int, pickup_points: List[int], filename: str) -> None:
        """Построение перемешивающей матрицы ММЛГ с модифицирующим преобразованием SPECK и запись ее в файл.
        Параметры:
            r:              размер ячейки ММЛГ в битах.
            n:              количество ячеек ММЛГ.
            pickup_points:  список точек съема, допустимый диапазон - 0 <= x < n.
            filename:       имя файла для записи матрицы.
        """
        mt_matrix = construct_matrix_SPECK(r)
        matrix = construct_matrix_MMLR(r, n, pickup_points, mt_matrix)
        write_matrix_pretty(filename, matrix)
