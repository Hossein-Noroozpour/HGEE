__author__ = "Hossein Noroozpour"

class Mesh():
    'A class that hold mesh information about an actor'
    def __init__(self):
        'Constructor for mesh class'

        #An interleaved array of vertices positions {XYZ}, normals vector {ABC} and UVs {ST}
        self.m_cFloatInterleavedArray = None
        #An array of indices for triangles
        self.m_cUIntIndexArray = None
        self.m_name = None
        self.m_id = None

        self.m_occlusionTestResult = False
        self.m_loadedToGPU = False
        self.m_deletedFromGPU = False
        self.m_loadedToCPU = False
        self.m_deletedFromCPU = False

    def loadToGPU(self):
        'Return False if mesh already loaded or anything went wrong otherwise True.'
        if(self.m_loadedToGPU):
            return False
        elif(not self.m_loadedToCPU):
            return False
        elif(self.m_deletedFromCPU):
            return False
        else:
            self.m_loadedToGPU = True
            #TODO
            return True


    def deleteFromGPU(self):
        'Return False if mesh already deleted or anything went wrong otherwise True.'
        if(self.m_deletedFromGPU):
            return False
        elif(not self.m_loadedToGPU):
            return False
        else:
            self.m_deletedFromGPU = True
            self.m_loadedToGPU = False
            #TODO
            return True


    def loadToCPU(self, interleavedArray, indexArray, name, id):
        'Return False if mesh already loaded or anything went wrong otherwise True.'
        if(self.m_loadedToCPU):
            return False
        elif(self.m_deletedFromCPU):
            return False
        else:
            self.m_loadedToCPU = True
            self.m_cFloatInterleavedArray = interleavedArray
            self.m_cUIntIndexArray = indexArray
            self.m_name = name
            self.m_id = id
            return True


    def deleteFromCPU(self):
        'Return False if mesh already deleted or anything went wrong otherwise True.'
        if(not self.m_loadedToCPU):
            return False
        elif(self.m_deletedFromCPU):
            return False
        else:
            self.m_deletedFromCPU = True
            self.m_cFloatInterleavedArray = None
            self.m_cUIntIndexArray = None
            return True


    def render(self):
        #TODO
        pass


    def occlusionTest(self):
        self.occlusionTestResult = False
        #TODO: Occlusion test must be implemented soon.