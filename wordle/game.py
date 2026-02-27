from random import choice
from enum import Enum

class LetterValidity(Enum):
	ExtraIncorrect = "extraincorrect"
	Incorrect = "incorrect"
	Exists = "exists"
	Correct = "correct"

with open("dictionary.txt", "r") as f:
	DICTIONARY = [x.strip() for x in f.readlines()]

def check_word(word: str, target: str) -> list[LetterValidity]:
	word_validity = []

	available_counts = { char:target.count(char) for char in word }
	existed = []

	for secret_char, guess_char in zip(target, word):
		if guess_char == secret_char:
			available_counts[guess_char] -= 1


	for secret_char, guess_char in zip(target, word):
		is_correct = secret_char == guess_char
		exists_in_secret = available_counts.get(guess_char, 0) > 0


		if is_correct:
			word_validity.append(LetterValidity.Correct)
			continue

		available_counts[guess_char] -= 1

		if not is_correct and exists_in_secret:
			existed.append(guess_char)
			word_validity.append(LetterValidity.Exists)
		elif guess_char in existed:
			word_validity.append(LetterValidity.ExtraIncorrect)
		else:
			word_validity.append(LetterValidity.Incorrect)

	return word_validity

# print(check_word("leech", "defer"))

class WordleGame:
	def __init__(self, max_guesses: int = 6, secret_word: str | None = None) -> None:
		self.max_guesses = max_guesses

		self.secret_word = secret_word or choice(DICTIONARY)
		self.guesses: list[tuple[str, list[LetterValidity]]] = []
	
	def make_guess(self, word: str) -> tuple[str, list[LetterValidity]]:
		info = (word, check_word(word, self.secret_word))
		self.guesses.append(info)

		return info