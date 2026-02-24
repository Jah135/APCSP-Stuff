Scene = tuple[str, list[tuple[str, 'Scene']]]

initial: Scene = (
	"Hello",
	[
		("Choice 1", ("Chose 1", [])),
		("Choice 2", ("Chose 2", []))
	]
)

def print_error(text: str):
	print(f"\x1b[31m{text}\x1b[0m")

def run_scene(scene: Scene):
	context, choices = scene
	
	print(context)

	if len(choices) == 0:
		return

	print("Choose an option")
	for index, choice in enumerate(choices):
		print(f"{index+1}: {choice[0]}")
	
	while True:
		# handling user input
		try:
			choice_index = int(input("> "))
			if choice_index <= 0:
				raise
			if choices[choice_index - 1] == None:
				raise
		except Exception:
			print_error("Invalid option.")
			continue
		break

	chosen_option = choices[choice_index - 1]
	run_scene(chosen_option[1])

run_scene(initial)