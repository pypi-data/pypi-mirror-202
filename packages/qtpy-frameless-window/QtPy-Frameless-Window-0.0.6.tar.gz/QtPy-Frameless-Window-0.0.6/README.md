<div align="center">

# QtPy-Frameless-Window

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Downloads](https://static.pepy.tech/badge/qtpy-frameless-window)](https://pepy.tech/project/qtpy-frameless-window)
![GitHub](https://img.shields.io/github/license/TaoChenyue/Qtpy-Frameless-Window?style=plastic)

A cross-platform frameless window based on QtPy.

</div>

This repo is based on *QtPy* and [PyQt-Frameless-Window](https://github.com/zhiyiYo/PyQt-Frameless-Window). Due to library in diffrent *PyQt-Frameless-Window* branches cannot exist in one virtual environment, I created this repository by adding *QtPy* dependence and modifying some modules. This repo will keep up with *PyQt-Frameless-Window*.

## Install
To install use pip:
```shell
pip install QtPy-Frameless-Window
```
Or clone the repo:
```shell
git clone https://github.com/TaoChenyue/QtPy-Frameless-Window.git
python setup.py install
```

## FQ
+ Q: Why acrylic window response slowly when dragging its edge on Windows platform?<br>
A: Reference to https://www.cnblogs.com/zhiyiYo/p/14659981.html, change settings.
