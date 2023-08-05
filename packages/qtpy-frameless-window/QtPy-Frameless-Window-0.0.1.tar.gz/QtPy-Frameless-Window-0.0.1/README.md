<div align=center>

# QtPy-Frameless-Window

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

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

## Usage
you can specify qt api(pyqt5,pyqt6,pyside2,pyside6) like this in the beginning:

```python
from qtframelesswindow import set_qt_api
set_qt_api("pyqt5")
```
or specify qt api through args
```sh
python your-pyscript.py
# or 
python your-pyscript.py --api pyside6
```
default qt api is pyqt5.
```python
from qtframelesswindow import FramelessWindow
from qtpy.QtWidgets import QApplication


class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("QtPy-Frameless-Window")


if __name__ == "__main__":
    app = QApplication([])
    demo = Window()
    demo.show()
    app.exec_()

```