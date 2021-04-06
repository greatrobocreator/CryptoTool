class Cypher:
    options = []

    def encrypt(self, text):
        pass

    def decrypt(self, text):
        pass


class CesarCypher(Cypher):
    options = [
        ("offset", "number")
    ]

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def __init__(self):
        self.offset = 4

    def encrypt(self, text):
        self.offset = ((self.offset % 26) + 26) % 26
        encrypted = ""
        for c in text:
            if c in self.alphabet:
                i = (65 if c.isupper() else 97)
                c = chr((ord(c) - i + self.offset) % 26 + i)
            encrypted += c

        return encrypted

    def decrypt(self, text):
        self.offset *= -1
        decrypted = self.encrypt(text)
        self.offset *= -1
        return decrypted


class VigenereCypher(Cypher):
    options = [
        ("key", "text")
    ]

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def __init__(self):
        self.key = "ABCD"

    @staticmethod
    def _ord(c):
        return ord(c) - (65 if c.isupper() else 97)

    @staticmethod
    def _chr(i, c):
        return chr(i + (65 if c.isupper() else 97))

    def encrypt(self, text):
        encrypted = ""
        self.key = self.key.upper()
        for i, c in enumerate(text):
            if c in self.alphabet:
                c = self._chr((self._ord(c) +
                               self._ord(self.key[i % len(self.key)])) % 26, c)
            encrypted += c

        return encrypted

    def decrypt(self, text):
        decrypted = ""
        self.key = self.key.upper()
        for i, c in enumerate(text):
            if c in self.alphabet:
                c = self._chr((self._ord(c) -
                               self._ord(self.key[i % len(self.key)])) % 26, c)
            decrypted += c

        return decrypted
