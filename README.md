
# New ASCII

This script allows to visualize the new jeans mvs in the terminal using ASCII art frame by frame. it uses `ffmpeg` to stream the video, and Pillow for image processing, rendering each frame as ASCII characters with color.

## Features

* Convert MV video to ASCII in real-time.
* Supports streaming via `ffmpeg` after having the video on the folder videos.
* The ASCII art is colored according to the video frame’s RGB values.
* Also the video is responsive to the side of the terminal, but don't make the terminal like 1x1 please is not that god of a code.

## Requirements

Make sure you have the following dependencies installed:
* Docker Desktop 
* WSL (optional but runs better and faste i don't know why)

To install the required python libraries: 

`docker build -t [name you want for the image] .`

Please run the command on the same folder as the project

## Usage

* Clone the repository or download the script.
* Run the build `docker build -t [name you want for the image] .`
* Run the code `docker run -it [name you selected for the image or id of the docker image]`

### Name problems
* if the name has whitespaces please use _ on the name  
* if you want to use an example run this command `python3 | python | py new_ascii.py ditto`
The script will process the video and display it in ASCII art format in your terminal.

# Goals

- [x]  Make it a terminal script without requiring users to download or install dependencies  
- [x]  Stream the video directly from YouTube instead of using local files  
- [ ]  Host it online to avoid needing to download the repository  
- [ ]  Better way to select videos