#!/usr/bin/python3.3
# coding=utf-8
"""
Shader utilities module.
"""
__author__ = 'Hossein Noroozpour Thany Abady'
from OpenGL import GL
import ctypes


class ShaderUtility():
    """
    Shader utility class.
    """
    def __init__(self):
        """
        """
        pass

    @staticmethod
    def create_program():
        """
        :return: program
        :raise Exception: on error
        """
        program = GL.glCreateProgram()
        if program == ctypes.c_uint(0):
            raise Exception('Error in creating shader program.')
        return program

    @staticmethod
    def add_shader_to_program(shader_string, shader_type, program):
        """
        :param shader_string:
        :param shader_type:
        :param program:
        :raise Exception:
        """
        shader_object = GL.glCreateShader(shader_type)
        if ctypes.c_uint(0) == shader_object:
            raise Exception('Error in adding shader to program.')
        string = ctypes.c_char_p(shader_string)
        strings = ctypes.c_void_p(ctypes.addressof(string))
        length = GL.GLuint(len(shader_string))
        lengthes = ctypes.c_void_p(ctypes.addressof(length))
        GL.glShaderSource(shader_object, ctypes.c_uint(1), strings, lengthes)
        GL.glCompileShader(shader_object)
        info_log = GL.GLchar * 1030
        GL.glGetShaderInfoLog(shader_object, GL.GLuint(1024), GL.GLuint(0), )