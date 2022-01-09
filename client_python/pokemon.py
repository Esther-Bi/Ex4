import json
import math
from pygame import Color

from client_python.DiGraph import DiGraph


class Pokemon:

    def __init__(self, value: float = 0.0, type: int = 1, pos: str = "0.0,0.0,0.0", graph: DiGraph = None):
        self.value = value
        self.type = type
        p = pos.split(",")
        self.x = float(p[0])
        self.y = float(p[1])
        if type < 0:
            self.color = 1
        if type > 0:
            self.color = 2
        found_src = None
        found_dest = None
        for src in graph.nodes.keys():
            src_node_x = graph.nodes[src].x
            src_node_y = graph.nodes[src].y
            for dest in graph.all_out_edges_of_node(src).keys():
                dest_node_x = graph.nodes[dest].x
                dest_node_y = graph.nodes[dest].y
                if (type > 0 and src < dest) or (type < 0 and src > dest):
                    real_length = math.dist([src_node_x, src_node_y], [dest_node_x, dest_node_y])
                    trial_length = math.dist([src_node_x, src_node_y], [self.x, self.y]) + math.dist([self.x, self.y],
                                                                                                     [dest_node_x,
                                                                                                      dest_node_y])
                    if trial_length - 0.0000001 <= real_length <= trial_length + 0.0000001:
                        found_src = src
                        found_dest = dest
                if found_src is not None:
                    break
            if found_src is not None:
                break
        self.src = found_src
        self.dest = found_dest


class Pokemons:

    def __init__(self, file_name: str = None, graph: DiGraph = None):

        self.pokemon_list = []
        try:
            dict_building = json.loads(file_name)
            for P in dict_building['Pokemons']:
                data = P['Pokemon']
                value = float(data['value'])
                type = int(data['type'])
                pos = data['pos']
                a = Pokemon(value, type, pos, graph)
                self.pokemon_list.append(a)

        except json.decoder.JSONDecodeError:
            print("String could not be converted to JSON")
