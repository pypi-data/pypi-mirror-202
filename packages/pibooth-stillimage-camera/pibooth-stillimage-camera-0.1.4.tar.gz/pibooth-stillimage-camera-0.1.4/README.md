# pibooth-stillimage-camera

`pibooth-stillimage-camera` is a plugin for the [pibooth](https://pypi.org/project/pibooth) application.

It provides a fake camera 'capturing' still images with a dummy text 'Still image for tests' writen in a customizable color, and background color.

It has no use in a real booth scenario, but this way anyone can test the app, even whithout having an actual camera attached!

This project was mostly a first try at cracking at pibooth using a plugin, so as to see how easy it is to interact with it, and try to provide feedback on the general structure of the project. It also actually enables testing of all the other parts without much work!

## Install

This plugin is published on Pypi, so you can use: `$ pip3 install pibooth-stillimage-camera`

Otherwise, as per other pibooth plugins, you can clone this repository, and add `/path/to/pibooth_stillimage_camera.py` to `[GENERAL]` `plugins` list in pibooth.cfg.

## Configuration

You need to set `debug = True` in `[GENERAL]` for the plugin to kick in.

Optional colors customization (and occasional eye bleed):

```
[CAMERA]
  dummy_background = blue
  dummy_foreground = yellow
```

