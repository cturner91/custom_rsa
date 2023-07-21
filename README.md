# custom_rsa

A custom basic implementation of the RSA encryption algorithm.

## Disclaimer

This was just for fun, and for use as an example of how RSA works. Only a fool would use this implementation for any real security purposes.

## Why?

I was just curious, and interested in how it worked. Did some research, aided by ChatGPT, and managed to get something working.

The implementation here is designed to show that we can encrypt a message with one component, and decrypt it with a totally different component and still reach the original message. The decryption component clearly does not have access to the same information as the encryption component, yet it can still decrypt the message.

## How to use

If an existing RSA triplet is known, then the `Encrypter` and `Decrypter` classes can be used directly. As an example:

```python
public, private, modulo = 163, 427, 527
message = 'Testing RSA - message'
encrypted = Encrypter(public, modulo).encrypt(message)
encrypted
[424,33,21,401,24,291,392,94,452,383,265,94,267,94,473,33,21,21,295,392,33]

decrypted = Decrypter(private, modulo).decrypt(encrypted)
decrypted
'Testing RSA - message'
```

If an existing RSA triplet it not known, one can be generated using the RSA class like so:

```python
rsa = RSA(<prime1>, <prime2>)
private, public, modulo = rsa.get_keys()
```

## How it works

(For people new to the topic, please recognise the difference between **encoding** and **encrypting**. Encoding means translating the string into a numeric representation in an easily reversible manner. There is usually some logical order to the encoded values e.g. the encoding of 'B' will be one more than the encoding of 'A'. **Encryption** is the obfuscation of the data such that it is unintelligible to anyone without the associated **decryption** information.)

1. The user's message is encoded from a string into a list of integers. If the user provides a `charmap` input, then that is used to encode the string. Otherwise, Python's in-built `ord()` function is used.
2. The encoded values are then transformed using the RSA **public** key. The transform is given by the formula: `<encoded value> ** public_key % modulo`.
3. The encrypted values can then be transmitted safely, knowing that no-one without the decryption spec can make sense of the data.
4. Once received, then encrypted values can be decrypted using the **private** key. The transform is given by the formula: `<encrypted value> ** private_key % modulo`. The result of this is an _encoded_ string.
5. The encoded string and then be simply decoded to return the original message.

## Real-world applications

RSA is everywhere. You are probably reading this via a `https` connection right now. The 's' in 'https' means 'secure', which indicates that the data transmitted has been encrypted for transit - almost always with RSA encryption.

RSA is an **asymmetric** encryption algorithm, meaning that the sender and the reader do not need to have the same information to ensure secure transit of the payload. This means that we do not need to worry about how to securely share the decryption key which, if mishandled, could lead to the entire payload being intercepted.

In internet communication, RSA is applied during the TLS handshake. A server can share its public key and modulo with anyone, and so long as its private key remains unknown, its communications will remain secure.

### Can't it be hacked?

The algorithm shows that the RSA triplet is worked out by multiplying two prime numbers. This process is very easy to perform this way round, but incredibly difficult to reverse-engineer. RSA in production environments will also typically use two incredibly large prime numbers - around 100 digits long. This is what keeps the RSA method secure. 

My little code example would break long before any such large numbers could be implemented.
