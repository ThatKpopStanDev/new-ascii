import subprocess
import sys
from PIL import Image
import time
import os
import numpy as np
import http.server
import socketserver
import time

import urllib

width = 95
height = 70
dictSongs = {"ditto": "Km71Rr9K-Bw",
             "eta": "s4Ow55AbdCg", "hype_boy2": "S4UEJePR0UE", "hype_boy_mv": "11cta61wi0g", "how_sweet": "Q3K0TOvTOno"}


def clear_console():
    os.system("clear" if os.name != "nt" else "cls")


CLEAR_SCREEN = "\033[H\033[J"


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
            raise ValueError(
                f"Error: No se pudo obtener la URL de streaming. Salida: {process.stderr}")
        return streaming_url
    except Exception as e:
        print(f"Error obteniendo el stream de YouTube: {e}")
        sys.exit(1)


def process_video_with_ffmpeg(stream_url, width_parameter):
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

    while True:
        frame = process.stdout.read(frame_size)
        if len(frame) != frame_size:
            break
        frame_np = np.frombuffer(frame, np.uint8).reshape(
            (frame_height, frame_width, 3))
        image = Image.fromarray(frame_np)
        ascii_frame = image_to_ascii(image, terminal_width=width_parameter)
        yield ascii_frame
        time.sleep(0.055)


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


class AsciiServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlsplit(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)

        query_values = query.get("song", [])
        size_values = query.get("size", [])

        if len(query_values) == 0 or len(size_values) == 0:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(
                "Error: Missing song or size parameter.\n".encode())
            return

        song_name = query_values[0]
        terminal_size = int(size_values[0])
        yt_id = dictSongs.get(query_values[0])
        if not yt_id:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(
                f"Error: Song '{song_name}' not found.\n".encode())
            return

        video_url = f"https://www.youtube.com/watch?v={yt_id}"
        stream_url = get_youtube_stream_url(video_url)

        try:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            self.wfile.write(CLEAR_SCREEN.encode())
            self.wfile.flush()

            for frame in process_video_with_ffmpeg(stream_url, terminal_size):
                try:
                    self.wfile.write(frame.encode())
                    self.wfile.write(b"\033[H")
                    self.wfile.flush()
                except BrokenPipeError:
                    print("Error: Broken pipe, cliente desconectado.")
                    self.wfile.flush()
                    self.wfile.write(b"clear" if os.name != "nt" else "cls")
                    break
                except Exception as e:
                    self.wfile.flush()
                    self.wfile.write(b"clear" if os.name != "nt" else "cls")
                    print(f"Error inesperado al enviar datos: {e}")
                    break

        except BrokenPipeError:
            print("Cliente desconectado antes de recibir todos los datos.")
            self.wfile.write(CLEAR_SCREEN.encode())
            self.wfile.flush()
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}\n".encode())
        finally:
            self.wfile.write(CLEAR_SCREEN.encode())
            self.wfile.flush()


PORT = 8080


def run_server():
    PORT = 8080
    with socketserver.TCPServer(("", PORT), AsciiServer) as httpd:
        print(f"Servidor HTTP corriendo en el puerto {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nInterrupción recibida, limpiando y cerrando el servidor.")
            clear_console()
            sys.exit(0)


if __name__ == "__main__":
    run_server()
