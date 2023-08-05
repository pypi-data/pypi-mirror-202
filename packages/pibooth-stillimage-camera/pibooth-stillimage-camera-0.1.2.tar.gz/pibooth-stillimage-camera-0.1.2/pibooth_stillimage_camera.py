"""Plugin to fake a camera, and present a still image, if debug is enabled.

You can customize the foreground and background color, however useless that may seem.

Licensed using the AGPLv3, see LICENSE

Author: Gilles Pietri <gilles@wolface.fr>

"""

import random
import time
from PIL import Image, ImageDraw
import pygame

import pibooth

from pibooth.utils import LOGGER
from pibooth import fonts
from pibooth.camera.base import BaseCamera

__version__ = "0.1.0"

class SiCamera(BaseCamera):
    """Dummy camera, showing a still image, for tests"""
    def __init__(self, camera_proxy=None, background_color='pink', foreground_color='black'):
        self.dummy_text = "Still image for tests"
        self.dummy_background = background_color
        self.dummy_foreground = foreground_color
        LOGGER.info("new dummy SiCamera instance")
        super().__init__(camera_proxy)

    def _generate_still_image(self):
        size = self.resolution
        dummy_font = fonts.get_pil_font(
                self.dummy_text,
                fonts.CURRENT,
                0.5 * size[0],
                0.5 * size[1]
                )
        dummy = Image.new('RGB', size, self.dummy_background)
        position = random.randint(0, size[1])
        textimg = ImageDraw.Draw(dummy)
        textimg.text((10,position), self.dummy_text, self.dummy_foreground, dummy_font)

        return dummy

    def preview(self, window, flip=True):
        """Preview: display a blank image"""
        self._window = window
        rect = self.get_rect()
        still = self._generate_still_image()
        preview =  still.resize(rect.size)
        self._window.show_image(preview)
        pygame.display.update()

    def preview_wait(self, timeout, alpha=60):
        """No need for implementation (but there could be a base implementation though)"""

    def preview_countdown(self, timeout, alpha=60):
        """Countdown: just wait"""
        time.sleep(timeout)

    def stop_preview(self):
        """Stop Preview: do nothing"""


    def capture(self, effect=None):
        """Simulate capture, return path to still image"""
        self._captures.append(self._generate_still_image())

    def _post_process_capture(self, capture_data):
        """Rework and return a PIL Image object from capture data.
        """
        image = capture_data
        return image

    def quit(self):
        """Do nothing when quitting"""

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Add 2 config options for foreground and background color"""
    cfg.add_option('CAMERA', 'dummy_background', 'pink', 'Background of the dummy still images')
    cfg.add_option('CAMERA', 'dummy_foreground', 'black', 'Foreground of the dummy still images')

@pibooth.hookimpl
def pibooth_setup_camera(cfg):
    """Return a SiCamera instance for pibooth to use, if debug is enabled"""
    LOGGER.info("Hello from '%s' plugin", __name__)
    if cfg.getboolean('GENERAL', 'debug'):
        bg_color = cfg['CAMERA'].get('dummy_background', 'pink')
        fg_color = cfg['CAMERA'].get('dummy_foreground', 'black')
        return SiCamera(background_color=bg_color,foreground_color=fg_color)
    return None
