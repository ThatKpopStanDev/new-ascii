import shutil
import subprocess
import sys
from PIL import Image
import time
import os
import numpy as np


width = 95
height = 70

def find(name, path):
    for root, _, files in os.walk(path):
        if name + ".webm" in files:
            return os.path.join(root, name + ".webm")
    raise ValueError("Archivo no encontrado")


def resize_image(image, new_width):
    orig_width, orig_height = image.size
    ratio = orig_height / orig_width
    new_height = int(new_width * ratio * 0.55)
    return image.resize((new_width, new_height))


def pixels_to_ascii(image):
    image = image.convert("RGB")
    pixels = np.array(image)
    ascii_image = ""

    for row in pixels:
        for pixel in row:
            r, g, b = pixel

            char = ASCII_CHARS[len(ASCII_CHARS) // 256]
            ascii_image += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        ascii_image += "\n"

    return ascii_image


def image_to_ascii(image, terminal_width, max_width=width ):

    new_width = min(terminal_width, max_width)
    image = resize_image(image, new_width)
    return pixels_to_ascii(image)


ASCII_CHARS = ["@"]



try:
    if len(sys.argv) < 2:
        raise AttributeError
    path = find(sys.argv[1], "./videos/")

    ffmpeg_command = [
        "ffmpeg",
        "-i", path,
        "-vf", "scale=160:-1,fps=15",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-an",
        "pipe:1"
    ]

    frame_width, frame_height = 160, 90
    frame_size = frame_width * frame_height * 3

    process = subprocess.Popen(
        ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    last_height = 0
    last_width = 0
    while True:
        frame = process.stdout.read(frame_size)
        if len(frame) != frame_size:
            break

        frame_np = np.frombuffer(frame, np.uint8).reshape(
            (frame_height, frame_width, 3))
        image = Image.fromarray(frame_np)

        terminal_width, terminal_height = shutil.get_terminal_size()
        ascii_frame = image_to_ascii(image, terminal_width)

        sys.stdout.write("\033[H")
        sys.stdout.write(ascii_frame)

        if ((last_height != terminal_height ) | (last_width != terminal_width)):
            last_height = terminal_height
            last_width = terminal_width
            sys.stdout.write("\033c")
  
         

        time.sleep(0.057)
    os.system('cls||clear')
except AttributeError:
    print("Hey insert something, don't expect the code to work for you like I did with ChatGPT")
except IndexError:
    print("Damn i fucked up")
except ValueError:
    print("Please enter a valid option... you have the GitHub right there to check...")
except KeyboardInterrupt:
    os.system('cls||clear')
