import os
import sys
from datetime import datetime
import cv2
from PIL import Image

def percentage(part, whole):
  return 100 * float(part)/float(whole)

def format_path(path):
    path_slash = '' if path[-1] == '/' else '/'
    return path + path_slash

def configure_ext(path, name, extension):
    filepath = path + name
    filename, file_extension = os.path.splitext(filepath)
    return filename + extension

def configure_images_file_paths(path, file_names, extension='.jpg'):
    file_paths = (map(lambda name: configure_ext(path, name, extension), file_names))
    return file_paths

def is_image_allowed(image):
    # return image.endswith('.jpg') or image.endswith('.jpeg') or image.endswith('.JPG')
    return image.endswith('.png')

def images_from_file_path(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    file_names = os.listdir(file_path)
    images = [image for image in file_names if is_image_allowed(image)]
    return images

def resize_image(input_image_path, output_image_path, count, total):
    print('input_image_path', input_image_path)
    image_size = int(size1), int(size2)
    img_data = cv2.imread(input_image_path, 0)
    img_data = cv2.resize(img_data, image_size)
    img = Image.fromarray(img_data)
    img.save(output_image_path)
    percent = str(percentage(count, total)) + '%'
    print (str(count) + ' ' + percent)

def Main():
    start = datetime.now()
    print "START TIME ", str(start)
    input_images = images_from_file_path(INPUT_PATH)
    output_images = images_from_file_path(OUTPUT_PATH)

    remaining_images = [input_image for input_image in input_images if input_image not in output_images]

    input_image_paths = configure_images_file_paths(INPUT_PATH, remaining_images, '.png')
    output_image_paths = configure_images_file_paths(OUTPUT_PATH, remaining_images, '.png')

    paths = zip(input_image_paths, output_image_paths)

    total = len(remaining_images)
    print 'Remaining images to generate by ELA', total

    processes = []
    for index, (input_image_path, output_image_path) in enumerate(paths):
        count = index + 1
        resize_image(input_image_path, output_image_path, count, total)

    print "Finished ", str(datetime.now())
    print 'Took ', datetime.now() - start
    print "ELA Images at: ", OUTPUT_PATH

if __name__ == '__main__':
    INPUT_PATH = format_path(sys.argv[1] if len(sys.argv) > 1 else 'data/images-ela/fake')
    OUTPUT_PATH = format_path(sys.argv[2] if len(sys.argv) > 2 else 'data/fake-ela-resized')
    size1 = sys.argv[3] if len(sys.argv) > 3 else 128
    size2 = sys.argv[4] if len(sys.argv) > 4 else 128
    Main()
