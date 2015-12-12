#!/usr/bin/python3.3
# coding=utf-8
"""
Module for basic model matrix manipulation.
"""
__author__ = 'Hossein Noroozpour Thany Abady'
from math3d.HGEMath import Math
import ctypes


class ModelMatrix:
    """
    Class for model matrix handling.
    """

    def __init__(self):
        self.matrix = Math.identity_matrix()
        self.location = Math.vec4f()
        self.local_x_direction = Math.vec4f(x=1.)
        self.local_y_direction = Math.vec4f(y=1.)
        self.local_z_direction = Math.vec4f(z=1.)
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
        r = Math.rotation_matrix(angle, axis)
        self.local_x_direction = r * self.local_x_direction
        self.local_y_direction = r * self.local_y_direction
        self.local_z_direction = r * self.local_z_direction
        self.rotation_scale_matrix = r * self.rotation_scale_matrix
        self.matrix[0:3, 0:3] = self.rotation_scale_matrix[0:3, 0:3]

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
        self.rotate(Math.vec4f(x=1.), angle)

    def rotate_global_y(self, angle):
        """
        :param angle: It must be radian degree.
        """
        self.rotate(Math.vec4f(y=1.), angle)

    def rotate_global_z(self, angle):
        """
        :param angle: It must be radian degree.
        """
        self.rotate(Math.vec4f(z=1.), angle)

    def move_forward(self, distance):
        """
        Move camera in forward direction.
        :param distance: Distance that camera must move.
        """
        self.location += self.local_z_direction * distance
        self.matrix[:3, 3] = self.location[:3]

    def move_sideward(self, distance):
        """
        Move camera in sideward direction.
        :param distance: Distance that camera must move.
        """
        self.location += self.local_x_direction * distance
        self.matrix[:3, 3] = self.location[:3]

    def move_upward(self, distance):
        """
        Move camera in upward direction.
        :param distance: Distance that camera must move.
        """
        self.location += self.local_y_direction * distance
        self.matrix[:3, 3] = self.location[:3]

    def __mul__(self, other):
        return self.matrix * other.matrix
