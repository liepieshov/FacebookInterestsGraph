# File: tests/test_facebook_network_graph.py
import unittest
from facebook_network_graph.facebook_network_graph import NetworkGraph


class TestNetworkGraph(unittest.TestCase):
    def setUp(self):
        self.graph = NetworkGraph(file_name=":memory:")

    def tearDown(self):
        self.graph.clear()
        self.graph = None

    def test_isNode_false(self):
        self.assertEquals(self.graph.isNode("Test", "id"), False)

    def test_isNode_true(self):
        self.graph.add_node("Test", "id")
        self.assertEquals(self.graph.isNode("Test", "id"), True)

    def test_findNode_true(self):
        test_node = self.graph.add_node("Test", "id")
        self.assertEquals(self.graph.findNode(test_node.name, test_node.facebook_id),
                          test_node)

    def test_findNode_false(self):
        self.assertEquals(self.graph.findNode("Test", "id"), None)

    def test_clear(self):
        self.graph.add_node("Test", "id")
        self.graph.clear()
        self.assertEquals(self.graph.findNode("Test", "id"), None)

    def test_get_nodes_exists_one(self):
        self.graph.add_node("Test", "id")
        self.assertEquals(self.graph.get_nodes().count(), 1)

    def test_get_nodes_exists_zero(self):
        self.assertEquals(self.graph.get_nodes().count(), 0)

    def test_id_from_url(self):
        self.assertEquals(self.graph.id_from_url(
            "https://www.facebook.com/idofuser"),
            "idofuser"
        )
        self.assertEquals(
            self.graph.id_from_url(
                "https://www.facebook.com/idofuser?fref=pb&hc_location=friends_tab"),
            "idofuser"
        )
        self.assertEquals(
            self.graph.id_from_url(
                "https://www.facebook.com/profile.php?id=12345678"
                "&fref=pb&hc_location=friends_tab"),
            "12345678"
        )

    def test_delete_node_exists_inst(self):
        self.graph.add_node("Test", "id")
        del_node = self.graph.add_node("TestDelete", "id")
        self.graph.delete_node(del_node)
        self.assertEquals(self.graph.get_nodes().count(), 1)

    def test_delete_node_exists_name_id(self):
        self.graph.add_node("Test", "id")
        self.graph.add_node("TestDelete", "id")
        self.graph.delete_node(name="TestDelete", facebook_id="id")
        self.assertEquals(self.graph.get_nodes().count(), 1)

    def test_delete_node_not_exists(self):
        self.graph.add_node("TestDelete", "id")
        test_amount = self.graph.get_nodes().count()
        self.graph.delete_node(name="Test", facebook_id="id")
        self.assertEquals(self.graph.get_nodes().count(), test_amount)

    def test_add_node_not_exists(self):
        test_node = self.graph.add_node("Test", "id")
        self.assertEquals(self.graph.findNode(name=test_node.name,
                                              facebook_id=test_node.facebook_id),
                          test_node)

    def test_add_node_exists(self):
        self.graph.add_node("Test", "id")
        self.assertEquals(self.graph.isNode(name="Test", facebook_id="id"), True)
        test_amount = self.graph.get_nodes().count()
        self.graph.add_node("Test", "id")
        self.assertEquals(self.graph.get_nodes().count(), test_amount)

    def test_add_edge(self):
        a = self.graph.add_node("Test_A", "id")
        b = self.graph.add_node("Test_B", "id")
        self.graph.add_edge(a, b)
        self.assertEquals(self.graph.get_edges().count(), 2)
        self.graph.add_edge(b, a)
        self.assertEquals(self.graph.get_edges().count(), 2)

    def test_get_edges_not_exists(self):
        self.assertEquals(self.graph.get_edges().count(), 0)

    def test_get_edges_exists(self):
        a = self.graph.add_node("Test_A", "id")
        b = self.graph.add_node("Test_B", "id")
        self.graph.add_edge(a, b)
        self.assertEquals(self.graph.get_edges().count(), 2)

    def test_delete_edge_exists(self):
        a = self.graph.add_node("Test_A", "id")
        b = self.graph.add_node("Test_B", "id")
        self.graph.add_edge(a, b)
        self.graph.delete_edge(a, b)
        self.assertEquals(self.graph.get_edges().count(), 0)

    def test_delete_edge_not_exists(self):
        a = self.graph.add_node("Test_A", "id")
        b = self.graph.add_node("Test_B", "id")
        c = self.graph.add_node("Test_C", "id")
        self.graph.add_edge(a, b)
        self.graph.delete_edge(a, c)
        self.assertEquals(self.graph.get_edges().count(), 2)

    def test_delete_node_with_edges(self):
        a = self.graph.add_node("Test_A", "id")
        b = self.graph.add_node("Test_B", "id")
        self.graph.add_edge(a, b)
        self.graph.delete_node(a)
        self.assertEquals(self.graph.get_edges().count(), 0)

    def test_find_neighbours(self):
        a = self.graph.add_node("Test_A", "id")
        b = self.graph.add_node("Test_B", "id")
        c = self.graph.add_node("Test_C", "id")
        self.graph.add_edge(a, b)
        self.assertIn(b, self.graph.find_neighbours(a))
        self.assertNotIn(c, self.graph.find_neighbours(a))
        self.graph.add_edge(a, c)
        self.assertIn(b, self.graph.find_neighbours(a))
        self.assertIn(c, self.graph.find_neighbours(a))

    def test_find_path(self):
        a = self.graph.add_node("Test_A", "id")
        b = self.graph.add_node("Test_B", "id")
        c = self.graph.add_node("Test_C", "id")
        d = self.graph.add_node("Test_D", "id")
        e = self.graph.add_node("Test_E", "id")
        self.graph.add_edge(a, b)
        self.graph.add_edge(a, c)
        self.graph.add_edge(c, d)
        self.graph.add_edge(b, d)
        self.graph.add_edge(a, d)
        self.assertIsNone(self.graph.find_path(a, e))
        self.graph.add_edge(d, e)
        self.assertEquals(self.graph.find_path(a, e), [a, d, e])

    def test_add_like_page(self):
        test_page = self.graph.add_like_page(name="TestPage", facebook_id="id")
        self.assertEquals(self.graph.get_like_pages().count(), 1)
        self.graph.add_like_page(name="TestPage", facebook_id="id")
        self.assertEquals(self.graph.get_like_pages().first(), test_page)
        self.graph.add_like_page(name="TestPage2", facebook_id="id")
        self.assertEquals(self.graph.get_like_pages().count(), 2)

    def test_get_like_pages(self):
        self.assertEquals(self.graph.get_like_pages().count(), 0)
        self.graph.add_like_page(name="TestPage", facebook_id="id")
        self.assertEquals(self.graph.get_like_pages().count(), 1)

    def test_add_like_edge(self):
        test_user = self.graph.add_node("Test_User", "id")
        test_like_page = self.graph.add_like_page("Test_Page", "id")
        self.graph.add_like_edge(test_user, test_like_page)
        self.assertEquals(self.graph.get_like_edges().count(), 1)
        self.graph.add_like_edge(test_user, test_like_page)
        self.assertEquals(self.graph.get_like_edges().count(), 1)
        self.assertIn(test_like_page, test_user.likes)
        self.assertIn(test_user, test_like_page.likers)

    def test_get_like_edges(self):
        test_user = self.graph.add_node("Test_User", "id")
        test_like_page = self.graph.add_like_page("Test_Page", "id")
        self.assertEquals(self.graph.get_like_edges().count(), 0)
        self.graph.add_like_edge(test_user, test_like_page)
        self.assertEquals(self.graph.get_like_edges().count(), 1)

    def test_delete_like_page(self):
        test_user = self.graph.add_node("Test_User", "id")
        test_like_page = self.graph.add_like_page("Test_Page", "id")
        self.graph.add_like_edge(test_user, test_like_page)
        self.graph.delete_like_page(test_like_page)
        self.assertEquals(self.graph.get_like_edges().count(), 0)
        self.assertEquals(self.graph.get_like_pages().count(), 0)
        self.assertEquals(test_user.likes, [])

    def test_delete_node_like_page(self):
        test_user = self.graph.add_node("Test_User", "id")
        test_like_page = self.graph.add_like_page("Test_Page", "id")
        self.graph.add_like_edge(test_user, test_like_page)
        self.graph.delete_node(test_user)
        self.assertEquals(self.graph.get_like_edges().count(), 0)
        self.assertEquals(test_like_page.likers, [])

    def test_delete_like_edge(self):
        test_user = self.graph.add_node("Test_User", "id")
        test_like_page = self.graph.add_like_page("Test_Page", "id")
        self.graph.add_like_edge(test_user, test_like_page)
        self.graph.delete_like_edge(test_user, test_like_page)
        self.assertEquals(self.graph.get_like_edges().count(), 0)
        self.assertEquals(test_like_page.likers, [])
        self.assertEquals(test_user.likes, [])

if __name__ == "__main__":
    unittest.main()
