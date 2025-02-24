import shutil
import subprocess
import sys
from PIL import Image
import time
import os
import numpy as np
import platform

width = 95
height = 70
dictSongs = {"ditto": "Km71Rr9K-Bw",
             "eta": "s4Ow55AbdCg", "hype_boy2": "S4UEJePR0UE", "hype_boy_mv": "11cta61wi0g", "how_sweet":"Q3K0TOvTOno"}


def get_youtube_stream_url(video_url):
    try:

        yt_dlp_command = [
            "yt-dlp",
            "--extractor-args", "youtube:player_client=android",
            "--cache-dir", "~/.cache/yt-dlp",
            "-f", "best[height<=480]",
            "-g", video_url
        ]
        process = subprocess.run(
            yt_dlp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        streaming_url = process.stdout.strip()
        if not streaming_url.startswith("http"):
            raise ValueError(f"Error: No se pudo obtener la URL de streaming. Salida: {process.stderr}")
        return streaming_url
    except Exception as e:
        print(f"Error obteniendo el stream de YouTube: {e}")
        sys.exit(1)


def process_video_with_ffmpeg(stream_url):
    frame_width, frame_height = 160, 90
    frame_size = frame_width * frame_height * 3

    ffmpeg_command = [
        "ffmpeg",
        "-i", stream_url,
        "-vf", "scale=160:-1,fps=15",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-an",
        "pipe:1"
    ]

    process = subprocess.Popen(
        ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8
    )

    last_height, last_width = 0, 0

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

        if (last_height != terminal_height) or (last_width != terminal_width):
            last_height = terminal_height
            last_width = terminal_width
            sys.stdout.write("\033c")

        time.sleep(0.057)


def resize_image(image, new_width):
    orig_width, orig_height = image.size
    ratio = orig_height / orig_width
    new_height = int(new_width * ratio * 0.55)
    return image.resize((new_width, new_height))


def pixels_to_ascii(image):
    ASCII_CHARS = ["@"]
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


def image_to_ascii(image, terminal_width, max_width=width):

    new_width = min(terminal_width, max_width)
    image = resize_image(image, new_width)
    return pixels_to_ascii(image)


try:
    if len(sys.argv) < 2:
        raise AttributeError(
            "Hey, inserta algo, no esperes que haga todo por ti.")
    yt_id = dictSongs.get(sys.argv[1])
    if not yt_id:
        raise ValueError("Video no encontrado en la lista.")
    video_url = f"https://www.youtube.com/watch?v={yt_id}"
    stream_url = get_youtube_stream_url(video_url)
    process_video_with_ffmpeg(stream_url)
except AttributeError:

    print("Hey insert something, don't expect the code to work for you like I did with ChatGPT")
except IndexError:
    print("Damn i fucked up")
except ValueError:
    print("Please enter a valid option... you have the GitHub right there to check...")
except KeyboardInterrupt:
    if(platform.uname().system.lower()=="linux"):
        os.system('clear')
    else:
        os.system('cls')

