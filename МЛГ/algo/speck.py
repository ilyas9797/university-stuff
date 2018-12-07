# SPECK 128, KEY 128
# #include <stdint.h>

# #define ROR(x, r) ((x >> r) | (x << (64 - r)))
# #define ROL(x, r) ((x << r) | (x >> (64 - r)))
# #define R(x, y, k) (x = ROR(x, 8), x += y, x ^= k, y = ROL(y, 3), y ^= x)
# #define ROUNDS 32

# void encrypt(uint64_t const pt[static 2],
#              uint64_t ct[static 2],
#              uint64_t const K[static 2])
# {
#    uint64_t y = pt[0], x = pt[1], b = K[0], a = K[1];

#    R(x, y, b);
#    for (int i = 0; i < ROUNDS - 1; i++) {
#       R(a, b, i);
#       R(x, y, b);
#    }

#    ct[0] = y;
#    ct[1] = x;
# }



# SPECK Семен
# #define ROR(x, r) ((x >> r) | (x << (8 - r))) 
# #define ROL(x, r) ((x << r) | (x >> (8 - r))) 
# #define R(x, y) (x = ROR(x, 2), x += y, y = ROL(y, 1), y ^= x) 

# unsigned short speck_2_steps(unsigned short plain) 
# { 
# unsigned char left = plain » 8, right = plain; 
# for (int i = 0; i < 2; i++) 
# R(left, right); 
# return (left « 8) | right; 
# }


def rol(n: int, x: int, shift: int):
    return 


def speck32_64_round(x: int):
    pass
    
