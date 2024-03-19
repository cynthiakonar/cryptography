import math

T = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]


def F(X, Y, Z):
    return (X & Y) | (~X & Z)

def G(X, Y, Z):
    return (X & Z) | (Y & ~Z)

def H(X, Y, Z):
    return X ^ Y ^ Z

def I(X, Y, Z):
    return Y ^ (X | ~Z)

def left_rotate(x, n):
    return (x << n | x >> (32 - n)) & 0xFFFFFFFF


def md5(message):
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    def pad_message(message):
        original_length = len(message)

        print("\nMessage Length ", original_length)

        message += b'\x80'
        while len(message) % 64 != 56:
            message += b'\x00'
        message += original_length.to_bytes(8, byteorder='little')
        return message

    message = pad_message(message)
    chunks = [message[i:i + 64] for i in range(0, len(message), 64)]
    count = 0

    for chunk in chunks:
        count+=1
        print("\nBlock ", count)

        X = [int.from_bytes(chunk[i:i + 4], byteorder='little') for i in range(0, 64, 4)]
        a, b, c, d = A, B, C, D

        for i in range(16):
            a, b, c, d = (b + left_rotate((a + F(b, c, d) + X[i] + T[i]) & 0xFFFFFFFF, 7),
                          a, left_rotate(b, 27), c)
        print("Round 1: ",a,b,c,d)                  

        for i in range(16):
            a, b, c, d = (d + left_rotate((a + G(b, c, d) + X[(1 * i + 5) % 16] + T[16 + i]) & 0xFFFFFFFF, 12),
                          a, left_rotate(b, 22), c)
        print("Round 2: ",a,b,c,d) 

        for i in range(16):
            a, b, c, d = (c + left_rotate((a + H(b, c, d) + X[(5 * i + 1) % 16] + T[32 + i]) & 0xFFFFFFFF, 17),
                          a, left_rotate(b, 22), c)
        print("Round 3: ",a,b,c,d)                  

        for i in range(16):
            a, b, c, d = (b + left_rotate((a + I(b, c, d) + X[(7 * i) % 16] + T[48 + i]) & 0xFFFFFFFF, 22),
                          a, left_rotate(b, 22), c)
        print("Round 4: ",a,b,c,d)                   

        A = (a + A) & 0xFFFFFFFF
        B = (b + B) & 0xFFFFFFFF
        C = (c + C) & 0xFFFFFFFF
        D = (d + D) & 0xFFFFFFFF

    digest = A.to_bytes(4, byteorder='little') + B.to_bytes(4, byteorder='little') + C.to_bytes(4, byteorder='little') + D.to_bytes(4, byteorder='little')

    return digest.hex()


def main():
    message = input("Enter the message to hash: ").encode()
    hash_value = md5(message)
    print("\nMD5 hash:", hash_value)


if __name__== "__main__":
    main()
