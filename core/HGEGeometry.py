#!/usr/bin/python3.3
# coding=utf-8
"""
Geometry module.
"""
__author__ = 'Hossein Noroozpour Thany Abady'
from math3d.HGEModelMatrix import ModelMatrix


class Geometry():
    """
    Geometry class.
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.m = ModelMatrix()
        self.mvp = None
        self.shader = None
        self.texture = None
        self.mesh = None

    def set_mesh(self, mesh):
        """
        :param mesh:
        """
        self.mesh = mesh

    def set_shader(self, shader):
        """
        :param shader:
        """
        self.shader = shader

    def set_texture(self, texture):
        """
        :param texture:
        """
        self.texture = texture

    def set_vp(self, vp):
        """
        :param vp:
        """
        self.mvp = vp * self.m.matrix

    def draw(self):
        """
        Draw.
        """
        self.mesh.bind()
        self.shader.use()
        self.texture.bind()
        self.shader.set_mvp(self.mvp)
        self.mesh.draw()