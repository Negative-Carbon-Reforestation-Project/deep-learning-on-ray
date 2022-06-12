import argparse
import shutil
import os

from matplotlib.image import imread, imsave

parser = argparse.ArgumentParser(description="checks if images are corrupt, and copy's good images to new dir")
parser.add_argument('data', type=str, help='path folder of images')
args = parser.parse_args()


def convert_image(image):
    return image[:, :, :3]


images = os.listdir(args.data)

if not os.path.exists(f'{args.data}\\valid_images'):
    print('Creating folder at ', f'{args.data}\\valid_images')
    os.makedirs(f'{args.data}\\valid_images')

length = len(images) - 1
count = 1
for image in images:
    print(f'\rchecking image {count}/{length}', end=' ')
    try:
        imread(f'{args.data}\\{image}')
        shutil.copyfile(os.path.abspath(f'{args.data}\\{image}'),
                        os.path.abspath(f'{args.data}\\valid_images\\{image}'))
    except:
        print('Current PNG appears to be corrupt, skipping!')
    count += 1
