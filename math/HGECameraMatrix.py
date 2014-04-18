#!/usr/bin/python3.3
# coding=utf-8
"""
Module for basic camera matrix.
"""
__author__ = 'Hossein Noroozpour Thany Abady'
from math.HGEMath import Math
import numpy
import ctypes


class CameraMatrix():
    """
    Class for camera handling.
    """

    def __init__(self):
        self.matrix = Math.identity_matrix()
        self.location = numpy.array([0., 0., 0., 1.])
        self.local_x_direction = numpy.array([1., 0., 0., 1.])
        self.local_y_direction = numpy.array([0., 1., 0., 1.])
        self.local_z_direction = numpy.array([0., 0., 1., 1.])
        self.rotation_scale_matrix = Math.identity_matrix()

    def get_value(self):
        """
        :return:
        """
        return ctypes.c_void_p(self.matrix.ctype.data)

    def get_matrix(self):
        """
        :return:
        """
        return self.matrix

    def rotate(self, axis, angle):
        """
        :param axis: It must be numpy array.
        :param angle: It must be radian degree.
        """
        r = Math.rotation_matrix(-angle, axis)
        self.local_x_direction *= r
        self.local_y_direction *= r
        self.local_z_direction *= r
        self.rotation_scale_matrix *= r

    def rotate_local_x(self, angle):
        """
        :param angle: It must be radian degree.
        """
        self.rotate(self.local_x_direction, angle)

    def rotate_local_y(self, angle):
        """
        :param angle: It must be radian degree.
        """
        self.rotate(self.local_y_direction, angle)

    def rotate_local_z(self, angle):
        """
        :param angle: It must be radian degree.
        """
        self.rotate(self.local_z_direction, angle)

    def rotate_global_x(self, angle):
        """
        :param angle: It must be radian degree.
        """
        self.rotate(numpy.array([1., 0., 0., 1.]), angle)

    def rotate_global_y(self, angle):
        """
        :param angle: It must be radian degree.
        """
        self.rotate(numpy.array([0., 1., 0., 1.]), angle)

    def rotate_global_z(self, angle):
        """
        :param angle: It must be radian degree.
        """
        self.rotate(numpy.array([0., 0., 1., 1.]), angle)

    def __mul__(self, other):
        return self.matrix * other.matrix