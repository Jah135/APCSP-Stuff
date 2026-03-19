from random import choice
from enum import Enum

with open("dictionary.txt", "r") as _dict:
	DICTIONARY = [x.strip() for x in _dict.readlines()]

class LetterValidity(Enum):
	TooMany = "toomany"
	Incorrect = "incorrect"
	Exists = "exists"
	Correct = "correct"

	def __repr__(self) -> str:
		return self.name

def check_word(guess: str, secret: str) -> list[LetterValidity]:
	available_counts = { char:secret.count(char) for char in guess }
	exists = {}

	for secret_char, guess_char in zip(secret, guess):
		if guess_char == secret_char:
			available_counts[guess_char] -= 1
		if guess_char in secret:
			exists[guess_char] = True
	
	word_validity = []

	for secret_char, guess_char in zip(secret, guess):
		is_correct = secret_char == guess_char
		exists_in_secret = available_counts.get(guess_char, 0) > 0

		if is_correct:
			word_validity.append(LetterValidity.Correct)
			continue

		available_counts[guess_char] -= 1

		if not is_correct and exists_in_secret:
			word_validity.append(LetterValidity.Exists)
		else:
			word_validity.append(LetterValidity.Incorrect if exists.get(guess_char, False) == False else LetterValidity.TooMany)

	return word_validity

class WordleGame:
	def __init__(self, max_guesses: int = 6, secret_word: str | None = None) -> None:
		self.max_guesses = max_guesses
		self.guesses: list[tuple[str, list[LetterValidity]]] = []
		self.is_over = False
		self.is_won = False

		self.secret_word = secret_word or choice(DICTIONARY)

	def make_guess(self, word: str) -> tuple[str, list[LetterValidity]]:
		info = (word, check_word(word, self.secret_word))
		self.guesses.append(info)

		self.is_over = (word == self.secret_word) or (len(self.guesses) >= self.max_guesses)
		self.is_won = word == self.secret_word

		return info
	
	def reset(self):
		self.is_over = False
		self.is_won = False
		self.guesses.clear()