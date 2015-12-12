#!/usr/bin/python3.3
# coding=utf-8
"""
Module for fundamental math3d operations.
"""
__author__ = 'Hossein Noroozpour Thany Abady'
import numpy
import math


class Math:
    """
    Math class for game engine.
    """

    def __init__(self):
        pass

    @staticmethod
    def normalize(vector):
        """
        :param vector:
        """
        data = numpy.array(vector, dtype=numpy.float32, copy=True)
        data /= math.sqrt(numpy.dot(data, data))
        return data

    @staticmethod
    def identity_matrix():
        """
        :return: Identity matrix NxN
        """
        return numpy.identity(4, numpy.float32)

    @staticmethod
    def translation_matrix(direction):
        """
        :param direction:
        :return: Matrix NxN
        """
        mat = numpy.identity(4, numpy.float32)
        mat[:3, 3] = direction[:3]
        return mat

    @staticmethod
    def rotation_matrix(angle, direction):
        """
        :param angle:
        :param direction:
        :return:
        """
        s = math.sin(angle)
        c = math.cos(angle)
        direction = Math.normalize(direction[:3])
        r = numpy.diag([c, c, c])
        r += numpy.outer(direction, direction) * (1.0 - c)
        direction *= s
        r += numpy.array([[0.0, -direction[2], direction[1]], [direction[2], 0.0, -direction[0]], [-direction[1], direction[0], 0.0]])
        m = numpy.identity(4)
        m[:3, :3] = r
        return m

    @staticmethod
    def scale_matrix(factor):
        """
        :param factor:
        :return:
        """
        return numpy.diag([factor, factor, factor, 1.0])

    @staticmethod
    def perspective_projection_matrix(near, far, width, height):
        """
        :param near:
        :param far:
        :param width:
        :param height:
        :return:
        """
        return numpy.matrix(
            [
                [near / width, 0.0, 0.0, 0.0],
                [0.0, near / height, 0.0, 0.0],
                [0.0, 0.0, (far + near) / (near - far), (2.0 * far * near) / (near - far)],
                [0.0, 0.0, -1.0, 0.0]
            ]
        )

    @staticmethod
    def vec4f(x=0., y=0., z=0., w=1.):
        """
        Create new vector.
        :param x: X component
        :param y: Y component
        :param z: Z component
        :param w: W component
        :return: vector4f
        """
        return numpy.array([x, y, z, w], numpy.float32)
