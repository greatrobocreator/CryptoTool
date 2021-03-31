class Analyser:

    options = []

    def analyze(self, text):
        pass


class FrequencyAnalyzer(Analyser):

    options = []

    def analyze(self, text):
        alphabet = [chr(i + 65) for i in range(26)] + [chr(i + 97) for i in range(26)]
        frequency = [0] * 26
        count = 0

        for c in text:
            if c in alphabet:
                frequency[ord(c) - (65 if c.isupper() else 97)] += 1
                count += 1

        for i in range(len(frequency)):
            frequency[i] /= count

        return [chr(i + 65) for i in range(26)], frequency
