from modules.dictionary import DICTIONARY

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
MAX_LENGTH = max(len(word) for word in DICTIONARY)

frequencies = {c: sum(word.count(c) for word in DICTIONARY) for c in ALPHABET}
frequencies_per_positions = [
    {c: sum(1 for word in DICTIONARY if word[index] == c) for c in ALPHABET}
    for index in range(MAX_LENGTH)
]

for index in range(MAX_LENGTH):
    letter, freq = max(frequencies_per_positions[index].items(), key=lambda x: x[1])
    print(index, letter, freq)
