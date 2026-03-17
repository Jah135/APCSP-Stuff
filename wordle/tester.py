from wordle.game import WordleGame
from wordle.modules.auto import WordleGuesser

def run_one_test(game: WordleGame) -> tuple[bool, str, list[str]]:
	target_word = game.secret_word

	guesser = WordleGuesser(game)

	guessed_words = []
	did_win = False

	while not game.is_over:
		guess, _ = guesser.make_guess()
		did_win = guess == target_word
		guessed_words.append(guess)

	info = (did_win, target_word, guessed_words)

	game.reset()

	return info

test_game = WordleGame()

data: list[tuple[bool, str, list[str]]] = []
num_trials_per_word = 500
words_to_test = ["jazzy", "horse", "zucco", "stand", "abash"]

for word in words_to_test:
	test_game.secret_word = word

	for i in range(num_trials_per_word):
		print(f"running test {i + 1}/{num_trials_per_word} for {word}")
		results = run_one_test(test_game)
		data.append(results)

with open("out.csv",mode="w") as f:
	f.write(f"Won,Target")

	for n in range(test_game.max_guesses):
		f.write(f",Guess {n + 1}")
	f.write("\n")

	for entry in data:
		won, target, guesses = entry

		f.write(f"{won},{target}")
		
		for word in guesses:
			f.write(f",{word}")
		f.write("\n")