<div align="center">

# QtPy-Fluent-Widgets

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Downloads](https://static.pepy.tech/badge/qtpy-fluent-widgets)](https://pepy.tech/project/qtpy-fluent-widgets)
![GitHub](https://img.shields.io/github/license/TaoChenyue/Qtpy-Frameless-Window?style=plastic)

A cross-platform frameless window based on QtPy.

</div>

This repo is based on *QtPy* and [PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets). Due to library in diffrent *PyQt-Fluent-Widgets* branches cannot exist in one virtual environment, I created this repository by adding *QtPy* dependence and modifying some modules. This repo will keep up with *PyQt-Fluent-Widgets*.

## Install
To install use pip:
```shell
pip install QtPy-Fluent-Widgets
```
Or clone the repo:
```shell
git clone https://github.com/TaoChenyue/QtPy-Fluent-Widgets.git
pip install -e .
```

## Usage
According to QtPy, environment argument ```QT_API``` must be set before importing qtpy. Here provides an easy way to set it.

```python
from qt_api import set_qt_api
# set through code
set_qt_api("pyqt5")
python examples/demo.py 
# set through sys.argv
set_qt_api(parse=True)
python examples/demo.py --api pyside6
```
If no QT_API is set, qtpy will use pyqt5 as default.

## Run Demo
```sh
cd examples/gallery
python demo.py
# or specify qt api
python demo.py --api pyqt5
python demo.py --api pyqt6
python demo.py --api pyside2
python demo.py --api pyside6
```