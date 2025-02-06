import subprocess
import sys
from PIL import Image
import time
import os
import numpy as np


def find(name, path):
    for root, _, files in os.walk(path):
        name = name + ".webm"
        if name in files:
            return os.path.join(root, name)
    raise ValueError


def resize_image(image, new_width):
    orig_width, orig_height = image.size
    ratio = orig_height / orig_width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def pixels_to_ascii_colored(image):
    image = image.convert("RGB")
    pixels = np.array(image)
    ascii_image = ""

    for row in pixels:
        for pixel in row:
            if isinstance(pixel, np.ndarray) and len(pixel) == 3:
                r, g, b = pixel
            else:
                r, g, b = 255, 255, 255

            brightness = int((r + g + b) / 3)
            char = ASCII_CHARS[brightness * len(ASCII_CHARS) // 256]

            ascii_image += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        ascii_image += "\n"

    return ascii_image


def image_to_ascii(frame):
    frame = resize_image(frame, new_width=width)
    return pixels_to_ascii_colored(frame)


def clear_screen():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()


try:
    if len(sys.argv) < 2:
        raise AttributeError
    path = find(sys.argv[1], "./videos/")
    print(path)

    ASCII_CHARS = list(
        "@#%WM&8B$O0QbdpqwmZOQLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

    width = 85
    height = 50

    ffmpeg_command = [
        "ffmpeg",
        "-i", path,
        "-vf", "scale=160:-1,fps=15",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-an",
        "pipe:1"
    ]

    frame_width = 160
    frame_height = 90
    frame_size = frame_width * frame_height * 3

    process = subprocess.Popen(
        ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        frame = process.stdout.read(frame_size)

        if len(frame) != frame_size:
            break

        frame_np = np.frombuffer(frame, np.uint8).reshape(
            (frame_height, frame_width, 3))

        image = Image.fromarray(frame_np)
        ascii_frame = image_to_ascii(image)

        clear_screen()
        sys.stdout.write(ascii_frame)

        time.sleep(0.07)

    process.stdout.close()
    process.stderr.close()
    os.system('cls||clear')
    process.wait()
except AttributeError:
    print("Hey insert something, don't expect the code to work for you like I did with ChatGPT")
except IndexError:
    print("Damn i fucked up")
except ValueError:
    print("Please enter a valid option... you have the GitHub right there to check...")
except KeyboardInterrupt:
    os.system('cls||clear')
