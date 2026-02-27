from game import WordleGame, LetterValidity, DICTIONARY
from player import WordlePlayer
from regex import match
from random import choice
from time import sleep

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

	for index in range(len(word)):
		correct_char = correct.get(index)

		if correct_char != None:
			pattern += correct_char
			continue
		
		nobueno = incorrect

		for char in exists.get(index, []):
			nobueno += char
		
		pattern += f"[^{nobueno}]"

	return pattern

class WordleGuesser(WordlePlayer):
	def __init__(self, game: WordleGame) -> None:
		self.game = game
		self.available = DICTIONARY
	
	def choose_word(self) -> str:
		return choice(self.available)

	def make_guess(self):
		word = self.choose_word()
		info = self.game.make_guess(word)
		pattern = build_regex_pattern(*info)

		
		old_available = self.available
		new_available = [s for s in old_available if match(pattern, s)]

		initial_count = len(old_available)
		current_count = len(new_available)
		percentage = 1 - (current_count / initial_count)

		print(f"guessing {word}\npattern: {pattern}\ninitial #: {initial_count} ({old_available[0:5]})\nremaining #: {current_count} ({new_available[0:5]})\nreduction: {percentage * 100:.1f}% ({current_count-initial_count})")

		self.available = new_available

		return info