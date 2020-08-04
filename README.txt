To use the scripts:

Put these scripts in the same directory as the top level Yummly28k directory you downloaded (NOT inside the actual metadata/image folders)

Run `python3 get_imgs.py your-name` (ex. `python get_imgs.py kanyes`) in order to get a folder (titled `images_to_filter`) of your images to filter through.

Go through the images in this new folder and DELETE the ones which are bad (as in objectively bad images, not just low-quality). Low-quality images can be upsampled and saved, so do not delete them. Also delete images with obtrusive watermarks, disgusting food, really weird cropping, etc. If you are unsure whether or not to delete an image, message the group chat.

When you are done, run `python3 compile_ids.py` to get a text file with a list of all the IDs (called `final_img_ids.txt`). Send this file to Kanyes and you're done :-) thanks a bundle~