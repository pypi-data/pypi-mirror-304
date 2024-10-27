
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

```
pip install glfy
```

## Usage

After installing, you can use the GLFY tool from the command line or in a Python script.

### Command Line Usage

To convert an image to ASCII art:

```
glfy image path/to/image.jpg
```

To convert a video to ASCII art:

```
glfy video path/to/video.mp4
```

To start live video ASCII conversion:

```
glfy live
```

## Customizable Parameters

- **Brightness**: Adjusts the brightness of the ASCII output.
- **Contrast**: Adjusts the contrast of the ASCII output.
- **Vibrancy**: Adjusts the color saturation of the ASCII output.
- **Gamma**: Adjusts the gamma correction of the ASCII output.
- **Horizontal & Vertical Spacing**: Defines the spacing between ASCII characters.

## License

This project is released under the MIT License.
