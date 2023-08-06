# coding:utf-8
import sys
from ctypes import cast
from ctypes.wintypes import LPRECT, MSG

import win32api
import win32con
import win32gui
from qtpy.QtCore import Qt
from qtpy.QtGui import QCloseEvent, QCursor
from qtpy.QtWidgets import QApplication, QWidget, QMainWindow, QDialog

from ..titlebar import TitleBar
from ..utils import win32_utils as win_utils
from ..utils.win32_utils import Taskbar
from .c_structures import LPNCCALCSIZE_PARAMS
from .window_effect import WindowsWindowEffect


class Ui_Frameless(object):
    BORDER_WIDTH = 5

    def __init__(self, *args, **kwds) -> None:
        pass

    def setupUi(self, Form: QWidget):
        self.windowEffect = WindowsWindowEffect(Form)
        self.titleBar = TitleBar(Form)
        self.resize(500, 500)
        self.titleBar.raise_()
        self._Form = Form
        self._isResizeEnabled = True

    def setTitleBar(self, titleBar: QWidget):
        """set custom title bar

        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.titleBar.deleteLater()
        self.titleBar = titleBar
        self.titleBar.setParent(self)
        self.titleBar.raise_()

    def resizeFrameless(self):
        self.titleBar.resize(self._Form.width(), self.titleBar.height())

    def nativeFrameless(self, message):
        """Handle the Windows message"""
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return False, 0

        if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
            pos = QCursor.pos()
            xPos = pos.x() - self._Form.x()
            yPos = pos.y() - self._Form.y()
            w, h = self._Form.width(), self._Form.height()
            lx = xPos < self.BORDER_WIDTH
            rx = xPos > w - self.BORDER_WIDTH
            ty = yPos < self.BORDER_WIDTH
            by = yPos > h - self.BORDER_WIDTH
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            else:
                rect = cast(msg.lParam, LPRECT).contents

            isMax = win_utils.isMaximized(msg.hWnd)
            isFull = win_utils.isFullScreen(msg.hWnd)

            # adjust the size of client rect
            if isMax and not isFull:
                ty = win_utils.getResizeBorderThickness(msg.hWnd, False)
                rect.top += ty
                rect.bottom -= ty

                tx = win_utils.getResizeBorderThickness(msg.hWnd, True)
                rect.left += tx
                rect.right -= tx

            # handle the situation that an auto-hide taskbar is enabled
            if (isMax or isFull) and Taskbar.isAutoHide():
                position = Taskbar.getPosition(msg.hWnd)
                if position == Taskbar.LEFT:
                    rect.top += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.BOTTOM:
                    rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.LEFT:
                    rect.left += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.RIGHT:
                    rect.right -= Taskbar.AUTO_HIDE_THICKNESS

            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result

        return False, 0

    def setResizeEnabled(self, isEnabled: bool):
        """set whether resizing is enabled"""
        self._isResizeEnabled = isEnabled

    def setScreenChanged(self):
        # solve issue #5
        self._Form.windowHandle().screenChanged.connect(self.__onScreenChanged)

    def __onScreenChanged(self):
        hWnd = int(self._Form.windowHandle().winId())
        win32gui.SetWindowPos(
            hWnd,
            None,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED,
        )

    def removeBorder(self):
        # remove window border
        if not win_utils.isWin7():
            self._Form.setWindowFlags(
                self._Form.windowFlags() | Qt.WindowType.FramelessWindowHint
            )
        else:
            self._Form.setWindowFlags(
                Qt.WindowType.FramelessWindowHint
                | Qt.WindowType.WindowMinMaxButtonsHint
            )

    def addShadowAndAnimatation(self):
        # add DWM shadow and window animation
        self.windowEffect.addWindowAnimation(self._Form.winId())
        if not isinstance(self, AcrylicWindow):
            self.windowEffect.addShadowEffect(self._Form.winId())


class WindowsFramelessWindow(QWidget, Ui_Frameless):
    """Frameless window for Windows system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.removeBorder()
        self.addShadowAndAnimatation()
        self.setScreenChanged()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.resizeFrameless()

    def nativeEvent(self, eventType, message):
        """Handle the Windows message"""
        return self.nativeFrameless(message)


class AcrylicWindow(WindowsFramelessWindow):
    """A frameless window with acrylic effect"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__closedByKey = False

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.windowEffect.enableBlurBehindWindow(self.winId())
        self.windowEffect.addWindowAnimation(self.winId())

        if win_utils.isWin7():
            self.windowEffect.addShadowEffect(self.winId())
            self.windowEffect.setAeroEffect(self.winId())
        else:
            self.windowEffect.setAcrylicEffect(self.winId())
            # if win_utils.isGreaterEqualWin11():
            #     self.windowEffect.addShadowEffect(self.winId())

        self.setStyleSheet("AcrylicWindow{background:transparent}")

    def nativeEvent(self, eventType, message):
        """Handle the Windows message"""
        msg = MSG.from_address(message.__int__())

        # handle Alt+F4
        if msg.message == win32con.WM_SYSKEYDOWN:
            if msg.wParam == win32con.VK_F4:
                self.__closedByKey = True
                QApplication.sendEvent(self, QCloseEvent())
                return False, 0

        return super().nativeEvent(eventType, message)

    def closeEvent(self, e):
        if not self.__closedByKey or QApplication.quitOnLastWindowClosed():
            self.__closedByKey = False
            return super().closeEvent(e)

        # system tray icon
        self.__closedByKey = False
        self.hide()


class WindowsFramelessMainWindow(QMainWindow, Ui_Frameless):
    """Frameless window for Windows system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.removeBorder()
        self.addShadowAndAnimatation()
        self.setScreenChanged()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.resizeFrameless()

    def nativeEvent(self, eventType, message):
        """Handle the Windows message"""
        return self.nativeFrameless(message)


class WindowsFramelessFramelessDialog(QDialog, Ui_Frameless):
    """Frameless dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.removeBorder()
        self.addShadowAndAnimatation()
        self.setScreenChanged()
        # for dialog
        self.titleBar.minBtn.hide()
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.resizeFrameless()

    def nativeEvent(self, eventType, message):
        """Handle the Windows message"""
        return self.nativeFrameless(message)
