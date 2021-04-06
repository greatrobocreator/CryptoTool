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
