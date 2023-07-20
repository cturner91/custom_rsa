import json
import random


class RSA:
    # https://justcryptography.com/rsa-key-pairs/
    # The RSA algorithm to generate the key pairs is as follows:
    # Choose p, q, two prime numbers
    # Calculate n = pq
    # Calculate f(n) = (p-1)(q-1)
    # Chose e such that gcd(f(n), e) = 1; 1 < e < f (n), and
    # Chose d, such that ed mod f(n) = 1
    
    def __init__(self, prime1, prime2):
        # choose any two primes
        # don't choose massive ones - could easily OOM
        if not self._is_prime(prime1):
            raise ValueError(f'{prime1} is not prime')
        elif not self._is_prime(prime2):
            raise ValueError(f'{prime2} is not prime')

        self.prime1 = prime1
        self.prime2 = prime2
        
        self._calculate_viable_pairs()

    @staticmethod
    def _gcd(a, b):
        # greatest common divisor (via ChatGPT)
        while b != 0:
            a, b = b, a % b
        return a
    
    @staticmethod
    def _is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    
    def _calculate_viable_pairs(self):

        self.n = self.prime1 * self.prime2
        fn = (self.prime1 - 1) * (self.prime2 - 1)
        es = [x for x in range(2, fn) if self._gcd(fn, x) == 1]
        ds = {}
        for e in es:
            ds[e] = [d for d in range(1, fn+1) if e != d and e*d % fn == 1]
        self._ds = {e: ds[e][0] for e in ds if len(ds[e]) == 1}
        
    def get_keys(self, i=None):
        keys = list(self._ds.keys())
        
        if i is None:
            # choose at random
            public = random.choice(keys)
        else:
            public = keys[i]

        private = self._ds[public]
        
        return private, public, self.n


class Encoder:
    
    def __init__(self, charmap=None):
        self.file_path = './file.txt'
        self.charmap = charmap
        
    def encode(self, message):
        if self.charmap is None:
            return [ord(char) for char in list(message)]
        else:
            return [self.charmap.index(char) for char in list(message)]
    
    def decode(self, encoded):
        if self.charmap is None:
            decoded = [chr(val) for val in encoded]
        else:
            decoded = [self.charmap[val] for val in encoded]

        return "".join(decoded)

    # all steps of our data should be json serialisable    
    def write_to_file(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data))
        return True

    def load_from_file(self):
        with open(self.file_path, encoding='utf-8') as f:
            return json.loads(f.read())


class Encrypter(Encoder):
    
    def __init__(self, public_key, modulo, charmap=None):
        self.public_key = public_key
        self.modulo = modulo
        self.charmap = charmap

    def encrypt(self, message):
        encoded_message = self.encode(message)
        return [num ** self.public_key % self.modulo for num in encoded_message]


class Decrypter(Encoder):
    
    def __init__(self, private_key, modulo, charmap=None):
        self.private_key = private_key
        self.modulo = modulo
        self.charmap = charmap

    def decrypt(self, encoded_message):
        decrypted_message = [num ** self.private_key % self.modulo for num in encoded_message]
        return self.decode(decrypted_message)


#%% Usage

if __name__ == '__main__':

    rsa = RSA(17, 31)
    private, public, modulo = rsa.get_keys()
    
    message = 'Testing message...'
    encrypted = Encrypter(public, modulo).encrypt(message)
    decrypted = Decrypter(private, modulo).decrypt(encrypted)

    print(message)
    print(encrypted)
    print(decrypted)
