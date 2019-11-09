import argparse
import cv2
from PIL import Image, ImageOps, ImageDraw
import os
import numpy as np

parser = argparse.ArgumentParser(
    description='Run Image Generator')

parser.add_argument(
    '-i',
    '--input_image',
    help='path to input image')
parser.add_argument(
    '-id',
    '--input_dir',
    help='path to directory with base images',
    default='base_images')
parser.add_argument(
    '-o',
    '--output_directory',
    help='path to directory where ouput images will be stored',
    default='output')
parser.add_argument(
    '-O',
    '--output_filename',
    help='Name of base of output file, after that will be added a number. Default name "output" ',
    default='output')    
parser.add_argument(
    '-m',
    '--mask',
    help='path to masks directory / library',
    default='masks')
parser.add_argument(
    '-n',
    '--number_combinations',
    type=int,
    help='number of combinations covering base images. Default 16',
    default=1)
parser.add_argument(
    '-l',
    '--label',
    type=str,
    help='label type. Defauñt Yolov3',
    default="yolo")


args = parser.parse_args()

def _main():
    if args.label:
        f = open(args.label, "r")
        label_content = f.read()


    if args.input_image:
        print(label_content)
        im2 = Image.open(args.input_image)
        im1 = Image.open('media/empty.png')
        im1 = im1.resize((im2.size[0], im2.size[1]), resample=0)

        for i in range(args.number_combinations):
            mask = Image.new("L", im1.size, 0)
            draw = ImageDraw.Draw(mask)
            point_x = np.random.randint(-im2.size[0]+20, im2.size[0]-20)
            point_y = np.random.randint(-im2.size[1]+20, im2.size[1]-20)
            point_x1 = point_x + im2.size[0]
            point_y1 = point_y + im2.size[1]
            draw.ellipse((point_x, point_y, point_x1, point_y1), fill=255)
            im= Image.composite(im1, im2, mask)
            output_filename = args.output_directory + "/" + args.output_filename + "_" + str(i)
            im.save(output_filename + ".png","PNG")
            statinfo = os.stat(output_filename + ".png")
            if statinfo.st_size > 2000:
                if label_content:
                    lf = open(output_filename + ".txt", "w")
                    lf.write(label_content)
                    lf.close()
            else:
                os.remove(output_filename + ".png")

if __name__ == '__main__':
    _main()