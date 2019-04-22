# Speck32/64
# Key:        1918 1110 0908 0100
# Plaintext:  6574 694c
# Ciphertext: a868 42f2

def enc_SPECK32_wt_key(plaintext, r=1):
    """Преобразование r-раундового алгоритма SPECK над блоком длины 32 бит."""
    if r < 1:
        raise Exception("Количество раундов шифрования не может быть меньше 1")
    
    word_size = 16
    mod_mask = (2 ** word_size) - 1
    beta_shift = 2
    alpha_shift = 7

    processtext = plaintext

    for _ in range(r):

        x = (processtext >> word_size) & mod_mask
        y = processtext & mod_mask

        rs_x = ((x << (word_size - alpha_shift)) + (x >> alpha_shift)) & mod_mask

        add_sxy = (rs_x + y) & mod_mask

        new_x = add_sxy # ^ k

        ls_y = ((y >> (word_size - beta_shift)) + (y << beta_shift)) & mod_mask

        new_y = new_x ^ ls_y

        processtext = (new_x << word_size) + new_y

    return processtext



def one_round_SPECK_32(plaintext, k=0):

    word_size = 16
    mod_mask = (2 ** word_size) - 1
    beta_shift = 2
    alpha_shift = 7

    x = (plaintext >> word_size) & mod_mask
    y = plaintext & mod_mask

    rs_x = ((x << (word_size - alpha_shift)) + (x >> alpha_shift)) & mod_mask

    add_sxy = (rs_x + y) & mod_mask

    new_x = k ^ add_sxy

    ls_y = ((y >> (word_size - beta_shift)) + (y << beta_shift)) & mod_mask

    new_y = new_x ^ ls_y

    ciphertext = (new_x << word_size) + new_y

    return ciphertext
