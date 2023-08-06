import os
import argparse
from .titlebar import TitleBar, TitleBarButton, SvgTitleBarButton, StandardTitleBar
from qtpy.QtWidgets import QDialog,QMainWindow
import sys
if sys.platform == "win32":
    from .windows import AcrylicWindow
    from .windows import WindowsFramelessWindow as FramelessWindow
    from .windows import WindowsFramelessMainWindow as FramelessMainWindow
    from .windows import WindowsFramelessFramelessDialog as FramelessDialog
    from .windows import WindowsWindowEffect as WindowEffect
elif sys.platform == "linux":
    from .linux import LinuxFramelessWindow as FramelessWindow
    from .linux import LinuxFramelessWindow as AcrylicWindow
    from .linux import LinuxFramelessMainWindow as FramelessMainWindow
    from .linux import LinuxFramelessDialog as FramelessDialog
    from .linux import LinuxWindowEffect as WindowEffect
else:
    from .mac import AcrylicWindow
    from .mac import MacFramelessWindow as FramelessWindow
    from .mac import MacFramelessMainWindow as FramelessMainWindow
    from .mac import MacFramelessDialog as FramelessDialog
    from .mac import MacWindowEffect as WindowEffect




