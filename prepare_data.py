import pandas as pd
import json
import os
import re
import shutil

imgs = os.listdir('./final_images')
# print(re.search(r'\d+', imgs[0]).group(0))
image_ids = [re.search(r'\d+', e).group(0) for e in imgs if re.search(r'\d+', e)]
# print(image_ids)
recipes = os.listdir('./metadata27638')
bad_recipes = [e for e in recipes if re.search(r'\d+', e) and re.search(r'\d+', e).group(0) not in image_ids]
print(bad_recipes)
# with open('all_yummly.json', 'r+') as f:
# 	data = json.load(f)
	# nums = []
	# for e in data:
	# 	nums.append(e['image_id'])
	# print(nums)
	# images = [f"img{str(num)}" for num in nums]
	# for image in images:
	# 	try:
	# 		shutil.copy(os.path.abspath(f"images27638/{image}.jpg"), "/Users/kanyes/Downloads/Yummly28K/Iris-Yummly-Data-Cleaning/final_images")
	# 	except Exception as e:
	# 		print(e)
	# 		continue
			
	# item = data[0]
	# print(data[0]['nutritionEstimates'][0].keys())
	# print(sorted([e['attribute'] for e in data[0]['nutritionEstimates']]))
	# flattened = pd.io.json.json_normalize(item).to_json()
	# print(json.dumps(json.loads(flattened), indent=4))