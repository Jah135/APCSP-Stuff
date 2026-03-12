from game import WordleGame, LetterValidity, DICTIONARY
from player import WordlePlayer
from regex import match
from random import choice

def build_regex_pattern(word: str, word_validity: list[LetterValidity]) -> str:
	incorrect = ""
	correct: dict[int, str] = {}
	exists: dict[int, list[str]] = {}

	for index, info in enumerate(zip(word, word_validity)):
		char, validity = info

		if validity == LetterValidity.Correct:
			correct[index] = char
		elif validity == LetterValidity.Exists or validity == LetterValidity.OnlyOne:
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

	def prompt_guess(self):
		word = self.choose_word()
		info = self.game.make_guess(word)

		pattern = build_regex_pattern(*info)
		
		old_available = self.available
		new_available = [s for s in old_available if match(pattern, s)]

		initial_count = len(old_available)
		current_count = len(new_available)
		percentage = 1 - (current_count / initial_count)

		# print(f"initial #: {initial_count}")
		# print(f"current #: {current_count}")
		# print(f"reduction: {percentage*100:.2f}% ({current_count - initial_count})")
		# print(f"guessed word: {word}")
		# print(f"feedback: {info[1]}")
		# print(f"pattern: {pattern}")

		self.available = new_available

		return info