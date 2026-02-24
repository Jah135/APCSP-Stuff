from random import choice
from enum import Enum

class LetterValidity(Enum):
	Incorrect = "Incorrect"
	Exists = "Exists"
	Correct = "Correct"

with open("dictionary.txt", "r") as f:
	DICTIONARY = [x.strip() for x in f.readlines()]

def check_word(word: str, target: str) -> list[LetterValidity]:
	word_validity = []

	available_counts = { char:target.count(char) for char in word }

	for secret_char, guess_char in zip(target, word):
		if guess_char == secret_char:
			available_counts[guess_char] -= 1

	for secret_char, guess_char in zip(target, word):
		is_correct = secret_char == guess_char
		exists_in_secret = available_counts.get(guess_char, 0) > 0

		available_counts[guess_char] -= 1

		if is_correct:
			word_validity.append(LetterValidity.Correct)
		elif not is_correct and exists_in_secret:
			word_validity.append(LetterValidity.Exists)
		else:
			word_validity.append(LetterValidity.Incorrect)

	return word_validity

class WordleGame:
	def __init__(self, max_guesses: int) -> None:
		self.max_guesses = max_guesses

		self.secret_word = choice(DICTIONARY)
		self.guesses = []
	
	def make_guess(self, word: str) -> list[LetterValidity]:
		self.guesses.append(word)

		return check_word(word, self.secret_word)