import numpy as np
from utils import cast_matrix_to_identity_format, write_matrix
from mixing_matrixes import construct_mixing_matrix_MMLR, construct_mixing_matrix_SPECK, construct_mixing_matrix_pow_SPECK
from mixing_props import get_exponent

np.set_printoptions(threshold=np.nan, linewidth=np.nan)

m = construct_mixing_matrix_MMLR(32, 8, [0,7], construct_mixing_matrix_SPECK(32))

# m = construct_mixing_matrix_SPECK(32)

# pow = 4
# m = construct_mixing_matrix_pow_SPECK(pow, 32)

# m = np.eye(32, dtype=np.int)

write_matrix(f'./matrixes/MMLR_SPECK_r_32_n_8_pp_0_7.txt',m)

print(get_exponent(m, 30))

# print(get_exponent(m, 25))
