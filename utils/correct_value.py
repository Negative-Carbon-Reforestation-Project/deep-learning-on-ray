import argparse
import shutil
import os
import numpy as np

from matplotlib.image import imread, imsave

parser = argparse.ArgumentParser(description="corrects class value, and copy's good images to new dir")
parser.add_argument('data', type=str, help='path folder of images')
args = parser.parse_args()

images = os.listdir(args.data)

if not os.path.exists(f'{args.data}\\..\\corrected_images'):
    print('Creating folder at ', f'{args.data}\\..\\corrected_images')
    os.makedirs(f'{args.data}\\..\\corrected_images')

length = len(images) - 1
count = 1
for image in images:
    print(f'\rchecking image {count}/{length}', end=' ')
    split_name = os.path.splitext(image)[0].split("_")
    print(split_name)
    curr_value = float(split_name[5])
    original_value = np.divide(np.multiply(54130, curr_value), np.add(curr_value, 1))
    new_value = np.divide(original_value, 54130)
    new_name = str(f'{split_name[0]}_{split_name[1]}_{split_name[2]}_{split_name[3]}_{split_name[4]}_{new_value}.png')
    shutil.copyfile(os.path.abspath(f'{args.data}\\{image}'),
                    os.path.abspath(f'{args.data}\\..\\corrected_images\\{new_name}'))
    count += 1