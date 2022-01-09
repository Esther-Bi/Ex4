class Node:

    def __init__(self, n_id: int = 0, x: float = None, y: float = None):

        self.id = n_id
        self.weight = float('inf')
        self.x = x
        self.y = y
        self.edge_out = {}
        self.edge_in = {}
        self.father = None
        self.visited = False

    def __str__(self):
        return f'{self.id}: |edges_out| {len(self.edge_out)} |edges in| {len(self.edge_in)}'

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self):
        return f'{self.id}: |edges_out| {len(self.edge_out)} |edges in| {len(self.edge_in)}'