'''
Title: trivia
Author: me
Description: answer the questions NOW
'''

LEADERBOARD: dict[str, float] = {}
CATEGORIES: dict[str, list[tuple[str, list[str]]]] = {
	"programming": [
		("\"Hello, _____!\"", ["world"]),
		("What data type should you use if you want to store a whole number?", ["int", "integer"]),
		("How many bits are in a byte?", ["8", "eight"]),
		("How many bytes are in a megabyte?", ["1000000", "million", "a million"]),
		("What do you use to end a line in most programming languages?", [";", "semicolon"]),
		("What data type should you use if you want to store a decimal number?", ["float", "double"]),
		("What is missing from this python code?\nif True\n\tprint(\"Hello\")\nelse:\n\tprint(\"something has gone terribly wrong!\")", [":", "colon"]),
		("What is objectively the worst programming language?", ["c++"]), # all of them
	],
	"spanish": [
		("What is 'friend' in Spanish?", ["amigo", "amiga"]),
		("Como se escribe \"The United States\" en espanol?", ["los unidos estadios"]) # probably correct
	]
}

def sanitized_input(text: str) -> str:
	return input(text).strip().lower()

def prompt_category():
	category_display = "Categories:\n"

	for category in CATEGORIES:
		category_display += f"- {category + "\n"}"

	print(category_display)

	while True:
		category = sanitized_input("Choose a category: ")

		if category in CATEGORIES:
			return category
		print("Invalid category.")

def run_game_category(category: str) -> float:
	questions = CATEGORIES[category]
	score = 0

	for question, answers in questions:
		player_answer = sanitized_input(question + "\n> ")

		if player_answer in answers:
			print("Correct!")
			score += 1
		else:
			print("Incorrect!")
			break

	return score / len(questions)

def display_leaderboard():
	output = "===============\nLeaderboard:\n"

	for player, score in LEADERBOARD.items():
		output += f"{player}: {score*100:.1f}%"

	print(output)

def main():
	done = False

	while not done:
		print("==========")
		print("s - Start")
		print("d - Display")
		print("q - Quit")

		choice = sanitized_input("Choice: ")

		if choice == "s":
			print("Starting Game")

			player_name = input("What's your name? ")

			print("Welcome to the game", player_name + "!")

			score = run_game_category(prompt_category())

			print(f"{player_name}, you scored {score*100:.1f}%")

			LEADERBOARD[player_name] = score

		elif choice == "d":
			display_leaderboard()
		elif choice == "q":
			print("Exiting Program")
			done = True

main()