import unittest
from DiGraph import DiGraph
# from client_python.DiGraph import DiGraph


class MyTestCase(unittest.TestCase):
    global graph
    graph = DiGraph()

    graph.add_node(1)
    graph.add_node(2)
    graph.add_node(3)

    graph.add_node(4)
    graph.add_edge(1, 2, 0.5)
    graph.add_edge(2, 3, 0.7)

    graph.add_node(5)
    graph.add_edge(5, 3, 1)

    graph.add_edge(4, 1, 0.9)
    graph.add_edge(4, 2, 1.1)

    graph.add_edge(1, 4, 0.9)
    graph.add_edge(2, 4, 1.1)
    graph.add_edge(3, 4, 0.8)

    def test_v_size(self):
        self.assertEqual(graph.v_size(), 5)
        graph.add_node(6)
        self.assertEqual(graph.v_size(), 6)
        graph.remove_node(6)


    def test_e_size(self):
        self.assertEqual(graph.e_size(), 9)
        graph.add_edge(2, 1, 0.3)
        self.assertEqual(graph.e_size(), 10)


    def test_get_all_v(self):
        self.assertEqual(len(graph.get_all_v()), graph.v_size())

    def test_all_in_edges_of_node(self):
        self.assertEqual(len(graph.all_in_edges_of_node(4)), 3)

    def test_all_out_edges_of_node(self):
        self.assertEqual(len(graph.all_in_edges_of_node(4)), 3)

    def test_get_mc(self):
        self.assertEqual(graph.get_mc(), 16)

    def test_add_edge(self):
        self.assertEqual(graph.e_size(), 8)
        graph.add_edge(4, 3, 1)
        self.assertEqual(graph.e_size(), 9)


    def test_add_node(self):
        self.assertEqual(graph.v_size(), 5)
        graph.add_node(8)
        self.assertEqual(graph.v_size(), 6)


    def test_remove_node(self):
        graph.add_edge(5, 3, 1)
        self.assertEqual(graph.v_size(), 6)
        self.assertEqual(graph.e_size(), 9)
        graph.remove_node(5)
        self.assertEqual(graph.v_size(), 5)
        self.assertEqual(graph.e_size(), 8)


    def test_remove_edge(self):
        graph.add_edge(4, 3, 1)
        self.assertEqual(graph.e_size(), 10)
        graph.remove_edge(4, 3)
        self.assertEqual(graph.e_size(), 9)


if __name__ == '__main__':
    unittest.main()
