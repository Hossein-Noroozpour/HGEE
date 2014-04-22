# coding=utf-8
"""
Scene module.
"""
__author__ = 'Hossein Noroozpour thany abady'
from math3d.HGEMath import Math
from math3d.HGECameraMatrix import CameraMatrix


class Scene():
    """
    Scene class.
    """
    def __init__(self):
        self.geometries = []
        self.cameras = [CameraMatrix()]
        self.current_camera = 0
        self.perspectives = [Math.perspective_projection_matrix(0.2, 10000.0, 1, 0.7)]
        self.current_perspective = 0
        self.occlusion_culling_shader = None  # TODO
        self.default_shader = None
        self.default_texture = None
        self.terrain = None  # TODO
        self.sky = None  # TODO

    def add_geometry(self, geometry):
        """
        :param geometry:
        """
        self.geometries.append(geometry)

    def render(self):
        """
        Render.
        """
        vp = self.perspectives[self.current_perspective] * self.cameras[self.current_camera].matrix
        for geometry in self.geometries:
            geometry.set_vp(vp)
            geometry.draw()