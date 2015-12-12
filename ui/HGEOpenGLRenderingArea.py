# coding=utf-8
"""
Module for creating rendering area.
"""
__author__ = """Hossein Noroozpour"""

from OpenGL import GL
from OpenGL import GLX
from OpenGL.raw._GLX import struct__XDisplay
from ctypes import cdll
from ctypes import c_char_p
from ctypes import POINTER
from ctypes import c_int
from ctypes import byref
from Xlib.display import Display
import ctypes
from gi.repository import GdkX11


class OpenGLRenderingArea:
    """Gtk Rendering Area for OpenGL"""

    def __init__(self, wid):
        """Constructor for OpenGLRenderingArea"""
        xlib = cdll.LoadLibrary('libX11.so')
        xlib.XOpenDisplay.argtypes = [c_char_p]
        xlib.XOpenDisplay.restype = POINTER(struct__XDisplay)
        self.xdisplay = xlib.XOpenDisplay((ctypes.c_char * 1)(*[0]))
        display = Display()
        attrs = [
            GLX.GLX_RGBA, True,
            GLX.GLX_RED_SIZE, 1,
            GLX.GLX_GREEN_SIZE, 1,
            GLX.GLX_BLUE_SIZE, 1,
            GLX.GLX_DOUBLEBUFFER, 0,
            0, 0
        ]
        width = 200
        height = 200
        cattrs = (c_int * len(attrs))(*attrs)
        xvinfo = GLX.glXChooseVisual(self.xdisplay, display.get_default_screen(), cattrs)
        configs = GLX.glXChooseFBConfig(self.xdisplay, 0, None, byref(c_int()))
        self.context = GLX.glXCreateContext(self.xdisplay, xvinfo, None, True)
        self.x_window_id = GdkX11.X11Window.get_xid(wid)
        if not GLX.glXMakeCurrent(self.xdisplay, self.x_window_id, self.context):
            print("failed")
        GL.glViewport(0, 0, width, height)  # todo
        self.app = None
        GL.glClearColor(0.24, 0.24, 0.24, 0.0)
        self.profiler_window = None

    def render(self):
        """Must be called each frame"""
        if not GLX.glXMakeCurrent(self.xdisplay, self.x_window_id, self.context):
            print("failed")
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        #todo
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glIndexi(0)
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glVertex2i(0, 1)
        GL.glIndexi(0)
        GL.glColor3f(0.0, 1.0, 0.0)
        GL.glVertex2i(-1, -1)
        GL.glIndexi(0)
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glVertex2i(1, -1)
        GL.glEnd()
        self.app.render_loop()
        GLX.glXSwapBuffers(self.xdisplay, self.x_window_id)
        self.profiler_window.one_frame_passed()
        return True

    def set_application(self, app):
        """Set main application
        :param app: Application instance.
        """
        self.app = app

    def set_size(self, width, height):
        """Change size of rendering area
        :param height:
        :param width:
        """
        if not GLX.glXMakeCurrent(self.xdisplay, self.x_window_id, self.context):
            print("failed")
        GL.glViewport(0, 0, width, height)  # todo

    def set_profiler_window(self, profiler_window):
        """Set profiler window
        :param profiler_window:
        """
        self.profiler_window = profiler_window
