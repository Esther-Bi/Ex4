import json
import random

from Node import Node


class DiGraph:

    def __init__(self, str_json: str = None) -> None:
        self.mc = 0
        self.nodes = {}
        if str_json is None:
            return
        try:
            dict_building = json.loads(str_json)
            for dict_of_node in dict_building['Nodes']:
                id = dict_of_node["id"]
                try:
                    pos = dict_of_node["pos"]
                    pos_list = pos.split(",")
                    x = float(pos_list[0])
                    y = float(pos_list[1])
                    n = Node(id, x, y)
                except:
                    x = random.randint(0, 20)
                    y = random.randint(0, 20)
                    pos = (x, y)
                    n = Node(id, pos[0], pos[1])
                self.nodes[id] = n
            for dict_of_edge in dict_building['Edges']:
                src = dict_of_edge["src"]
                weight = dict_of_edge["w"]
                dest = dict_of_edge["dest"]

                self.nodes[src].edge_out[dest] = weight
                self.nodes[dest].edge_in[src] = weight

        except json.decoder.JSONDecodeError:
            print("String could not be converted to JSON")

    def __str__(self):
        return f"Graph: |V|={self.v_size()}, |E|={self.e_size()}"

    def __repr__(self):
        return f"Graph: |V|={self.v_size()}, |E|={self.e_size()}"

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        num = 0
        for node in self.nodes:
            num = num + len(self.nodes[node].edge_out)
        return num

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.nodes[id1].edge_in

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.nodes[id1].edge_out

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        try:
            self.nodes[id1].edge_out[id2] = weight
            self.nodes[id2].edge_in[id1] = weight
            self.mc += 1
            return True
        except:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        try:
            if pos is None:
                x = random.randint(0, 20)
                y = random.randint(0, 20)
                pos = (x, y)
            n = Node(node_id, pos[0], pos[1])
            self.nodes[node_id] = n
            self.mc += 1
            return True
        except:
            return False

    def remove_node(self, node_id: int) -> bool:
        try:
            for k, w in self.nodes.get(node_id).edge_in.items():
                self.nodes.get(k).edge_out.pop(node_id)
            self.nodes.get(node_id).edge_in.clear()
            for k, w in self.nodes.get(node_id).edge_out.items():
                self.nodes.get(k).edge_in.pop(node_id)
            self.nodes.get(node_id).edge_out.clear()
            del self.nodes[node_id]
            self.mc += 1
            return True
        except:
            return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        try:
            del self.nodes[node_id1].edge_out[node_id2]
            del self.nodes[node_id2].edge_in[node_id1]
            self.mc += 1
            return True
        except:
            return False

    def return_dict(self):
        a = "Edges"
        b = "Nodes"
        edges = []
        for nod_id, node in self.nodes.items():
            for dest, w in node.edge_out.items():
                dict = {}
                dict["src"] = nod_id
                dict["w"] = w
                dict["dest"] = dest
                edges.append(dict)
        node_list = []
        for nod_id, node in self.nodes.items():
            dict = {}
            dict["pos"] = str(node.x) + "," + str(node.y)
            dict["id"] = nod_id
            node_list.append(dict)

        return {a: edges, b: node_list}