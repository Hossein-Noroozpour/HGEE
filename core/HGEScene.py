__author__ = 'Hossein Noroozpour'
class Scene():
    def __init__(self):
        'Scene manager class for HGE.'
        self.actors = []

    def addActor(self, actor):
        'Add actor to the scene.'
        self.actors.append(actor)

    def render(self):
        'Render the whole scene.'
        #todo
        pass