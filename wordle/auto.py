from game import WordleGame, LetterValidity, DICTIONARY
from regex import match
from random import choice

GAME = WordleGame(10)

def build_regex_pattern(word: str, word_validity: list[LetterValidity]) -> str:
	incorrect = ""
	correct: dict[int, str] = {}
	exists: dict[int, list[str]] = {}

	for index, info in enumerate(zip(word, word_validity)):
		char, validity = info

		if validity == LetterValidity.Correct:
			correct[index] = char
		elif validity == LetterValidity.Exists or validity == LetterValidity.ExtraIncorrect:
			chars = exists.get(index, [])

			if char not in chars:
				chars.append(char)

			exists[index] = chars

		elif validity == LetterValidity.Incorrect and char not in incorrect:
			incorrect += char
	
	pattern = ""

	for index in range(len(GAME.secret_word)):
		correct_char = correct.get(index)

		if correct_char != None:
			pattern += correct_char
			continue
		
		nobueno = incorrect

		for char in exists.get(index, []):
			nobueno += char
		
		pattern += f"[^{nobueno}]"

	return pattern

class Guesser:
	def __init__(self, game: WordleGame) -> None:
		self.game = game
		self.choices = DICTIONARY
	
	def make_guess(self):
		word = choice(self.choices)
		pattern = build_regex_pattern(*self.game.make_guess(word))

		initial_count = len(self.choices)

		# print(self.game.secret_word in self.choices, self.game.secret_word, pattern)
		self.choices = [s for s in self.choices if match(pattern, s)]

		secret_exists = self.game.secret_word in self.choices
		
		current_count = len(self.choices)
		percentage = 1 - (current_count / initial_count)

		print(f"guessing {word}\npattern: {pattern}\ninitial #: {initial_count}\nremaining #: {current_count}\nreduction: {percentage * 100:.1f}%\n\nvalid: {secret_exists}\ntarget: {self.game.secret_word}")

		return word