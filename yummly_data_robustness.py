import json
import math

# Test query robustness for common queries
with open('all_yummly.json', 'r+') as f:
	vegetarian_exclude = ['meat', 'gelatin', 'chicken', 'turkey', 'duck', 'quail',
		'beef', 'pork', 'bacon', 'lamb', 'mutton', 'venison', 'rabbit', 'goat',
		'salmon', 'fish', 'tuna', 'cod', 'tilapia', 'bass',
		'shrimp', 'oyster', 'crab', 'clam', 'octopus', 'eel']
	vegan_exclude = ['milk', 'cheese', 'yogurt', 'egg', 'honey', 'butter', 'cream', 'custard', 'ghee', 'queso', 'paneer']
	vegetarian_count = 0
	vegan_count = 0
	neither_count = 0
	data = json.load(f)


	def search_ingredient(query):
		counter = 0
		for e in data:
			query_flag = True
			for ingredient in e['ingredientLines']:
				if query in ingredient and query_flag:
					counter += 1
					query_flag = False
		return f"Total results for ingredient \"{query}\": {counter}"

	def search_cuisine(query):
		counter = 0
		for e in data:
			if query in e['attributes']['cuisine'].lower():
				counter += 1
		return f"Total results for cuisine \"{query}\": {counter}"

	def search_dish(query):
		counter = 0
		for e in data:
			if query in e['name'].lower():
				counter += 1
				print(e['name'])
		return f"Total results for dish \"{query}\": {counter}"

	def search_flavor(query):
		counter = 0
		for e in data:
			if 'flavors' in e.keys() and query in [a.lower() for a in e['flavors'].keys()] and float(e['flavors'][query]) > 0 : counter += 1
		return f"Total results for flavor \"{query}\": {counter}"


	def __main__():
		cont = True
		function = None
		while cont:
			action = input("(1) Ingredient, (2) Cuisine, (3) Dish, (4) Flavor: ")
			if action == "1":
				query = input("Ingredient: ")
				print(search_ingredient(query))
			elif action == "2":
				query = input("Cuisine: ")
				print(search_cuisine(query))
			elif action == "4":
				query = input("Flavor: ")
				print(search_flavor(query))
			else:
				query = input("Dish: ")
				print(search_dish(query))

			loop= input("Again? y/n: ")
			if loop == "n":
				cont = False

	__main__()
	# chicken_counter = 0
	# carrot_counter = 0
	# chinese_counter = 0
	# omelette_counter = 0
	# ramen_counter = 0
	# flavor_counter = 0
	# for e in data:
		# if 'flavors' in e.keys() and e['flavors'] is not None: flavor_counter += 1
		# if 'Chinese' in e['attributes']['cuisine']: chinese_counter += 1
		# if 'enchilada' in e['name'].lower():
		# 	print(e['name'])
		# 	omelette_counter += 1
		# chicken_flag, carrot_flag = True, True
		# ramen_flag = True
		# diet_flag = True
		# for ingredient in e['ingredientLines']:
		# 	if 'carrot' in ingredient and carrot_flag:
		# 		carrot_counter += 1
		# 		carrot_flag = False
		# 	if 'spaghetti' in ingredient.lower() and chicken_flag:
		# 		chicken_counter += 1
		# 		chicken_flag = False
		# 	if 'ramen' in ingredient.lower() and ramen_flag:
		# 		ramen_counter += 1
		# 		ramen_flag = False

		# nonveg_ingredients = list(filter(lambda item: any(ing in item for ing in vegetarian_exclude), e['ingredientLines']))
		# nonvegan_ingredients = list(filter(lambda item: any(ing in item for ing in vegan_exclude), e['ingredientLines']))

		# if len(nonveg_ingredients) == 0 and len(nonvegan_ingredients) == 0:
		# 	vegan_count += 1
		# elif len(nonveg_ingredients) == 0 and len(nonvegan_ingredients) > 0:
		# 	vegetarian_count += 1
		# else:
		# 	neither_count += 1


	# print(f"Dishes with flavor information: {flavor_counter}")
	# print(f"Chinese dishes: {chinese_counter}. Assuming 6 recipes a day, this lasts for {int(math.floor(chinese_counter/6))}.")
	# print(f"Ramen: {omelette_counter}. Assuming 3 recipes a day, this lasts for {int(math.floor(omelette_counter/3))}.")
	# print(f"Chicken dishes: {chicken_counter}. Assuming 6 recipes a day, this lasts for {int(math.floor(chicken_counter/6))}.")
	# print(f"Carrot dishes: {carrot_counter}. Assuming 6 recipes a day, this lasts for {int(math.floor(carrot_counter/6))}.")
	# print(f"Breakdown: Vegan - {vegan_count}, Vegetarian - {vegetarian_count}, Neither - {neither_count}")

