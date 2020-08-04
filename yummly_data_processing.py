import json, os
import random
import statistics
from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
import uuid

def add_field(field, func):
	with open('all_yummly.json', 'r+') as f:
		f.seek(0)
		data = json.load(f)
		for e in data:
			e[field] = func(e)
		f.seek(0)
		f.write(json.dumps(data, indent=4))
		f.truncate()

def remove_field(field):
	with open('all_yummly.json', 'r+') as f:
		f.seek(0)
		data = json.load(f)
		for e in data:
			del e[field]
		f.seek(0)
		f.write(json.dumps(data, indent=4))
		f.truncate()

def extract_titles():
	titles = []
	with open('all_yummly.json', 'r+') as f:
		f.seek(0)
		data = json.load(f)
		titles = [e['name'] for e in data]
		f.seek(0)
	with open('yummly_titles.txt', 'w+') as f:
		f.seek(0)
		f.write('\n'.join(titles))
		f.truncate()

def extract_course():
	titles = []
	with open('all_yummly.json', 'r+') as f:
		f.seek(0)
		data = json.load(f)
		titles = [e['attributes']['course'] for e in data]
		f.seek(0)
	with open('yummly_courses.txt', 'w+') as f:
		f.seek(0)
		f.write('\n'.join(['\n'.join(e) for e in titles]))
		f.truncate()

def extract_temp_field(field_name):
	with open('all_yummly.json', 'r+') as f:
		f.seek(0)
		data = json.load(f)
		return [e[field_name] for e in data]

### Filter main JSON based on a lambda boolean expression
def filter_json(expr):
	with open('all_yummly.json', 'r+') as f:
		f.seek(0)
		data = json.load(f)
		keep = [e for e in data if expr(e)]
		f.seek(0)
		f.write(json.dumps(keep, indent=4))
		f.truncate()

### Apply a regex function to clean JSON
def clean_json(field, regexpr):
	with open('all_yummly.json', 'r+') as f:
		f.seek(0)
		data = json.load(f)
		for e in data:
			e[field] = regexpr(e)
		f.seek(0)
		f.write(json.dumps(data, indent=4))
		f.truncate()

### Plot histograms of data based on extraction expression
def hist(data_expr):
	with open('all_yummly.json', 'r+') as f:
		f.seek(0)
		data = json.load(f)
		vals = [data_expr(e) for e in data]
		mean_val = statistics.mean(vals)
		print(f"Average: {mean_val}")
		sns.set(color_codes=True)
		sns.distplot(vals)
		plt.show()

def count(data_expr):
	with open('all_yummly.json', 'r+') as f:
		f.seek(0)
		data = json.load(f)
		vals = [data_expr(e) for e in data]
		sns.set(color_codes=True)
		sns.countplot(vals)
		plt.show()

###Load all recipes into single file

recipes = []

with open('final_img_ids_shalin.txt', 'r+') as f:
	shalin_ids = str(f.read())

with open('final_img_ids_sam.txt', 'r+') as f:
	sam_ids = str(f.read())

with open('final_img_ids_kanyes.txt', 'r+') as f:
	kanyes_ids = str(f.read())

shalin_ids = shalin_ids.split('\n')
sam_ids = sam_ids.split('\n')
kanyes_ids = kanyes_ids.split('\n')

good_imgs = shalin_ids + sam_ids + kanyes_ids

for f in os.scandir('./metadata27638'):
	with open(f) as file:
		item = json.load(file)
		img_id = re.search(r'\d+', f.name).group(0)
		if img_id not in good_imgs:
			continue
		else:
			item['image_id'] = img_id
			recipes.append(item)

with open('all_yummly.json', 'r+') as f:
	f.seek(0)
	f.write(json.dumps(recipes, indent=4))
	f.truncate()

### Remove all recipes that take > 1 hr
time_expr = lambda e: e['totalTimeInSeconds'] and e['totalTimeInSeconds']<=3600
filter_json(time_expr)

### Remove all condiments and sauces
type_expr = lambda e: 'Condiments and Sauces' not in ','.join(e['attributes']['course'])
filter_json(type_expr)
type_expr = lambda e: 'Beverages' not in ','.join(e['attributes']['course'])
filter_json(type_expr)

### Find average title length of recipes
title_length_expr = lambda e: len(e['name'])
# hist(title_length_expr)

### Substitute out all hashtags
field = 'name'
regexpr = lambda e: re.sub(r'(#[A-Za-z0-9]+)', "",e['name'])
clean_json(field, regexpr)

### Substitute bad unicode encodings
field = 'ingredientLines'
regexpr = lambda e: [re.sub(r'(\u00bd)', "1/2",a) for a in e['ingredientLines']]
clean_json(field, regexpr)

