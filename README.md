
# New ASCII

This script allows to visualize the new jeans mvs in the terminal using ASCII art frame by frame. it uses `ffmpeg` to stream the video, and Pillow for image processing, rendering each frame as ASCII characters with color.

## Features

* Convert MV video to ASCII in real-time.
* Supports streaming via `ffmpeg` after having the video on the folder videos.
* The ASCII art is colored according to the video frame’s RGB values.
* Also the video is responsive to the side of the terminal, but don't make the terminal like 1x1 please is not that god of a code.

## Requirements

Make sure you have the following dependencies installed:
* Python 3.x.
* `ffmpeg` (installed on your system).
* `Pillow` library (for image manipulation).
* `numpy` library.

To install the required python libraries: 

`pip install pillow numpy` or `pip install -r requirements.txt`

Also, make sure you have ffmpeg installed. You can download it from in [ffmpeg](https://www.ffmpeg.org/download.html) official site.

## Usage

* Clone the repository or download the script.
* Install the [dependencies](#requirements) (you can try and use WSL it works pretty well to install the dependencies)
* Place the video you want to conver to ASCII in the `./videos/` directory
* Run the script with the followin command, providing the name of the video (without the `.webm` extension. right now only works with webm because is the initialization of the project, you can try with the video that comes in the github) 
`python3 | python | py new_ascii.py [name of the video]`  
## Name problems
* if the name has whitespaces please use _ on the name  
* if you want to use an example run this command `python3 | python | py new_ascii.py ditto`
The script will process the video and display it in ASCII art format in your terminal.


# Troubleshooting
* Ensure `ffmpeg` is correctly installed and added to your system's PATH

# Goals

* Make it a terminal script without making the people download or install dependencies
* Stream the video directly from youtube instead of having it in a folder
