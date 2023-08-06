import qtpy
if qtpy.PYQT5:
    # coding:utf-8
from PyQt5.QtCore import QCoreApplication, QEvent, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget

from ..titlebar import TitleBar
from ..utils.linux_utils import LinuxMoveResize
from .window_effect import LinuxWindowEffect


class LinuxFramelessWindow(QWidget):
    """ Frameless window for Linux system """

    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.windowEffect = LinuxWindowEffect(self)
        self.titleBar = TitleBar(self)
        self._isResizeEnabled = True

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        QCoreApplication.instance().installEventFilter(self)

        self.titleBar.raise_()
        self.resize(500, 500)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.titleBar.resize(self.width(), self.titleBar.height())

    def setTitleBar(self, titleBar):
        """ set custom title bar

        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.titleBar.deleteLater()
        self.titleBar = titleBar
        self.titleBar.setParent(self)
        self.titleBar.raise_()

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled

    def eventFilter(self, obj, event):
        et = event.type()
        if et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._isResizeEnabled:
            return False

        edges = Qt.Edges()
        pos = QMouseEvent(event).globalPos() - self.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.LeftEdge
        if pos.x() >= self.width()-self.BORDER_WIDTH:
            edges |= Qt.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.TopEdge
        if pos.y() >= self.height()-self.BORDER_WIDTH:
            edges |= Qt.BottomEdge

        # change cursor
        if et == QEvent.MouseMove and self.windowState() == Qt.WindowNoState:
            if edges in (Qt.LeftEdge | Qt.TopEdge, Qt.RightEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeFDiagCursor)
            elif edges in (Qt.RightEdge | Qt.TopEdge, Qt.LeftEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeBDiagCursor)
            elif edges in (Qt.TopEdge, Qt.BottomEdge):
                self.setCursor(Qt.SizeVerCursor)
            elif edges in (Qt.LeftEdge, Qt.RightEdge):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        elif obj in (self, self.titleBar) and et == QEvent.MouseButtonPress and edges:
            LinuxMoveResize.starSystemResize(self, event.globalPos(), edges)

        return super().eventFilter(obj, event)
if qtpy.PYQT6:
    # coding:utf-8
from PyQt6.QtCore import QCoreApplication, QEvent, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget

from ..titlebar import TitleBar
from ..utils.linux_utils import LinuxMoveResize
from .window_effect import LinuxWindowEffect


class LinuxFramelessWindow(QWidget):
    """ Frameless window for Linux system """

    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.windowEffect = LinuxWindowEffect(self)
        self.titleBar = TitleBar(self)
        self._isResizeEnabled = True

        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowType.FramelessWindowHint)
        QCoreApplication.instance().installEventFilter(self)

        self.titleBar.raise_()
        self.resize(500, 500)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.titleBar.resize(self.width(), self.titleBar.height())

    def setTitleBar(self, titleBar):
        """ set custom title bar
        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.titleBar.deleteLater()
        self.titleBar = titleBar
        self.titleBar.setParent(self)
        self.titleBar.raise_()

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled

    def eventFilter(self, obj, event):
        et = event.type()
        if et != QEvent.Type.MouseButtonPress and et != QEvent.Type.MouseMove or not self._isResizeEnabled:
            return False

        edges = Qt.Edge(0)
        pos = event.globalPosition().toPoint() - self.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.Edge.LeftEdge
        if pos.x() >= self.width()-self.BORDER_WIDTH:
            edges |= Qt.Edge.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.Edge.TopEdge
        if pos.y() >= self.height()-self.BORDER_WIDTH:
            edges |= Qt.Edge.BottomEdge

        # change cursor
        if et == QEvent.Type.MouseMove and self.windowState() == Qt.WindowState.WindowNoState:
            if edges in (Qt.Edge.LeftEdge | Qt.Edge.TopEdge, Qt.Edge.RightEdge | Qt.Edge.BottomEdge):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif edges in (Qt.Edge.RightEdge | Qt.Edge.TopEdge, Qt.Edge.LeftEdge | Qt.Edge.BottomEdge):
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            elif edges in (Qt.Edge.TopEdge, Qt.Edge.BottomEdge):
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            elif edges in (Qt.Edge.LeftEdge, Qt.Edge.RightEdge):
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

        elif obj in (self, self.titleBar) and et == QEvent.Type.MouseButtonPress and edges:
            LinuxMoveResize.starSystemResize(self, event.globalPosition(), edges)

        return super().eventFilter(obj, event)
if qtpy.PYSIDE2:
    # coding:utf-8
from PySide2.QtCore import QCoreApplication, QEvent, Qt
from PySide2.QtWidgets import QWidget

from ..titlebar import TitleBar
from ..utils.linux_utils import LinuxMoveResize
from .window_effect import LinuxWindowEffect


