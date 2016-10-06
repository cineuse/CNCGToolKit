#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

"""
    Generates default avatars from a given string (such as username).

    Usage:

    >>> from avatar_generator import Avatar
    >>> photo = Avatar.generate(128, "example@sysnove.fr", "PNG")
"""

import os
import re
from random import randint, seed
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

__all__ = ['Avatar']


class Avatar(object):
    FONT_COLOR = (255, 255, 255)
    MIN_RENDER_SIZE = 128

    @classmethod
    def generate(cls, size, string, filetype="JPEG"):
        """
            Generates a squared avatar with random background color.

            :param size: size of the avatar, in pixels
            :param string: string to be used to print text and seed the random
            :param filetype: the file format of the image (i.e. JPEG, PNG)
        """
        render_size = max(size, Avatar.MIN_RENDER_SIZE)
        image = Image.new('RGB', (render_size, render_size),
                          cls._background_color(string))
        draw = ImageDraw.Draw(image)
        # font = cls._font(render_size)
        font = ImageFont.load_default()
        text = cls._text(string)
        draw.text(cls._text_position(render_size, text, font),
                  text,
                  fill=cls.FONT_COLOR,
                  font=font)
        stream = BytesIO()
        image = image.resize((size, size), Image.ANTIALIAS)
        image.save(stream, format=filetype, optimize=True)
        return stream.getvalue()

    @staticmethod
    def _background_color(s):
        """
            Generate a random background color.
            Brighter colors are dropped, because the text is white.

            :param s: Seed used by the random generator
            (same seed will produce the same color).
        """
        seed(s)
        r = v = b = 255
        while r + v + b > 255 * 2:
            r = randint(0, 255)
            v = randint(0, 255)
            b = randint(0, 255)
        return (r, v, b)

    @staticmethod
    def _font(size):
        """
            Returns a PIL ImageFont instance.

            :param size: size of the avatar, in pixels
        """
        path = os.path.join(os.path.dirname(__file__), 'data',
                            "Inconsolata.otf")
        return ImageFont.truetype(path, size=int(0.8 * size))

    @staticmethod
    def _text(string):
        """
            Returns the text to draw.
        """
        if len(string) == 0:
            return "#"
        else:
            # if text like : Hello return HO
            # if text like : HelloWorld return HW
            # if text like : Hello_World return HW
            # if text like : hello_builtiful_world return HB
            if "_" in string:
                str_list = string.split("_")
            elif len(re.findall(r"[A-Z]", string)) >= 2:
                str_list = re.findall(r"[A-Z]", string)
            else:
                str_list = [string, string[-1]]
            # get 2 letters
            letters = "%s%s" % (str_list[0][0], str_list[1][0])
            return letters.upper()

    @staticmethod
    def _text_position(size, text, font):
        """
            Returns the left-top point where the text should be positioned.
        """
        width, height = font.getsize(text)
        left = (size - width) / 2.0
        # I just don't know why 5.5, but it seems to be the good ratio
        top = (size - height) / 5.5
        return left, top
