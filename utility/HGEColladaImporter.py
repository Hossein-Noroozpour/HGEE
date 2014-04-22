# coding=utf-8
"""
Module for importing Collada file to the game engine.
"""
__author__ = """Hossein Noroozpour"""

from xml.etree import ElementTree
from ctypes import c_float
from ctypes import c_uint

from core.HGEActor import Actor
from core.HGEMesh import Mesh


def collada_importer(file_name):
    """
    It's not general purpose Collada importer yet and it's gonna be!
    It returns a scene.
    :param file_name:
    """
    collada_tree = ElementTree.parse(file_name)
    root = collada_tree.getroot()
    namespace_length = len(root.tag) - len('COLLADA')
    namespace = root.tag[0:namespace_length]
    if root.tag != namespace + "COLLADA":
        print('Error! It not a proper collada format!')
        raise Exception('Collada format error.')
    # TAGS #############################################################################################################
    library_geometries_tag = namespace + "library_geometries"
    geometry_tag = namespace + "geometry"
    mesh_tag = namespace + "mesh"
    source_tag = namespace + "source"
    float_array_tag = namespace + "float_array"
    poly_list_tag = namespace + "polylist"
    v_count_tag = namespace + "vcount"
    p_tag = namespace + "p"
    # LABELS ###########################################################################################################
    id_label = "id"
    name_label = "name"
    positions_label = "positions"
    normals_label = "normals"
    map_0_label = "map-0"
    map_label = "map"

    def source_positions_parser(root_node):
        """
        It will return positions in this format:
            [(X1,Y1,Z1),(X2, Y2, Z2),...,(Xn, Yn, Zn)]
        which X, Y and  Z are float numbers.
        :param root_node:
        """
        #TODO: This version is very strict to blender format, I must make it more flexible.
        positions = []
        for c in root_node:
            if c.tag == float_array_tag:
                string_numbers = c.text.split(' ')
                for i in range(0, len(string_numbers), 3):
                    positions.append(
                        (float(string_numbers[i]),
                         float(string_numbers[i + 1]),
                         float(string_numbers[i + 2])))
        return positions

    def source_normals_parser(root_node):
        """
        It will return normals in this format:
            [(X1,Y1,Z1),(X2, Y2, Z2),...,(Xn, Yn, Zn)]
        which X, Y and  Z are float numbers.
        :param root_node:
        """
        #TODO: This version is very strict to blender format, I must make it more flexible.
        normals = []
        for c in root_node:
            if c.tag == float_array_tag:
                string_numbers = c.text.split(' ')
                for i in range(0, len(string_numbers), 3):
                    normals.append((
                        float(string_numbers[i]),
                        float(string_numbers[i + 1]),
                        float(string_numbers[i + 2])))
        return normals

    def source_uvs_parser(root_node):
        """
        It will return UVs in this format:
            [(S1,T1),(S2, T2),...,(Sn, Tn)]
        which S and T are float numbers.
        :param root_node:
        """
        #TODO: This version is very strict to blender format, I must make it more flexible.
        uvs = []
        for c in root_node:
            if c.tag == float_array_tag:
                string_numbers = c.text.split(' ')
                for i in range(0, len(string_numbers), 2):
                    uvs.append((
                        float(string_numbers[i]),
                        float(string_numbers[i + 1])))
        return uvs

    def poly_list_parser(root_node):
        """
        Parser of poly list branch.
        It will return polygons in this format:
            [(
                (VertexINDEX1, NormalINDEX1, UVINDEX1),
                (VertexINDEX2, NormalINDEX2, UVINDEX2),
                (VertexINDEX3, NormalINDEX3, UVINDEX3)),...]
        which VertexINDEX is vertex index, NormalINDEX is normal index and UVINDEX is uv index.
        :param root_node:
        """
        #TODO: This version is very strict to blender format, I must make it more flexible.
        c = root_node.find(v_count_tag)
        for string_numbers in c.text.split():
            if string_numbers != '3':
                print('Error! Your mesh must be in triangular form.')
                raise Exception('Not triangulated mesh form error.')
        c = root_node.find(p_tag)
        string_numbers = c.text.split(' ')
        result = []
        for i in range(0, len(string_numbers), 9):
            result.append(((int(string_numbers[i]), int(string_numbers[i + 1]), int(string_numbers[i + 2])),
                           (int(string_numbers[i + 3]), int(string_numbers[i + 4]), int(string_numbers[i + 5])),
                           (int(string_numbers[i + 6]), int(string_numbers[i + 7]), int(string_numbers[i + 8]))))
        return result

    # noinspection PyCallingNonCallable
    def mesh_parser(root_node, geometry_id):
        """
        Parser for mesh element branch.
        :param geometry_id:
        :param root_node:
        It will return in this format:
            [c_uint_Array_N1, c_float_Array_N2]:
        which parameter 1 is C pointer to uint array with N1 element in it and
        parameter 2 is C pointer to float array with N2 element in it.
        """
        pattern_offset = len(geometry_id) + 1
        source_positions_result = None
        source_normals_result = None
        source_uvs_result = None
        for c in root_node:
            if c.tag == source_tag and c.attrib[id_label][pattern_offset:] == positions_label:
                source_positions_result = source_positions_parser(c)
            elif c.tag == source_tag and c.attrib[id_label][pattern_offset:] == normals_label:
                source_normals_result = source_normals_parser(c)
            elif c.tag == source_tag and c.attrib[id_label][pattern_offset:] == map_0_label:
                source_uvs_result = source_uvs_parser(c)
            #TODO: I must support multichannel UV, but for now it's OK! And in addition,
            #TODO: I must say multichannel UV will cause performance penalty, And maybe its not necessary at all.
            elif c.tag == source_tag and map_label in c.attrib[id_label][pattern_offset:]:
                print('Error! This version of HGE does not support multichannel UV.')
                raise Exception('Collada format error.')
        c = root_node.find(poly_list_tag)
        poly_list_result = poly_list_parser(c)
        print('Number of total vertices is ' + str(len(source_positions_result)))
        print('Number of total normals is ' + str(len(source_normals_result)))
        print('Number of total UVs is ' + str(len(source_uvs_result)))
        print('Number of total polygons is ' + str(len(poly_list_result)))
        nodes = dict()
        index = 0
        for poly in poly_list_result:
            for node in poly:
                temp_node = (
                    source_positions_result[node[0]],
                    source_normals_result[node[1]],
                    source_uvs_result[node[2]])
                if nodes.get(temp_node) is None:
                    nodes[temp_node] = [index]
                else:
                    nodes[temp_node].append(index)
                index += 1
        print('Number of optimized nodes is ' + str(len(nodes)))
        print('Number of total nodes is ' + str(index))
        float_list = [e for n in nodes.keys() for e in n]
        indices = [i for i in nodes.values()]
        print('Number of float numbers is ' + str(len(float_list)))
        result = [indices, float_list]
        return result

    def geometry_parser(root_node):
        """
        Parser for geometry element branch.
        It will return a dictionary with following keys:
        "id",
        "name",
        "buffer",
        "indices"
        for more investigation see mesh_parser result.
        :param root_node:
        """
        geometry_id = root_node.attrib[id_label]
        geometry_name = root_node.attrib[name_label]
        mesh_result = None
        for c in root_node:
            if c.tag == mesh_tag:
                mesh_result = mesh_parser(c, geometry_id)
        result = {"id": geometry_id, "name": geometry_name, "buffer": mesh_result[1], "indices": mesh_result[0]}
        return result

    def library_geometries_parser(root_node):
        """
        Parser of library_geometries element branch.
        It will return a list in following form:
            [geometryResult1, geometryResult2, ... , geometryResultN]
        for more investigation see result of geometry_parser.
        :param root_node:
        """
        geometries_results_list = []
        for c in root_node:
            if c.tag == geometry_tag:
                geometries_results_list.append(geometry_parser(c))
        return geometries_results_list

    library_geometries_result = None
    for child in root:
        if child.tag == library_geometries_tag:
            library_geometries_result = library_geometries_parser(child)
            #TODO: Other Collada properties must be implemented
