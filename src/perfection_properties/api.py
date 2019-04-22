from src.perfection_properties.perfection_check import get_GEN_class_perfection_power
from src.generators.mag import MAG
from src.generators.mmlr import MMLR
from src.algorythms.speck import enc_SPECK32_wt_key
from typing import List

class PerfectionCmdAPI:
    def calculate_perf_pow_for_MMLR_SPECK_api(
            self,
            r: int,
            n: int,
            pickup_points: List[int],
            max_rounds: int,
            samples_num: int
        ) -> None:
        """Расчет показателя совершенности для преобразования ММЛГ с модифицирующим преобразованием одно-раундовым SPECK и вывод на экран.
        Параметры:
            r:              размер ячейки ММЛГ в битах.
            n:              количество ячеек ММЛГ.
            pickup_points:  список точек съема, допустимый диапазон - 0 <= x < n.
            max_rounds:     максимальое число раундов, до которого искать экспонент.
            samples_num:    количество пар соседних векторов, на которых будет происходить проверка."""
        perf_pow = get_GEN_class_perfection_power(n, r, pickup_points, enc_SPECK32_wt_key, samples_num, max_rounds, MMLR)
        print(f'Показатель совершенности = {perf_pow}')
    
    def calculate_perf_pow_for_MAG_SPECK_api(
            self,
            r: int,
            n: int,
            pickup_points: List[int],
            max_rounds: int,
            samples_num: int
        ) -> None:
        """Расчет показателя совершенности для преобразования МАГ с модифицирующим преобразованием одно-раундовым SPECK и вывод на экран.
        Параметры:
            r:              размер ячейки ММЛГ в битах.
            n:              количество ячеек МАГ.
            pickup_points:  список точек съема, допустимый диапазон - 0 <= x < n.
            max_rounds:     максимальое число раундов, до которого искать экспонент.
            samples_num:    количество пар соседних векторов, на которых будет происходить проверка."""
        perf_pow = get_GEN_class_perfection_power(n, r, pickup_points, enc_SPECK32_wt_key, samples_num, max_rounds, MAG)
        print(f'Показатель совершенности = {perf_pow}')