import os, json
import base64


with open("all_yummly.json", 'r+') as f:
	data = json.load(f)

	imgs = [e['image_id'] for e in data]
	imgs = ','.join(imgs)

	string = base64.b64encode(bytes(imgs, 'utf-8'))

	print(base64.b64decode(string))