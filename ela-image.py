from __future__ import print_function
from PIL import Image, ImageChops, ImageEnhance
import sys, os, time, collections
from threading import Thread
from Queue import Queue
from datetime import datetime

TMP_EXT = ".tmp_ela.jpg"
ELA_EXT = "_ela.png"
quality = 90

def format_path(path):
    path_slash = '' if path[-1] == '/' else '/'
    return path + path_slash

def is_image_allowed(image):
    return image.endswith('.jpg') or image.endswith('.jpeg') or image.endswith('.JPG') or image.endswith('.png')

def images_from_file_path(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    file_names = os.listdir(file_path)
    images = [image for image in file_names if is_image_allowed(image)]
    return images

def configure_ext(path, name, extension):
    filepath = path + name
    filename, file_extension = os.path.splitext(filepath)
    return filename + extension

def configure_images_file_paths(path, file_names, extension='.jpg'):
    file_paths = (map(lambda name: configure_ext(path, name, extension), file_names))
    return file_paths

def print_progress(progress):
    sys.stdout.write('\033[2J\033[H') #clear screen
    for filename, percent in progress.items():
        bar = ('=' * int(percent * 20)).ljust(20)
        percent = int(percent * 100)
        sys.stdout.write("%s [%s] %s%%\n" % (filename, bar, percent))
    sys.stdout.flush()

def ela(orig_path, temp_path, save_path, i, total, status):
    """
    Generates an ELA image on save_path.
    """
    im = Image.open(orig_path)
    im.save(temp_path, 'JPEG', quality=quality)

    tmp_fname_im = Image.open(temp_path)
    ela_im = ImageChops.difference(im, tmp_fname_im)

    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0/max_diff
    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)

    ela_im.save(save_path)
    os.remove(temp_path)

    status.put([save_path, 1.0])

def get_remaining_images(input_images, output_images):
    input_images = map(lambda x: x.split('.jpg')[0], input_images)
    output_images = map(lambda x: x.split('_ela.png')[0], output_images)
    return [input_image for input_image in input_images if input_image not in output_images]

def main(INPUT_PATH, OUTPUT_PATH):
    start = datetime.now()
    dirc = INPUT_PATH
    ela_dirc = OUTPUT_PATH

    print("Performing ELA on images at %s" % dirc)

    input_images = images_from_file_path(dirc)
    output_images = images_from_file_path(ela_dirc)
    remaining_images = get_remaining_images(input_images, output_images)

    input_image_paths = configure_images_file_paths(dirc, remaining_images)
    temp_image_paths = configure_images_file_paths(dirc, remaining_images, TMP_EXT)
    output_image_paths = configure_images_file_paths(ela_dirc, remaining_images, ELA_EXT)
    paths = zip(input_image_paths, temp_image_paths, output_image_paths)

    total = len(remaining_images)
    print('Remaining images to generate by ELA', total)

    status = Queue()
    progress = collections.OrderedDict()
    threads = []

    for i, (input_image_path, temp_path, output_image_path) in enumerate(paths):
        thread = Thread(target=ela, args=[input_image_path, temp_path, output_image_path, i, total, status])
        threads.append(thread)
        thread.start()
        progress[output_image_path] = 0.0

    while any(i.is_alive() for i in threads):
        while not status.empty():
            filename, percent = status.get()
            progress[filename] = percent
            print_progress(progress)

    for t in threads:
        t.join()

    print("Finished!")
    print('Took ', datetime.now() - start)
    print("Head to %s to check the results!" % ela_dirc)


if __name__ == '__main__':
    INPUT_PATH = format_path(sys.argv[1] if len(sys.argv) > 1 else 'data/images/fake')
    OUTPUT_PATH = format_path(sys.argv[2] if len(sys.argv) > 2 else 'data/images-ela/fake-ela')
    main(INPUT_PATH, OUTPUT_PATH)
else:
    print("This shouldn't be imported.", file=sys.stderr)
    sys.exit(1)
