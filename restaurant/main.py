SANDWICHES = { 
	"veggie": 7,
	"chicken": 5.5,
	"steak": 6.25,
}

TOPPINGS = {
	"lettuce": 0.15,
	"tomatoes": 0.10,
	"olives": 0.25,
}

BEVERAGES = {
	"small": 1,
	"medium": 1.5,
	"large": 2.25,
}

DESSERTS = {
	"dulce de leche chantilly": 2.5,
	"chocolate chip": 1.5,
	"tres leches": 3
}

IRS_MANDATED_TAX_ON_YOUR_HARD_EARNED_MONEY_PERCENT = 0.03 # i think it's 3% based off googling "indiana tax rate" :)

class Receipt:
	def __init__(self) -> None:
		self.items = []
		self.costs = []
	
	def add_item(self, item: str, cost: float):
		self.items.append(item)
		self.costs.append(cost)

	def calculate_subtotal(self) -> float:
		# return sum(self.costs)
		# just incase im supposed to be doing it like this
		total = 0

		for cost in self.costs:
			total += cost

		return total

def tax(subtotal: float) -> float:
	return subtotal + subtotal * IRS_MANDATED_TAX_ON_YOUR_HARD_EARNED_MONEY_PERCENT

def sanitized_input(prompt: str) -> str:
	return input(prompt).strip().lower()
def prompt_menu(title: str, items: dict[str, float]) -> tuple[str, float]:
	print(f"===== {title} =====")

	for name, price in items.items():
		print(f"{name}: ${price:.2f}")

	while True:
		choice = sanitized_input("Choice: ")

		if choice not in items:
			print("Invalid item")
			continue

		return choice, items[choice]

def prompt_toppings(receipt: Receipt):
	item_name, price = prompt_menu("TOPPINGS MENU", TOPPINGS)
	receipt.add_item("with " + item_name, price)
def prompt_sandwiches(receipt: Receipt):
	item_name, price = prompt_menu("SANDWICHES MENU", SANDWICHES)
	receipt.add_item(item_name + " sandwich", price)

	if sanitized_input("Toppings? (y/n) ") == "y":
		prompt_toppings(receipt)
def prompt_beverages(receipt: Receipt):
	item_name, price = prompt_menu("BEVERAGES MENU", BEVERAGES)
	receipt.add_item(item_name + " drink", price)
def prompt_desserts(receipt: Receipt):
	receipt.add_item(*prompt_menu("DESSERTS MENU", DESSERTS))

def special(receipt: Receipt):
	if receipt.calculate_subtotal() > 20:
		receipt.add_item("SPECIAL: 2 liter of DIET coke", 0)
	else:
		receipt.add_item("SPECIAL: $1 coupon for future purchases", 0)
def checkout(receipt: Receipt):
	if sanitized_input("Are you interested in any special offers? (y/n) ") == "y":
		special(receipt)
	
	print("Final Bill:")

	for item in receipt.items:
		print(f" - {item}")
	
	subtotal = receipt.calculate_subtotal()
	final = tax(subtotal)

	print("-" * 20)
	print(f"Subtotal: ${subtotal:.2f}")
	print(f"Final Price With TAX: ${final:.2f}")

def main():
	our_receipt = Receipt()

	done = False

	while not done:
		print("S - Sandwiches")
		print("B - Beverages")
		print("D - Dessert")
		print("C - Checkout and Quit")

		choice = sanitized_input("Choice: ")

		if choice == "s":
			prompt_sandwiches(our_receipt)
		elif choice == "b":
			prompt_beverages(our_receipt)
		elif choice == "d":
			prompt_desserts(our_receipt)
		elif choice == "c":
			checkout(our_receipt)
			done = True

main()