class LinuxFramelessWindow(QWidget):
    """ Frameless window for Linux system """

    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def _initFrameless(self):
        self.windowEffect = LinuxWindowEffect(self)
        self.titleBar = TitleBar(self)
        self._isResizeEnabled = True

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        QCoreApplication.instance().installEventFilter(self)

        self.titleBar.raise_()
        self.resize(500, 500)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.titleBar.resize(self.width(), self.titleBar.height())

    def setTitleBar(self, titleBar):
        """ set custom title bar
        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.titleBar.deleteLater()
        self.titleBar = titleBar
        self.titleBar.setParent(self)
        self.titleBar.raise_()

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled

    def eventFilter(self, obj, event):
        et = event.type()
        if et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._isResizeEnabled:
            return False

        edges = Qt.Edge(0)
        pos = event.globalPos() - self.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.LeftEdge
        if pos.x() >= self.width()-self.BORDER_WIDTH:
            edges |= Qt.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.TopEdge
        if pos.y() >= self.height()-self.BORDER_WIDTH:
            edges |= Qt.BottomEdge

        # change cursor
        if et == QEvent.MouseMove and self.windowState() == Qt.WindowNoState:
            if edges in (Qt.LeftEdge | Qt.TopEdge, Qt.RightEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeFDiagCursor)
            elif edges in (Qt.RightEdge | Qt.TopEdge, Qt.LeftEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeBDiagCursor)
            elif edges in (Qt.TopEdge, Qt.BottomEdge):
                self.setCursor(Qt.SizeVerCursor)
            elif edges in (Qt.LeftEdge, Qt.RightEdge):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        elif obj in (self, self.titleBar) and et == QEvent.MouseButtonPress and edges:
            LinuxMoveResize.starSystemResize(self, event.globalPos(), edges)

        return super().eventFilter(obj, event)
if qtpy.PYSIDE6:
    # coding:utf-8
from PySide6.QtCore import QCoreApplication, QEvent, Qt
from PySide6.QtWidgets import QWidget, QMainWindow, QDialog

from ..titlebar import TitleBar
from ..utils.linux_utils import LinuxMoveResize
from .window_effect import LinuxWindowEffect


class LinuxFramelessWindowBase:
    """ Frameless window base class for Linux system """

    BORDER_WIDTH = 5

    def __init__(self, *args, **kwargs):
        pass

    def _initFrameless(self):
        self.windowEffect = LinuxWindowEffect(self)
        self.titleBar = TitleBar(self)
        self._isResizeEnabled = True

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        QCoreApplication.instance().installEventFilter(self)

        self.titleBar.raise_()
        self.resize(500, 500)

    def resizeEvent(self, e):
        self.titleBar.resize(self.width(), self.titleBar.height())

    def setTitleBar(self, titleBar):
        """ set custom title bar
        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.titleBar.deleteLater()
        self.titleBar = titleBar
        self.titleBar.setParent(self)
        self.titleBar.raise_()

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled

    def eventFilter(self, obj, event):
        et = event.type()
        if et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._isResizeEnabled:
            return False

        edges = Qt.Edge(0)
        pos = event.globalPos() - self.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.LeftEdge
        if pos.x() >= self.width()-self.BORDER_WIDTH:
            edges |= Qt.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.TopEdge
        if pos.y() >= self.height()-self.BORDER_WIDTH:
            edges |= Qt.BottomEdge

        # change cursor
        if et == QEvent.MouseMove and self.windowState() == Qt.WindowNoState:
            if edges in (Qt.LeftEdge | Qt.TopEdge, Qt.RightEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeFDiagCursor)
            elif edges in (Qt.RightEdge | Qt.TopEdge, Qt.LeftEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeBDiagCursor)
            elif edges in (Qt.TopEdge, Qt.BottomEdge):
                self.setCursor(Qt.SizeVerCursor)
            elif edges in (Qt.LeftEdge, Qt.RightEdge):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        elif obj in (self, self.titleBar) and et == QEvent.MouseButtonPress and edges:
            LinuxMoveResize.starSystemResize(self, event.globalPos(), edges)

        return False


class LinuxFramelessWindow(QWidget, LinuxFramelessWindowBase):
    """ Frameless window for Linux system """


    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()

    def resizeEvent(self, e):
        LinuxFramelessWindowBase.resizeEvent(self, e)

    def eventFilter(self, obj, event):
        return LinuxFramelessWindowBase.eventFilter(self, obj, event)


class LinuxFramelessMainWindow(QMainWindow, LinuxFramelessWindowBase):
    """ Frameless main window for Linux system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()

    def resizeEvent(self, e):
        QMainWindow.resizeEvent(self, e)
        self.titleBar.resize(self.width(), self.titleBar.height())

    def eventFilter(self, obj, event):
        return LinuxFramelessWindowBase.eventFilter(self, obj, event)


class LinuxFramelessDialog(QDialog, LinuxFramelessWindowBase):
    """ Frameless dialog for Windows system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()
        self.titleBar.minBtn.hide()
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)

    def resizeEvent(self, e):
        self.titleBar.resize(self.width(), self.titleBar.height())

    def eventFilter(self, obj, event):
        return LinuxFramelessWindowBase.eventFilter(self, obj, event)