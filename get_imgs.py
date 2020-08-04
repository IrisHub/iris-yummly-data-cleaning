import os, json, re, shutil, sys
import base64

def printProgressBar (iteration, total, prefix = 'Progress:', suffix = 'Complete', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print("\nDone")

def __main__():

	assert len(sys.argv) > 1, "AssertionError: missing value (name)"
	if not str(sys.argv[1].lower())=="kanyes":
		assert re.search(r'/Yummly28K$', os.getcwd()), "AssertionError: must run inside the Yummly28k directory"

	new_dir=f"{os.getcwd()}/images_to_filter"

	with open("recipe_ids.txt", "r+") as f:
		ids=f.read()

	bytes_ids = str(ids).encode('utf-8')
	ids = base64.b64decode(bytes_ids).decode('utf-8')
	ids = ids.split(',')
	
	if not (os.path.exists(new_dir) and os.access(new_dir, os.R_OK)):
		os.mkdir(new_dir)
	
	img_list = os.listdir('./images27638')
	imgs = [f"img{e}.jpg" for e in ids if f"img{e}.jpg" in img_list]

	if sys.argv[1].lower() == "shalin":
		imgs=imgs[:len(imgs)//3]
	elif sys.argv[1].lower() == "sam":
		imgs=imgs[len(imgs)//3:-len(imgs)//3]
	else:
		imgs = imgs[-len(imgs)//3:]

	printProgressBar(0, len(imgs), prefix='Copying Images:')
	for i,img in enumerate(imgs):
		try:
			shutil.copy(os.path.abspath(f"images27638/{img}"), new_dir)
		except Exception as e:
			print(e)
			pass
		printProgressBar(i+1, len(imgs), prefix='Copying Images:')

__main__()