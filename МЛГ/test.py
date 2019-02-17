import numpy as np
from utils import cast_matrix_to_identity_format, write_matrix
from mixing_matrixes import construct_mixing_matrix_MMLR, construct_mixing_matrix_SPECK, construct_mixing_matrix_pow_SPECK, change_column_order
from mixing_props import get_exponent

np.set_printoptions(threshold=np.nan, linewidth=np.nan)

m = construct_mixing_matrix_MMLR(32, 8, [0,7], construct_mixing_matrix_SPECK(32))

# m = construct_mixing_matrix_SPECK(32)

# pow = 1
# m = construct_mixing_matrix_pow_SPECK(pow, 32)


write_matrix(f'./matrixes/MMLR_SPECK_r_32_n_8_pp_0_7.txt', m)

print(get_exponent(m, 30))

# print(get_exponent(m, 25))
# size = 32
# half_size = size // 2
# alpha = 7

# right_alpha_shift = np.zeros((half_size, half_size), dtype=np.int)
# for i in range(half_size):
#     right_alpha_shift[i, (-(i + 1) + alpha + half_size) % half_size] = 1

# triangular = np.zeros((half_size, half_size), dtype=np.int)
# for i in range(half_size):
#     for j in range(half_size - i):
#         triangular[i, j] = 1

# bottom_left = bottom_right = (change_column_order(right_alpha_shift) @ change_column_order(triangular))
# write_matrix(f'./matrixes/right_alpha_shift_r_32.txt', right_alpha_shift)
# write_matrix(f'./matrixes/triangular_r_32.txt', triangular)
# write_matrix(f'./matrixes/SPECK_r_32_bottom_left.txt', bottom_left)