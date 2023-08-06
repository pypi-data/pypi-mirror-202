import os
import argparse
def set_qt_api(api:str=None,parse:bool=False):
    if parse:
        parser = argparse.ArgumentParser(description='Set Qt API')
        parser.add_argument('--api', type=str)
        args = parser.parse_args()
        if args.api is not None:
            api=args.api
        return args
    if api is None:
        api="pyqt5"
    os.environ["QT_API"]=api
    
set_qt_api(parse=True)

from .titlebar import TitleBar, TitleBarButton, SvgTitleBarButton, StandardTitleBar
from qtpy.QtWidgets import QDialog,QMainWindow
import sys
if sys.platform == "win32":
    from .windows import AcrylicWindow
    from .windows import WindowsFramelessWindow as FramelessWindow
    from .windows import WindowsFramelessMainWindow as FramelessMainWindow
    from .windows import WindowsFramelessFramelessDialog as FramelessDialog
    from .windows import WindowsWindowEffect as WindowEffect
else:
    if sys.platform == "darwin":
        from .mac import AcrylicWindow
        from .mac import MacFramelessWindow as FramelessWindow
        from .mac import MacWindowEffect as WindowEffect
    else:
        from .linux import LinuxFramelessWindow as FramelessWindow
        from .linux import LinuxWindowEffect as WindowEffect

    AcrylicWindow = FramelessWindow

    class FramelessDialog(QDialog, FramelessWindow):
        """ Frameless dialog """

        def __init__(self, parent=None):
            super().__init__(parent)
            self.titleBar.minBtn.hide()
            self.titleBar.maxBtn.hide()
            self.titleBar.setDoubleClickEnabled(False)


    class FramelessMainWindow(QMainWindow, FramelessWindow):
        """ Frameless main window """

        def __init__(self, parent=None):
            super().__init__(parent)



