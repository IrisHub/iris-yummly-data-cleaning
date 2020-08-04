import os, json, re, shutil

def printProgressBar (iteration, total, prefix = 'Progress:', suffix = 'Complete', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print("\nDone")

def __main__():
	final_dir=f"{os.getcwd()}/images_to_filter"
	imgs = os.listdir(final_dir)
	ids = []

	printProgressBar(0, len(imgs), prefix='Extracting IDs:')
	for i,e in enumerate(imgs):
		if re.search(r'\d+', e):
			ids.append(str(re.search(r'\d+',e).group(0)))
		printProgressBar(i+1, len(imgs), prefix='Extracting IDs:')
	with open('final_img_ids.txt', 'w+') as f:
		f.seek(0)
		f.write('\n'.join(ids))
		f.truncate()

__main__()