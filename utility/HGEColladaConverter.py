__author__ = """Hossein Noroozpour"""

from xml.etree import ElementTree
from ctypes import c_float
from ctypes import c_uint

from core.HGEActor import Actor
from core.HGEMesh import Mesh


def ColladaToHGEActors(colladaFileAddress):
    """It's not general purpose Collada importer and it's not gonna be!
It returns list of actors."""
    colladaTree = ElementTree.parse(colladaFileAddress)
    root = colladaTree.getroot()
    namespaceLength = len(root.tag) - len('COLLADA')
    namespace = root.tag[0:namespaceLength]
    if root.tag != namespace + "COLLADA":
        print """Error! It not a proper collada format!"""
        raise Exception("""Collada format error.""")

    libraryGeometriesTag = namespace + "library_geometries"
    geometryTag = namespace + "geometry"
    meshTag = namespace + "mesh"
    sourceTag = namespace + "source"
    floatArrayTag = namespace + "float_array"
    polyListTag = namespace + "polylist"
    vcountTag = namespace + "vcount"
    pTag = namespace + "p"

    idLabel = "id"
    nameLabel = "name"
    positionsLabel = "positions"
    normalsLabel = "normals"
    map0Label = "map-0"
    mapLabel = "map"

    def SourcePositionsParser(root):
        """It will return positions in this format:
        [(X1,Y1,Z1),(X2, Y2, Z2),...,(Xn, Yn, Zn)]
        which X, Y and  Z are float numbers."""
        #TODO: This version is very strict to blender format, I must make it more flexible.
        positions = []
        for child in root:
            if child.tag == floatArrayTag:
                strnums = child.text.split(' ')
                for i in range(0, len(strnums), 3):
                    positions.append((float(strnums[i]), float(strnums[i+1]), float(strnums[i+2])))
        return positions

    def SourceNormalsParser(root):
        """It will return normals in this format:
        [(X1,Y1,Z1),(X2, Y2, Z2),...,(Xn, Yn, Zn)]
        which X, Y and  Z are float numbers."""
        #TODO: This version is very strict to blender format, I must make it more flexible.
        normals = []
        for child in root:
            if child.tag == floatArrayTag:
                strnums = child.text.split(' ')
                for i in range(0, len(strnums), 3):
                    normals.append((float(strnums[i]), float(strnums[i+1]), float(strnums[i+2])))
        return normals

    def SourceUVsParser(root):
        """It will return UVs in this format:
        [(S1,T1),(S2, T2),...,(Sn, Tn)]
        which S and T are float numbers."""
        #TODO: This version is very strict to blender format, I must make it more flexible.
        uvs = []
        for child in root:
            if child.tag == floatArrayTag:
                strnums = child.text.split(' ')
                for i in range(0, len(strnums), 2):
                    uvs.append((float(strnums[i]), float(strnums[i+1])))
        return uvs

    def PolyListParser(root):
        """Parser of poly list branch.
It will return pages in this format:
    [(
        (VertexINDEX1, NormalINDEX1, UVINDEX1),
        (VertexINDEX2, NormalINDEX2, UVINDEX2),
        (VertexINDEX3, NormalINDEX3, UVINDEX3)
     ),
     ...]
which VertexINDEX is vertex index, NormalINDEX is normal index and UVINDEX is uv index."""
        #TODO: This version is very strict to blender format, I must make it more flexible.
        child = root.find(vcountTag)
        for strnum in child.text.split():
            if strnum != '3':
                print """Error! Your mesh must be in triangular form."""
                raise Exception("""Not triangulated mesh form error.""")
        child = root.find(pTag)
        strnums = child.text.split(' ')
        result = []
        for i in range(0, len(strnums), 9):
            result.append(((int(strnums[i]), int(strnums[i+1]), int(strnums[i+2])),
                           (int(strnums[i+3]), int(strnums[i+4]), int(strnums[i+5])),
                           (int(strnums[i+6]), int(strnums[i+7]), int(strnums[i+8]))))
        return result


    def MeshParser(root, geometryID, geometryName):
        """Parser for mesh element branch.
It will return in this format:
[c_uint_Array_N1, c_float_Array_N2]:
which parameter 1 is C pointer to uint array with N1 element in it and
parameter 2 is C pointer to float array with N2 element in it."""
        patternOffset = len(geometryID) + 1
        sourcePositionsResult = None
        sourceNormalsResult = None
        sourceUVsResult = None
        polyListResult = None
        for child in root:
            if child.tag == sourceTag and child.attrib[idLabel][patternOffset:] == positionsLabel:
                sourcePositionsResult = SourcePositionsParser(child)
            elif child.tag == sourceTag and child.attrib[idLabel][patternOffset:] == normalsLabel:
                sourceNormalsResult = SourceNormalsParser(child)
            elif child.tag == sourceTag and child.attrib[idLabel][patternOffset:] == map0Label:
                sourceUVsResult = SourceUVsParser(child)
            #TODO: I must support multichannel UV, but for now it's OK! And in addition,
            #TODO: I must say multichannel UV will cause performance penalty, And maybe its not necessary at all.
            elif child.tag == sourceTag and mapLabel in child.attrib[idLabel][patternOffset:]:
                print """Error! This version of HGE does not support multichannel UV."""
                raise Exception("Collada format error.")
        child = root.find(polyListTag)
        polyListResult = PolyListParser(child)

        print "Number of total vertices is " + str(len(sourcePositionsResult))
        print "Number of total normals is " + str(len(sourceNormalsResult))
        print "Number of total UVs is " + str(len(sourceUVsResult))
        print "Number of total polies is " + str(len(polyListResult))

        nodes = set()
        nodesList = []
        optiNodes = []
        indices = []

        nodesLength = len(nodes)

        for poly in polyListResult:
            for node in poly:
                tmpnd = (sourcePositionsResult[node[0]], sourceNormalsResult[node[1]], sourceUVsResult[node[2]])
                nodes.add(tmpnd)
                nodesList.append(tmpnd)
                if nodesLength != len(nodes):
                    indices.append(nodesLength)
                    nodesLength = len(nodes)
                    optiNodes.append(tmpnd)
                else:
                    indices.append(optiNodes.index(tmpnd))

        print "Number of total nodes is " + str(len(nodesList))
        print "Number of optimized nodes set is " + str(len(nodes))
        print "Number of optimized nodes list is " + str(len(optiNodes))
        print "Number of indices nodes is " + str(len(indices))

        floatList = []

        for node in optiNodes:
            for attr in node:
                for number in attr:
                    floatList.append(number)

        print "Number of float numbers is " + str(len(floatList))

        indexArray = (c_uint * len(indices))(*indices)
        floatArray = (c_float *len(floatList))(*floatList)

        result = [indexArray, floatArray]

        return result

    def GeometryParser(root):
        """Parser for geometry element branch.
It will return a dictionary with following keys:
"id",
"name",
"buffer",
"indices"
for more investigation see MeshParser result."""
        geometryID = root.attrib[idLabel]
        geometryName = root.attrib[nameLabel]
        meshResult = None
        for child in root:
            if child.tag == meshTag:
                meshResult = MeshParser(child, geometryID, geometryName)

        result = {"id" : geometryID, "name" : geometryName, "buffer": meshResult[1], "indices" : meshResult[0]}

        return result

    def LibraryGeometriesParser(root):
        """Parser of library_geometries element branch.
It will return a list in following form:
[geometryResult1, geometryResult2, ... , geometryResultN]
for more investigation see result of GeometryParser."""

        geometriesResultsList = []
        for child in root:
            if child.tag == geometryTag:
                geometriesResultsList.append(GeometryParser(child))
        return geometriesResultsList

    library_geometriesResult = None
    for child in root:
        if child.tag == libraryGeometriesTag:
            library_geometriesResult = LibraryGeometriesParser(child)
        #TODO: Other Collada properties must be implemented

    actors = []
    for geometry in library_geometriesResult:
        actor = Actor()
        mesh = Mesh()
        mesh.loadToCPU(geometry['buffer'], geometry['indices'], geometry['name'], geometry['id'])
        actor.addMesh(mesh)
        actors.append(actor)
        print actor

    return actors

if __name__ == "__main__":
    ColladaToHGEActors("/home/thany/PycharmProjects/Resources/cube.dae")