# coding=utf-8
"""
TEXT MENU
Menu with text and buttons.

The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Library import
from pygameMenu.menu import Menu
import pygameMenu.config_textmenu as _cfg
import pygame as _pygame


# noinspection PyProtectedMember
class TextMenu(Menu):
    """
    Text menu object.
    """

    def __init__(self,
                 surface,
                 window_width,
                 window_height,
                 font,
                 title,
                 draw_text_region_x=_cfg.TEXT_DRAW_X,
                 text_centered=_cfg.TEXT_CENTERED,
                 text_color=_cfg.TEXT_FONT_COLOR,
                 text_fontsize=_cfg.MENU_FONT_TEXT_SIZE,
                 text_margin=_cfg.TEXT_MARGIN,
                 **kwargs
                 ):
        """
        TextMenu constructor.

        :param draw_text_region_x: X-Axis drawing region of the text
        :param font: Font file direction
        :param kwargs: Aditional parameters
        :param surface: Pygame surface object
        :param text_centered: Indicate if text is centered
        :param text_color: Text color
        :param text_fontsize: Text font size
        :param text_margin: Line margin
        :param title: Title of the Menu
        :param window_height: Window height
        :param window_width: Window width
        :type draw_text_region_x: int
        :type font: str
        :type text_centered: bool
        :type text_color: tuple
        :type text_fontsize: int
        :type text_margin: int
        :type title: str
        :type window_height: int
        :type window_width: int
        """
        assert isinstance(draw_text_region_x, int)
        assert isinstance(text_centered, bool)
        assert isinstance(text_fontsize, int)
        assert isinstance(text_margin, int)
        assert draw_text_region_x >= 0, 'X-Axis drawing region of the text must be greater than zero'
        assert text_fontsize > 0, 'Text font size must be greater than zero'
        assert text_margin >= 0, 'Text margin must be greater or equal than zero'

        # Super call
        super(TextMenu, self).__init__(surface, window_width, window_height,
                                       font, title, **kwargs)

        # Store configuration
        self._centered_text = text_centered
        self._draw_text_region_x = draw_text_region_x
        self._font_textcolor = text_color
        self._font_textsize = text_fontsize
        self._textdy = text_margin

        # Load font
        self._fonttext = _pygame.font.Font(font, self._font_textsize)

        # Inner variables
        self._text = []

        # Position of text
        self._pos_text_x = int(self._width * (self._draw_text_region_x / 100.0)) + self._posy
        self._opt_posy -= self._textdy / 2 + self._font_textsize / 2

    def add_line(self, text):
        """
        Add line of text.

        :param text: Line text
        :type text: str
        :return: None
        """
        assert isinstance(text, str)

        text = text.strip()
        self._text.append(text)
        dy = -self._font_textsize / 2 - self._textdy / 2
        self._opt_posy += dy

    def add_option(self, element_name, element, *args):
        """
        Add option to menu.

        :param element_name: Name of the element
        :param element: Menu object
        :param args: Aditional arguments
        :type element_name: basestring
        :type element: Menu, _locals._PymenuAction
        :return: None
        """
        if self._size <= 1:
            dy = -self._fsize / 2 - self._opt_dy / 2
            self._opt_posy += dy
        super(TextMenu, self).add_option(element_name, element, *args)

    def draw(self):
        """
        Draw menu on surface.

        :return: None
        """
        super(TextMenu, self).draw()

        # Draw text
        dy = 0
        for linea in self._text:
            text = self._fonttext.render(linea, 1, self._font_textcolor)
            text_width = text.get_size()[0]
            if self._centered_text:
                text_dx = -int(text_width / 2.0)
            else:
                text_dx = 0
            ycoords = self._opt_posy + self._textdy + dy * (self._font_textsize + self._textdy)
            ycoords -= self._font_textsize / 2

            self._surface.blit(text, (self._pos_text_x + text_dx, ycoords))
            dy += 1

    def _get_option_pos(self, index):
        """
        Get option position from the option index.

        :param index: Option index
        :type index: int
        :return: None
        """
        dysum = len(self._text) * (self._font_textsize + self._textdy)
        dysum += 2 * self._textdy + self._font_textsize

        rect = self._option[index].get_rect()
        if self._centered_option:
            text_dx = -int(rect.width / 2.0)
        else:
            text_dx = 0
        t_dy = -int(rect.height / 2.0)

        xccord = self._opt_posx + text_dx
        ycoord = self._opt_posy + index * (self._fsize + self._opt_dy) + t_dy + dysum

        return xccord, ycoord
