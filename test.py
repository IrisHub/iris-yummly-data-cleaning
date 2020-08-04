import json
import time

now = time.time()

with open('all_yummly.json', 'r+') as f:
	data = json.load(f)
	print(len(data))
	def run_through():
		i = 1
		for e in data:
			i += 1
	run_through()	
	run_through()
	run_through()
	run_through()
	run_through()
	run_through()
	run_through()
	run_through()
	run_through()
	run_through()
	run_through()


print(time.time() - now)