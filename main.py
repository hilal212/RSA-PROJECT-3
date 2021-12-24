import random

def powmod_sm(base, exponent, modular):
    bin_exponent = bin(exponent)
    result = 1
    for bit in bin_exponent:
        result = (result * result) % modular
        if bit == '1':
            result = (result * base) % modular
    return result


def mrt(value, num_tests):
    if value == 2 or value == 3:
        return True

    if value == 0 or value == 1 or value % 2 == 0:
        return False

    s = 0
    t = value - 1
    while t % 2 == 0:
        t //= 2
        s += 1

    for _ in range(num_tests - 1):
        a = random.randrange(2, value - 2)
        x = powmod_sm(a, t, value)

        if x == 1 or x == value - 1:
            continue

        is_pass_check = False
        for _ in range(s - 1):
            x = powmod_sm(x, 2, value)
            if x == 1:
                return False
            if x == value - 1:
                is_pass_check = True
                break

        if not is_pass_check:
            return False

    return True


def generate_random_prime(num_bits):
    while True:
        number = random.getrandbits(num_bits)

        if number % 2 == 0:
            number -= 1

        if mrt(number, 30):
            return number


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, coeff_a, coeff_b = gcd_extended(b % a, a)
    return gcd, coeff_b - (b // a) * coeff_a, coeff_a


def modular_inverse(base, modular):
    _, result, _ = gcd_extended(base, modular)
    return result % modular


def generate_keys_RSA(num_bits):
    #a
    p = generate_random_prime(num_bits)
    q = generate_random_prime(num_bits)

    #b
    n = p * q
    phi_n = (p - 1) * (q - 1)

    #c
    e = phi_n
    while gcd(e, phi_n) != 1:
        e = random.randrange(1, phi_n - 1)

    #d
    d = modular_inverse(e, phi_n)

    #e
    return n, e, d


def ASCII_to_number(text):
    number = 0
    for c in text:
        number = number * 256 + ord(c)
    return number


def number_to_ASCII(number):
    text = ""
    while number != 0:
        text += chr(number % 256)
        number //= 256
    return text[::-1]


def encrypt_RSA(text, key):
    n, e = key
    to_encrypt = ASCII_to_number(text)
    return powmod_sm(to_encrypt, e, n)


def decrypt_RSA(encrypted_text, key):
    n, d = key
    decrypted_number = powmod_sm(encrypted_text, d, n)
    decrypted_text = number_to_ASCII(decrypted_number)
    return decrypted_text


if __name__ == '__main__':
    NUM_BITS = 512

    n, e, d = generate_keys_RSA(NUM_BITS)

    text = "ABRACADABRA cadabara"
    encrypted = encrypt_RSA(text, (n, e))
    decrypted = decrypt_RSA(encrypted, (n, d))

    print("Text: ", text)
    print("Encrypted: ", encrypted)
    print("Decrypted: ", decrypted)
