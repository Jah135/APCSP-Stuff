from ansi import tint

INITIAL_SCENARIO = (
	"I'm not a story writer",
	{
		"Yeah man, you suck at this": (
			"Why don't you do it yourself then huh"
		),
		"Option2": "Answer2"
	}
)

def run_scene(scene: str | tuple[str, dict]):
	if isinstance(scene, str):
		print(scene)
		
		return
	
	initial_message, options = scene

	print(initial_message, "\n")

	# list options
	choice_indices = []

	for (index, option) in enumerate(options.keys()):
		print(f"{index + 1}. {option}")
		choice_indices.append(option)

	choice_scene = None

	# wait for valid input
	while True:
		try:
			choice_index = int(input("> ")) - 1
			choice_scene = options[choice_indices[choice_index]] # this fucking sucks

			if choice_scene:
				break
		except:
			pass

		print(tint("Invalid option!", 91))

	print("-" * 40)

	run_scene(choice_scene)

run_scene(INITIAL_SCENARIO)