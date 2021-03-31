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

    def __init__(self):
        self.offset = 4

    def encrypt(self, text):
        alphabet = [chr(i + 65) for i in range(26)] + [chr(i + 97) for i in range(26)]
        self.offset = ((self.offset % 26) + 26) % 26
        encrypted = ""
        for c in text:
            if c in alphabet:
                i = (65 if c.isupper() else 97)
                c = chr((ord(c) - i + self.offset) % 26 + i)
            encrypted += c

        return encrypted

    def decrypt(self, text):
        self.offset *= -1
        decrypted = self.encrypt(text)
        self.offset *= -1
        return decrypted


