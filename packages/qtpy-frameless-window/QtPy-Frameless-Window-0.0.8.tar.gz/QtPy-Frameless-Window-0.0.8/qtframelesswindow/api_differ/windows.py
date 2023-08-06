from ctypes import byref, c_int,windll

# fit api differ
try:
    from qtpy.QtWinExtras import QtWin
except:
    from ctypes import c_int
    class QtWin:
        def isCompositionEnabled():
            """ detect if dwm composition is enabled """
            bResult = c_int(0)
            windll.dwmapi.DwmIsCompositionEnabled(byref(bResult))
            return bool(bResult.value)
        def enableBlurBehindWindow(*args):
            pass