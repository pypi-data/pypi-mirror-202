# Images to GIF Converter

## Table of Contents
  + [Installation](#installation)
  + [Quick start](#quick-start)
  + [Features](#features)

<br>

## Installation

Download the package using pip from PyPI.
```bash
$ pip install img2gif_aijinsol --upgrade
```

Alternatively, you can also intall the package as follows.
```bash
$ pip install git+https://github.com/aijinsol/img2gif.git
```
Note: `Mac` or `homebrew` users may need to use `pip3`.

<br>

## Quick start
```python
 >>> from img2gif_aijinsol.converter import GifConverter
 >>> c = GifConverter(${IMG_PATH}, ${GIF_PATH}, ${IMG_SIZE}, ${DURATION})
 >>> c.convert()
```

<br>

## Features
  + A Python library for converting single or multiple-frame GIF images.
  + OpenCV does not support GIF images.