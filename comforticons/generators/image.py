"""Image icon generators module"""
from __future__ import annotations

import io
from typing import Literal

from PIL import Image, ImageDraw

from .base import BaseGenerator


"""HTML named colors list"""
HTML_COLORS = [
    "#F0F8FF",
    "#FAEBD7",
    "#00FFFF",
    "#7FFFD4",
    "#F0FFFF",
    "#F5F5DC",
    "#FFE4C4",
    "#000000",
    "#FFEBCD",
    "#0000FF",
    "#8A2BE2",
    "#A52A2A",
    "#DEB887",
    "#5F9EA0",
    "#7FFF00",
    "#D2691E",
    "#FF7F50",
    "#6495ED",
    "#FFF8DC",
    "#DC143C",
    "#00FFFF",
    "#00008B",
    "#008B8B",
    "#B8860B",
    "#A9A9A9",
    "#006400",
    "#BDB76B",
    "#8B008B",
    "#556B2F",
    "#FF8C00",
    "#9932CC",
    "#8B0000",
    "#E9967A",
    "#8FBC8F",
    "#483D8B",
    "#2F4F4F",
    "#00CED1",
    "#9400D3",
    "#FF1493",
    "#00BFFF",
    "#696969",
    "#1E90FF",
    "#B22222",
    "#FFFAF0",
    "#228B22",
    "#FF00FF",
    "#DCDCDC",
    "#F8F8FF",
    "#FFD700",
    "#DAA520",
    "#808080",
    "#008000",
    "#ADFF2F",
    "#F0FFF0",
    "#FF69B4",
    "#CD5C5C",
    "#4B0082",
    "#FFFFF0",
    "#F0E68C",
    "#E6E6FA",
    "#FFF0F5",
    "#7CFC00",
    "#FFFACD",
    "#ADD8E6",
    "#F08080",
    "#E0FFFF",
    "#FAFAD2",
    "#D3D3D3",
    "#90EE90",
    "#FFB6C1",
    "#FFA07A",
    "#20B2AA",
    "#87CEFA",
    "#778899",
    "#B0C4DE",
    "#FFFFE0",
    "#00FF00",
    "#32CD32",
    "#FAF0E6",
    "#FF00FF",
    "#800000",
    "#66CDAA",
    "#0000CD",
    "#BA55D3",
    "#9370D8",
    "#3CB371",
    "#7B68EE",
    "#00FA9A",
    "#48D1CC",
    "#C71585",
    "#191970",
    "#F5FFFA",
    "#FFE4E1",
    "#FFE4B5",
    "#FFDEAD",
    "#000080",
    "#FDF5E6",
    "#808000",
    "#6B8E23",
    "#FFA500",
    "#FF4500",
    "#DA70D6",
    "#EEE8AA",
    "#98FB98",
    "#AFEEEE",
    "#D87093",
    "#FFEFD5",
    "#FFDAB9",
    "#CD853F",
    "#FFC0CB",
    "#DDA0DD",
    "#B0E0E6",
    "#800080",
    "#FF0000",
    "#BC8F8F",
    "#4169E1",
    "#8B4513",
    "#FA8072",
    "#F4A460",
    "#2E8B57",
    "#FFF5EE",
    "#A0522D",
    "#C0C0C0",
    "#87CEEB",
    "#6A5ACD",
    "#708090",
    "#FFFAFA",
    "#00FF7F",
    "#4682B4",
    "#D2B48C",
    "#008080",
    "#D8BFD8",
    "#FF6347",
    "#40E0D0",
    "#EE82EE",
    "#F5DEB3",
    "#FFFFFF",
    "#F5F5F5",
    "#FFFF00",
    "#9ACD32",
]


