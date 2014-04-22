# coding=utf-8
"""
Module for handling OpenGL buffers.
"""
__author__ = "Hossein Noroozpour"
from OpenGL import GL
import ctypes


class Mesh():
    """
    A class that hold mesh information about an actor
    """
    def __init__(self, elements, indices):
        temp_list = [0]
        # noinspection PyCallingNonCallable
        self.vbo = (ctypes.c_uint32 * 1)(*temp_list)
        # noinspection PyCallingNonCallable
        self.ibo = (ctypes.c_uint32 * 1)(*temp_list)
        GL.glGenBuffers(1, self.vbo)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        # noinspection PyCallingNonCallable
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            len(elements) * 4,
            (ctypes.c_float * len(elements))(*elements),
            GL.GL_STATIC_DRAW
        )
        GL.glGenBuffers(1, self.ibo)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        # noinspection PyCallingNonCallable
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER,
            len(indices) * 4,
            (ctypes.c_uint32 * len(indices))(*indices),
            GL.GL_STATIC_DRAW
        )
        self.indices_number = ctypes.c_uint32(len(indices))

    def __del__(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, ctypes.c_uint32(0))
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ctypes.c_uint32(0))
        GL.glDeleteBuffers(1, self.vbo)
        GL.glDeleteBuffers(1, self.ibo)

    def bind(self):
        """
        Bind itself.
        """
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

    def draw(self):
        """
        Draw.
        """
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices_number, GL.GL_UNSIGNED_INT, ctypes.c_uint32(0))