field = 'ingredientLines'
regexpr = lambda e: [re.sub(r'(\u00bc)', "1/4",a) for a in e['ingredientLines']]
clean_json(field, regexpr)

field = 'ingredientLines'
regexpr = lambda e: [re.sub(r'(\u00f1)', "n",a) for a in e['ingredientLines']]
clean_json(field, regexpr)


### Remove anything in parentheses
field = 'name'
regexpr = lambda e: re.sub(r'\(.*\)|\{.*\}', "", e['name'])
clean_json(field, regexpr)

### Remove anything in parentheses
field = 'name'
regexpr = lambda e: re.sub(r'(")(.*)(")', lambda rgx: f"{rgx.group(2)}", e['name'])
clean_json(field, regexpr)

###Sub all recipes with the word "With"
field = 'name'
regexpr = lambda e: re.sub(r'(?i)^(([a-zA-Z-&]+\s?\b){2,})( with.*)$',lambda rgx: f"{rgx.group(1)}",e['name'])
clean_json(field, regexpr)

###Sub all recipes with the word "from"
field = 'name'
regexpr = lambda e: re.sub(r'(?i)^( from.*)$',"",e['name'])
clean_json(field, regexpr)

### Extract titles to new file for safekeeping!
extract_titles()

### Remove recipes with exceptionally poor ratings
ratings_expr = lambda e: e['rating']>=3
filter_json(ratings_expr)

get_source = lambda e: e['source']['sourceRecipeUrl']
add_field('url', get_source)
remove_field('source')

get_cuisine = lambda e: e['attributes']['cuisine'][0]
add_field('cuisine', get_cuisine)
get_course = lambda e: e['attributes']['course'][0]
add_field('course', get_course)
remove_field('attributes')
remove_field('attribution')
remove_field('images')

get_spice = lambda e: True if 'Piquant' in e['flavors'] and e['flavors']['Piquant'] > 0.6 else False
add_field('spicy', get_spice)
get_sweet = lambda e: True if 'Sweet' in e['flavors'] and e['flavors']['Sweet'] > 0.6 else False
add_field('sweet', get_sweet)
remove_field('flavors')

title_length_expr = lambda e: len(e['name'])
# hist(title_length_expr)

def diet_function(e):
	vegetarian_exclude = ['meat', 'gelatin', 'chicken', 'turkey', 'duck', 'quail',
		'beef', 'pork', 'bacon', 'lamb', 'mutton', 'venison', 'rabbit', 'goat',
		'salmon', 'fish', 'tuna', 'cod', 'tilapia', 'bass',
		'shrimp', 'oyster', 'crab', 'clam', 'octopus', 'eel']
	vegan_exclude = ['milk', 'cheese', 'yogurt', 'egg', 'honey', 'butter', 'cream', 'custard', 'ghee', 'queso', 'paneer']
	pescatarian_exclude = ['meat', 'gelatin', 'chicken', 'turkey', 'duck', 'quail',
		'beef', 'pork', 'bacon', 'lamb', 'mutton', 'venison', 'rabbit', 'goat',]
	nonveg_ingredients = list(filter(lambda item: any(ing in item for ing in vegetarian_exclude), e['ingredientLines']))
	nonvegan_ingredients = list(filter(lambda item: any(ing in item for ing in vegan_exclude), e['ingredientLines']))

	if len(pescatarian_exclude) == 0 and len(nonveg_ingredients) > 0:
		return 'pescatarian'
	elif len(nonveg_ingredients) == 0 and len(nonvegan_ingredients) == 0:
		return 'vegan'
	elif len(nonveg_ingredients) == 0 and len(nonvegan_ingredients) > 0:
		return 'vegetarian'
	else:
		return 'none'


field='diet'
add_field(field, diet_function)
diet_expr = lambda e: e['diet']
# count(diet_expr)


times = extract_temp_field('totalTimeInSeconds')
steps = [len(e) for e in extract_temp_field('ingredientLines')]

def difficulty_function(e):
	time_percentile = stats.percentileofscore(times, e['totalTimeInSeconds'])
	steps_percentile = stats.percentileofscore(steps, len(e['ingredientLines']))
	difficulty = 0.5*time_percentile + 0.5*steps_percentile
	if difficulty < 0.37:
		return "Beginner"
	elif difficulty < 0.63:
		return "Intermediate"
	else:
		return "Advanced"

field = 'difficulty'
add_field(field, difficulty_function)
difficulty_expr = lambda e: e['difficulty']

# hist(spice_expr)

remove_field('totalTime')
remove_field('nutritionEstimates')

with open('all_yummly.json', 'r+') as f:
	data = json.load(f)
	if 'uuid' not in data[0].keys():
		for e in data:
			e['uuid'] = str(uuid.uuid4())
		f.seek(0)
		f.write(json.dumps(data, indent=4))
		f.truncate()