class PixelGenerator(BaseGenerator):
    """Pixel square grid identicon generator (gravatar "retro" type)

    Generated avatars are images of requested `avatar_size` with optional `padding`. The
    avatar (without padding) consists out of `size blocks, laid out in a square, where M is the number of blocks in each column, while N is number
    of blocks in each row.

    Each block is a small rectangle on its own, filled using the foreground or
    background color.

    The foreground is picked randomly, based on the passed data, from the list
    of foreground colours set during initialisation of the generator.

    The blocks are always laid-out in such a way that the identicon will be
    symterical by the Y (vertical) axis. The center of symetry will be the central column
    of blocks if `size` is odd or division between two center columns if `size` is even.

    Simply put, the generated identicons are small symmetric mosaics with
    optional padding.

    :ivar size: avatar features size
    :ivar entropy: required entropy
    """

    def __init__(
        self,
        size: int = 5,
        foreground_colors: list[str] = HTML_COLORS,
        background: str = "#00000000",
        image_format: Literal["png", "jpeg", "jpg"] = "png",
        invert: bool = False,
    ):
        """Constructor

        Required entropy calculation: ceil(size / 2) * size + 8

        :param size: avatar features size, defaults to 5
        :type size: int, optional
        :param foreground_colors: list of hex background color strings, defaults to
        :type foreground_colors: list[str], optional
        :param background: hex background color string, defaults to "#00000000" - transparent black
        :type background: str, optional
        :param invert: invert foreground and background colors, defaults to False
        :type invert: bool, optional
        """
        super().__init__(size)
        self.entropy = (
            self.size // 2 + self.size % 2
        ) * self.size + 8  # Y axis symmetry + 8 bits for color selection
        self.foreground_colors = foreground_colors
        self.background = background
        self.format = image_format
        self.invert = invert

    def _data_to_byte_list(self, data: str) -> list[int]:
        """Convert incoming data string (hopefully hexdigest of hash function) to list of int bytes

        Parses every two characters of `data` string as hex number and converts it to int 0-255 (byte).

        :param data: base data for generation
        :type data: str
        :return: list of integers 0-255 (byte)
        :rtype: list[int]
        """
        return [int(data[i * 2 : i * 2 + 2], 16) for i in range(len(data) // 2)]

    def _get_bit(self, n: int, data: list[int]) -> bool:
        """Get bit from data byte list

        Determines if the n-th bit of passed bytes is 1 or 0.

        :param data: list of byte (int 0-255) values for which the n-th bit value should be checked
        :type data: list[int]
        :param n: bit number of data list that should be checked
        :type n: int
        :return: True if the bit is 1. False if the bit is 0
        :rtype: bool
        """

        return data[n // 8] >> int(8 - ((n % 8) + 1)) & 1 == 1

    def generate(self, data: str, avatar_size: int = 120, padding: int = 0) -> bytes:
        """Generate pixel identicon

        :param data: avatar data
        :type data: str
        :param avatar_size: generated square avatar dimensions
        :type avatar_size: int
        :param padding: generated square avatar dimensions
        :type avatar_size: int
        :return: bytes of generated avatar encoded by PIL in `image_format`
        :rtype: bytes
        """

        """
            Copyright (c) 2013, Branko Majic
            All rights reserved.

            Redistribution and use in source and binary forms, with or without modification,
            are permitted provided that the following conditions are met:

            Redistributions of source code must retain the above copyright notice, this
            list of conditions and the following disclaimer.

            Redistributions in binary form must reproduce the above copyright notice, this
            list of conditions and the following disclaimer in the documentation and/or
            other materials provided with the distribution.

            Neither the name of Branko Majic nor the names of any other
            contributors may be used to endorse or promote products derived from
            this software without specific prior written permission.

            THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
            ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
            WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
            DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
            ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
            (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
            LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
            ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
            (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
            SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        """

        data = self._data_to_byte_list(data)

        background, foreground = (
            self.background,
            self.foreground_colors[
                data[0] % len(self.foreground_colors)
            ],  # Select foreground color
        )
        # Swap selected colors
        if self.invert:
            background, foreground = foreground, background

        image = Image.new(
            "RGB"
            if self.format.lower() in ("jpg", "jpeg")
            else "RGBA",  # Account for non-transparent jp(e)g images
            (avatar_size + padding * 2,) * 2,
            background,
        )

        draw = ImageDraw.Draw(image)

        # Initialise the matrix (list of rows) that will be returned.
        matrix = [[False] * self.size for _ in range(self.size)]

        # Process the cells one by one.

        # Since the identicon needs to be symmetric, we'll need to work on half
        # the columns (rounded-up), and reflect where necessary.
        for cell in range(self.size * (self.size // 2 + self.size % 2)):
            # If the bit from hash correpsonding to this cell is 1, mark the
            # cell as foreground one. Do not use first byte (since that one is
            # used for determining the foreground colour.
            if self._get_bit(cell, data[1:]):
                # Determine the cell coordinates in matrix.
                column = cell // self.size
                row = cell % self.size

                # Mark the cell and its reflection. Central column may get
                # marked twice, but we don't care.
                matrix[row][column] = True
                matrix[row][self.size - column - 1] = True

        block_size = avatar_size // self.size
        # Go through all the elements of a matrix, and draw the rectangles.
        for row, row_columns in enumerate(matrix):
            for column, cell in enumerate(row_columns):
                if cell:
                    # Set-up the coordinates for a block.
                    x1 = padding + column * block_size
                    y1 = padding + row * block_size
                    x2 = padding + (column + 1) * block_size - 1
                    y2 = padding + (row + 1) * block_size - 1

                    # Draw the rectangle.
                    draw.rectangle((x1, y1, x2, y2), fill=foreground)

        # Set-up a stream where image will be saved.
        stream = io.BytesIO()

        # Save the image to stream.
        try:
            image.save(stream, format=self.format, optimize=True)
        except KeyError:
            raise ValueError(
                "Pillow does not support requested image format: %s" % self.format
            )
        image_raw = stream.getvalue()
        stream.close()

        # Return the resulting image bytes.
        return image_raw


__all__ = ["PixelGenerator"]
