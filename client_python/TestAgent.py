import unittest
from Agent import Agents
from DiGraph import DiGraph

class MyTestCase(unittest.TestCase):


    str_agent= "{\"Agents\":[{\"Agent\":{\"id\":0,\"value\":0.0,\"src\":0,\"dest\":1,\"speed\":1.0,\"pos\":\"35.18753053591606,32.10378225882353,0.0\"}},{\"Agent\":{\"id\":1,\"value\":0.0,\"src\":0,\"dest\":1,\"speed\":1.0,\"pos\":\"36.18753053591606,33.10378225882353,0.0\"}}]}"
    str_agent_change = "{\"Agents\":[{\"Agent\":{\"id\":0,\"value\":0.0,\"src\":0,\"dest\":1,\"speed\":1.0,\"pos\":\"35.18753053591606,32.10378225882353,0.0\"}},{\"Agent\":{\"id\":1,\"value\":0.0,\"src\":2,\"dest\":3,\"speed\":1.0,\"pos\":\"36.18753053591606,33.10378225882353,0.0\"}}]}"
    str_graph = "{\"Edges\":[{\"src\":0,\"w\":1.4004465106761335,\"dest\":1},{\"src\":0,\"w\":1.4620268165085584,\"dest\":10},{\"src\":1,\"w\":1.8884659521433524,\"dest\":0},{\"src\":1,\"w\":1.7646903245689283,\"dest\":2},{\"src\":2,\"w\":1.7155926739282625,\"dest\":1},{\"src\":2,\"w\":1.1435447583365383,\"dest\":3},{\"src\":3,\"w\":1.0980094622804095,\"dest\":2},{\"src\":3,\"w\":1.4301580756736283,\"dest\":4},{\"src\":4,\"w\":1.4899867265011255,\"dest\":3},{\"src\":4,\"w\":1.9442789961315767,\"dest\":5},{\"src\":5,\"w\":1.4622464066335845,\"dest\":4},{\"src\":5,\"w\":1.160662656360925,\"dest\":6},{\"src\":6,\"w\":1.6677173820549975,\"dest\":5},{\"src\":6,\"w\":1.3968360163668776,\"dest\":7},{\"src\":7,\"w\":1.0176531013725074,\"dest\":6},{\"src\":7,\"w\":1.354895648936991,\"dest\":8},{\"src\":8,\"w\":1.6449953452844968,\"dest\":7},{\"src\":8,\"w\":1.8526880332753517,\"dest\":9},{\"src\":9,\"w\":1.4575484853801393,\"dest\":8},{\"src\":9,\"w\":1.022651770039933,\"dest\":10},{\"src\":10,\"w\":1.1761238717867548,\"dest\":0},{\"src\":10,\"w\":1.0887225789883779,\"dest\":9}],\"Nodes\":[{\"pos\":\"35.18753053591606,32.10378225882353,0.0\",\"id\":0},{\"pos\":\"35.18958953510896,32.10785303529412,0.0\",\"id\":1},{\"pos\":\"35.19341035835351,32.10610841680672,0.0\",\"id\":2},{\"pos\":\"35.197528356739305,32.1053088,0.0\",\"id\":3},{\"pos\":\"35.2016888087167,32.10601755126051,0.0\",\"id\":4},{\"pos\":\"35.20582803389831,32.10625380168067,0.0\",\"id\":5},{\"pos\":\"35.20792948668281,32.10470908739496,0.0\",\"id\":6},{\"pos\":\"35.20746249717514,32.10254648739496,0.0\",\"id\":7},{\"pos\":\"35.20319591121872,32.1031462,0.0\",\"id\":8},{\"pos\":\"35.19597880064568,32.10154696638656,0.0\",\"id\":9},{\"pos\":\"35.18910131880549,32.103618700840336,0.0\",\"id\":10}]}"

    global agents
    global graph
    graph = DiGraph(str_graph)
    agents= Agents(str_agent,graph)


    agents.agent_dict[0].add_task([1,2,3],4)
    agents.change_values(str_agent_change,graph)

    def test_init(self):
        self.assertEqual(agents.agent_dict[0].id, 0)
        self.assertEqual(agents.agent_dict[1].id, 1)  # add assertion here

    def test_add_task(self):
        self.assertEqual(agents.agent_dict[0].node_tasks, [1,2,3,4])

    def test_remove_task(self):
        agents.agent_dict[0].remove_task()
        self.assertEqual(agents.agent_dict[0].node_tasks, [2, 3,4])

    def test_already_taken(self):
        self.assertEqual(agents.agent_dict[0].already_taken(2,3), True)

    def test_change_values(self):
        self.assertEqual(agents.agent_dict[1].src, 2)
        self.assertEqual(agents.agent_dict[1].dest, 3)


if __name__ == '__main__':
    unittest.main()
