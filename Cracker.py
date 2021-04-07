from Analyzer import FrequencyAnalyzer


class Cracker:
    options = []
    output_options = []

    def crack(self, text):
        pass


class CesarCracker(Cracker):
    output_options = [
        ("offset", "number")
    ]

    true_frequency = [0.082, 0.015, 0.028, 0.043, 0.13, 0.022, 0.02, 0.061,
                      0.07, 0.0015, 0.0077, 0.04, 0.024, 0.067, 0.075, 0.019,
                      0.00095, 0.06, 0.063, 0.091, 0.028, 0.0098, 0.024,
                      0.0015, 0.02, 0.00074]

    @staticmethod
    def _mse(a, b):
        error = 0
        for i in range(min(len(a), len(b))):
            error += (a[i] - b[i]) ** 2

        return error

    def crack(self, text):
        frequency = FrequencyAnalyzer().analyze(text)[1]

        min_error = float('inf')
        offset = -1
        for i in range(26):
            error = self._mse(self.true_frequency,
                              frequency[i:] + frequency[:i])
            if error < min_error:
                min_error = error
                offset = i

        return offset,


class VigenereCracker(Cracker):
    options = [
        ('language', 'combobox', ('English', 'Russian', 'Rus'))
    ]

    output_options = [
        ('possible_keys', 'multiline')
    ]

    true_index = {
        "English": 0.0644,
        "Russian": 0.0553
    }

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def __init__(self):
        self.language = 'English'

    @staticmethod
    def _coincidence_index(text):
        frequency = FrequencyAnalyzer().analyze(text)[1]
        return sum([x ** 2 for x in frequency])

    def crack(self, text):

        text_len = sum(x in self.alphabet for x in text)

        ma = []
        key_lens = []
        for key_len in range(1, text_len // 10):

            mean = 0
            for i in range(key_len):
                mean += self._coincidence_index(text[i::key_len])
            mean /= key_len

            print(key_len, ':', mean)

            if len(ma) != 0 and mean > 1.25 * (sum(ma) / len(ma)):
                key_lens.append(key_len)

            ma.append(mean)
            if len(key_lens) != 0:
                ma = ma[1:]

        if len(key_lens) == 0:
            return 'Error!',

        cesar_cracker = CesarCracker()

        keys = ''
        for key_len in key_lens:
            key = ''
            for i in range(key_len):
                key += chr(cesar_cracker.crack(text[i::key_len])[0] + 65)
            keys += key + '\n'

        return keys,
