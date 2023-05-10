# Comforticons
This package is an identicon generation module for different identicon/icon/gravatar/avatar flavors.

See **[libravatar project](https://www.libravatar.org/)** and **[gravatar project](https://gravatar.com/)**.

This module is heavly inspired by **[bitverseio's PHP Identicon Generator](https://github.com/bitverseio/identicon)** architecture/generators and **[azaghal's pydenticon package](https://github.com/azaghal/pydenticon)** (gravatar retro-like identicon generator).

## Source

[Link to source](https://github.com/blackwarlow/comforticons).

## Requirements
* Python 3.8+
  * pillow 9.5+

## Installation
This module is available on [pypi.org](https://pypi.org/).

[![Newest PyPi version](https://img.shields.io/pypi/v/comforticons.svg)](https://pypi.org/project/comforticons/)
```
pip install comforticons
```

## Features

* Modular Identicon factory architecture
  > `preprocessors` list and `generator` class powered identicon generation
* Abstract/Interface implementations for data preprocessor and identicon generator
* Pillow 9.5+ support
* MyPy typings support

## Roadmap
* [ ] ASCII-denticon generation in [this package](comforticons/generators/text.py).
* [ ] SVG support for [ring identicon](https://github.com/bitverseio/identicon/blob/master/src/Bitverse/Identicon/Generator/RingsGenerator.php) in [this package](comforticons/generators/image.py) with **[svglib project](https://pypi.org/project/svglib/)**.
* [ ] More programmer-friendly generator architecture (choose return type - PIL.Image, bytes), (direct writing to file).
* [ ] [Django](https://djangoproject.com/) integration.
* [ ] Self-hosting solution for small ecosystems with FastAPI.
* [ ] Custom error classes implementation.

## Usage

### Interactive
```
python3 -m comforticons
```

### Basic

```py
from comforticons import Identicon

# Customize preprocessors and generator settings here
generator = Identicon()

# This will generate 120x120 with 0 padding PNG identicon
# with transparent background 5x5 pixel identicon (retro gravatar)
# using PixelGenerator and MD5Preprocessor as default
identicon = generator.generate("provide data here")

# Save to file
with open("image.png", "wb") as file:
    file.write(identicon)
```

### Advanced

```py
from comforticons import Identicon
from comforticons.preprocessors.hash import * # *Preprocessor
from comforticons.generators.image import * # PixelGenerator

# Customize preprocessors and generator settings here
generator = Identicon(
    # First, process data with md5, then with sha1
    preprocessors = [MD5Preprocessor(), SHA1Preprocessor],
    generator = PixelGenerator(
        size = 10, # 10x10 grid
        foreground_colors = ["#ffffff"], # Only use white foreground
        background = "#000000", # black, non-transparent background
        image_format = "png",   # PNG image format
        invert = True,          # This will swap bg-fg colors
    )
)

# Actually generate identicon
identicon = generator.generate("provide data here")

# Save to file
with open("image.png", "wb") as file:
    file.write(identicon)
```

## Examples
> `MD5Preprocessor` + `PixelGenerator`<br>
> "identicon"<br>
> ![identicon](docs/md5.png)

> `SHA1Preprocessor` + `PixelGenerator`<br>
> "identicon"<br>
> ![identicon](docs/sha1.png)

## Licensing

See [LICENCE](LICENCE).

Also see [this LICENCE](LICENCE2).