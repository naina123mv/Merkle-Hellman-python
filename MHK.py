from random import randint
from gmpy2 import invert

b = []
w = []
q = 0
r = 0
MAX_CHARS = 150
BINARY_LENGTH = MAX_CHARS * 8

class MHK_Crypto_w_Arrays:
    
    def __init__(self):
        self.genKeys()

    def genKeys(self):
        global w, b, q, r
        maxBits = 50

        w.append(randint(1, 2**maxBits))
        sum = w[0]
        for i in range(1, BINARY_LENGTH):
            w.append(sum + randint(1, 2**maxBits))
            sum += w[i]

        q = sum + randint(1, 2**maxBits)
        r = q - 1
        for i in range(BINARY_LENGTH):
            b.append((w[i]*r)%q)

    def encryptMsg(self, message):
        global w, b, q, r
        if len(message) > MAX_CHARS:
            raise Exception("Maximum message length allowed is " + MAX_CHARS + ".")
        if len(message) <= 0:
            raise Exception("Cannot encrypt an empty string.")

        msgBinary = ''.join('{:08b}'.format(b) for b in message.encode('utf8'))
        print(msgBinary)

        if len(msgBinary) < BINARY_LENGTH:
            msgBinary = msgBinary.zfill(BINARY_LENGTH)

        result = 0
        for i in range(len(msgBinary)):
            result += b[i]*int(msgBinary[i], 2)

        return str(result)

    def decryptMsg(self, ciphertext):
        global w, b, q, r
        tmp = int(ciphertext)%q*invert(r,q)%q
        decrypted_binary = ''

        for i in range(len(w)-1,-1,-1):
            if w[i] <= tmp:
                tmp -= w[i]
                decrypted_binary += '1'
            else:
                decrypted_binary += '0'

        return int(decrypted_binary[::-1], 2).to_bytes((len(decrypted_binary) + 7) // 8, 'big').decode()

if __name__ == "__main__":
    crypto = MHK_Crypto_w_Arrays()
    print("Public and private keys have been generated.\n")
    while True:
        print("Enter a string and I will encrypt it as single large integer:")
        message = input()
        if len(message) > MAX_CHARS:
            print("\nYour message should have at most " + MAX_CHARS + "characters! Please try again.\n\n")
        elif len(message) <= 0:
            print("\nYou message should not be empty! Please try again.\n\n")
        else:
            break

    print("\nClear text:")
    print(message)
    print("\nNumber of clear text bytes = " + str(len(message)))

    encrypted = crypto.encryptMsg(message)
    print("\n\"" + message + "\"" + " is encrypted as:")
    print(encrypted)

    print("\nResult of decryption:")
    print(crypto.decryptMsg(encrypted))
