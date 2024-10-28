# GLFY Tool

GLFY is a versatile tool that converts videos, images, and live streams into ASCII art. It supports various processing modes, including live video capture, virtual camera streaming, and screen capturing. The tool is designed to be efficient and customizable, making it ideal for artistic and fun applications.

## Features

- Convert Videos to ASCII Art: Converts video files into ASCII art video files.
- Convert Images to ASCII Art: Converts image files into ASCII art images.
- Live Video ASCII Conversion: Captures live video from your webcam and displays it as ASCII art.
- Virtual Camera Support: Streams ASCII art to a virtual camera, making it compatible with various video applications.
- Screen Capture: Streams your screen as ASCII art in real-time.
- Customizable Parameters: Adjust brightness, contrast, vibrancy, gamma, and more to fine-tune the ASCII art output.

## Installation

Install GLFY directly from PyPI:

pip install glfy

## Usage

After installing, you can use the GLFY tool directly from the command line or within a Python script, similar to tools like `ffmpeg`.

### Command Line Usage

To convert an image to ASCII art:

glfy image path/to/image.jpg

To convert a video to ASCII art:

glfy video path/to/video.mp4

To start live video ASCII conversion:

glfy live

### Python Script Usage

If you want to use GLFY's CLI from within a Python script, you can do so using the `subprocess` module:

```python
import subprocess

# Example: Convert an image to ASCII art using the CLI
subprocess.run(['glfy', 'image', 'path/to/image.jpg'])

# Example: Convert a video to ASCII art using the CLI
subprocess.run(['glfy', 'video', 'path/to/video.mp4'])

# Example: Start live video ASCII conversion using the CLI
subprocess.run(['glfy', 'live'])
