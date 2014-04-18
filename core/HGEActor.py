__author__ = "Hossein Noroozpour"

class Actor():
    'Everything in a game is an actor.'
    def __init__(self):
        'Actor class constructor.'
        self.m_meshes = []
        #todo

    def addMesh(self, mesh):
        'Add mesh to actor.'
        self.m_meshes.append(mesh)
