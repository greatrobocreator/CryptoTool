class Analyser:
    options = []

    def analyze(self, text):
        pass


class FrequencyAnalyzer(Analyser):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    options = []

    def analyze(self, text):
        frequency = [0] * 26
        count = 0

        for c in text:
            if c in self.alphabet:
                frequency[ord(c) - (65 if c.isupper() else 97)] += 1
                count += 1

        if count != 0:
            for i in range(len(frequency)):
                frequency[i] /= count

        return [chr(i + 65) for i in range(26)], frequency


class CoincidenceIndexAnalyzer(Analyser):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    options = []

    @staticmethod
    def _coincidence_index(text):
        frequency = FrequencyAnalyzer().analyze(text)[1]
        return sum([x ** 2 for x in frequency])

    def analyze(self, text):

        text_len = sum(x in self.alphabet for x in text)

        indexes = []

        for key_len in range(1, text_len // 10):

            mean = 0
            for i in range(key_len):
                mean += self._coincidence_index(text[i::key_len])
            mean /= key_len

            indexes.append(mean)

        return list(range(1, text_len // 10)), indexes
