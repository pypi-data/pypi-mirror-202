import sys
import time
from pathlib import Path

import fire
import numpy as np
import pyperclip
import keyboard
from PIL import Image
from PIL import UnidentifiedImageError
from loguru import logger

from manga_ocr import MangaOcr

page = 0
picture = 0
box = 0
text = 0
bubble = 0

def are_images_identical(img1, img2):
    if None in (img1, img2):
        return img1 == img2

    img1 = np.array(img1)
    img2 = np.array(img2)

    return (img1.shape == img2.shape) and (img1 == img2).all()


def process_and_write_results(mocr, img_or_path, write_to, file, result):
    t0 = time.time()
    text = mocr(img_or_path)
    t1 = time.time()

    logger.info(f'Text recognized in {t1 - t0:0.03f} s: {text}')

    if write_to == 'clipboard':
        pyperclip.copy(text)
    
    file = Path(file)
    if file.suffix != '.txt':
        raise ValueError('write_to must be either "clipboard" or a path to a text file')

    with file.open('a', encoding="utf-8") as f:
        f.write(result + ': ' + text + '\n')


def get_path_key(path):
    return path, path.lstat().st_mtime

def record_keystrokes(picture, bubble, text, box):
    event = keyboard.read_event()
    result = ""
    if event.event_type == 'down':
        if event.name == 'b':
            bubble += 1
            result = "b" + bubble
            result = "P" + picture + result 
        elif event.name == 'x':
            box += 1
            result = "box " + box
            result = "P" + picture + result 
        elif event.name == 't':
            text += 1
            result = "text " + text
            result = "P" + picture + result 
    return result
    

def run(read_from='clipboard',
        write_to='clipboard',
        file = 'tl.txt',
        pretrained_model_name_or_path='kha-white/manga-ocr-base',
        force_cpu=False,
        delay_secs=0.1
        ):
    """
    Run OCR in the background, waiting for new images to appear either in system clipboard, or a directory.
    Recognized texts can be either saved to system clipboard, or appended to a text file.

    :param read_from: Specifies where to read input images from. Can be either "clipboard", or a path to a directory.
    :param write_to: Specifies where to save recognized texts to. Can be either "clipboard", or a path to a text file.
    :param pretrained_model_name_or_path: Path to a trained model, either local or from Transformers' model hub.
    :param force_cpu: If True, OCR will use CPU even if GPU is available.
    :param delay_secs: How often to check for new images, in seconds.
    """
    global page, picture, bubble, text, box
    mocr = MangaOcr(pretrained_model_name_or_path, force_cpu)

    if read_from == 'clipboard':

        if sys.platform not in ('darwin', 'win32'):
            msg = 'Reading images from clipboard works only on macOS and Windows. ' \
                  'On Linux, run "manga_ocr /path/to/screenshot/folder" to read images from a folder instead.'
            raise NotImplementedError(msg)

        from PIL import ImageGrab
        logger.info('Reading from clipboard')

        img = None
        while True:
            old_img = img
            event = keyboard.read_event()
            result = ""
            if event.name == 'z':
                page += 1
                box = bubble = text = 0
                picture = 1
                result = "Page " + page + "\n"
                file = Path(file)
                if file.suffix != '.txt':
                    raise ValueError('write_to must be either "clipboard" or a path to a text file')
                with file.open('a', encoding="utf-8") as f:
                    f.write(result)

            if event.name == 'space':
                picture += 1
                box = bubble = text = 0

            result = record_keystrokes(picture, bubble, text, box)
            try:
                img = ImageGrab.grabclipboard()
            except OSError:
                logger.warning('Error while reading from clipboard')
            else:
                if isinstance(img, Image.Image) and not are_images_identical(img, old_img):
                    process_and_write_results(mocr, img, write_to, file, result)

            time.sleep(delay_secs)


    else:
        read_from = Path(read_from)
        if not read_from.is_dir():
            raise ValueError('read_from must be either "clipboard" or a path to a directory')

        logger.info(f'Reading from directory {read_from}')

        old_paths = set()
        for path in read_from.iterdir():
            old_paths.add(get_path_key(path))

        while True:
            for path in read_from.iterdir():
                path_key = get_path_key(path)
                if path_key not in old_paths:
                    old_paths.add(path_key)

                    try:
                        img = Image.open(path)
                        img.load()
                    except (UnidentifiedImageError, OSError) as e:
                        logger.warning(f'Error while reading file {path}: {e}')
                    else:
                        process_and_write_results(mocr, img, write_to, file)

            time.sleep(delay_secs)


if __name__ == '__main__':
    fire.Fire(run)
