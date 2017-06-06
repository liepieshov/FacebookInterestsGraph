import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm

Base = declarative_base()
Edge = db.Table(
    "edges", Base.metadata,
    db.Column('source', db.Integer, db.ForeignKey('nodes.id'), primary_key=True),
    db.Column('target', db.Integer, db.ForeignKey('nodes.id'), primary_key=True)
)


class Node(Base):
    """
    Class representing Node of the NetworkGraph using sqlalchemy
    """
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    facebook_id = db.Column(db.String)
    friends = orm.relationship('Node',
                               secondary=Edge,
                               primaryjoin=id == Edge.c.source,
                               secondaryjoin=id == Edge.c.target,
                               backref='source'
                               )

    def add_friend(self, node):
        if node not in self.friends:
            self.friends.append(node)
        if self not in node.friends:
            node.friends.append(self)

    def remove_all_friends(self):
        for friend in self.friends:
            # print(friend, friend.name)
            self.remove_friend(friend)

    def remove_friend(self, node):
        if node in self.friends:
            self.friends.remove(node)
        if self in node.friends:
            node.friends.remove(self)

    def __eq__(self, other):
        if isinstance(other, Node):
            if self.name == other.name and self.facebook_id == other.facebook_id:
                return True
            else:
                return False
        elif isinstance(other, dict):
            if self.name == other["name"] and self.facebook_id == other["facebook_id"]:
                return True
            else:
                return False
        else:
            raise (ValueError("%s must be Node or dict" % str(other)))

    def __repr__(self):
        return "<Facebook user(Name: %s, Facebook ID: %s)>" % (self.name, self.facebook_id)


class NetworkGraph:
    """
    Class representing the facebook network graph
    """

    def __init__(self, file_name):
        """
        Connects to the database in a new session
        :param file_name: the name of the database file
        """
        self.engine = db.create_engine('sqlite:///%s' % file_name)
        Base.metadata.create_all(self.engine)
        self.session = orm.sessionmaker(bind=self.engine)()

    def clear(self):
        """
        Drops all the tables of the database
        """
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def add_node(self, name=None, facebook_id=None):
        """
        Adds a new Node with name and facebook_id into the database
        :param name: (str) name of the user
        :param facebook_id: (str) id of the user's facebook page
        """
        node_identifier = self.get_nodes().filter(Node.name == name, Node.facebook_id == facebook_id)
        if node_identifier.count() > 0:
            return node_identifier.first()
        new_node = Node(name=name, facebook_id=facebook_id)
        self.session.add(new_node)
        self.session.commit()
        return new_node

    def add_edge(self, source, target):
        source.add_friend(target)
        self.session.commit()

    def delete_node(self, source):
        """
        Deletes the source Node from database
        :param source: instance of Node class
        """
        source_identifier = self.get_nodes().filter(
            Node.name == source.name,
            Node.facebook_id == source.facebook_id
        )
        if source_identifier.count() > 0:
            source_identifier.first().remove_all_friends()
            source_identifier.delete()
            self.session.commit()

    def get_nodes(self):
        """
        Returns the list of all nodes from database
        :return: list of nodes, each of them is instance of class Node
        """
        return self.session.query(Node)

    def get_edges(self):
        """
        Returns the list of all edges from database
        :return: list of tuples of ids. Each tuple represents an edge
        """
        return self.session.query(Edge)

    def find_neighbours(self, source):
        """
        Finds the neighbours of the source Node
        :param source: instance of Node class
        :return: the list of Nodes
        """
        if not isinstance(source, Node):
            raise ValueError

        source_identifier = self.get_nodes().filter(
            Node.name == source.name,
            Node.facebook_id == source.facebook_id
        )
        if source_identifier.count() < 1:
            return list()
        else:
            # print(source_identifier.all()[0])
            return source_identifier.all()[0].friends

    def find_path(self, source, target):
        """
        Finds the shortest path between two Nodes
        :param source: instance of Node class, from which the path is starting
        :param target: instance of Node class, where the path finishes
        :return: list of nodes of the path if the path exists otherwise None
        """

        def find_shortest_path(graph, start, end, path=list()):
            path = path + [start]
            if start == end:
                return path
            shortest = None
            for node in graph.find_neighbours(start):
                if node not in path:
                    newpath = find_shortest_path(graph, node, end, path)
                    if newpath:
                        if not shortest or len(newpath) < len(shortest):
                            shortest = newpath
            return shortest

        return find_shortest_path(self, source, target)

    @staticmethod
    def id_from_url(link):
        res_id = ""
        link = link.strip()
        if "profile.php" in link:
            id_index = link.find("id=") + 3
            for index in range(id_index, len(link)):
                if link[index] in "0123456789":
                    res_id += link[index]
                else:
                    return res_id
        else:
            id_index = link.find("facebook.com/") + 13
            for index in range(id_index, len(link)):
                if link[index] in "/?&":
                    return res_id
                else:
                    res_id += link[index]

    def write_gephi(self, wnodes="nodes.csv", wedges="edges.csv"):
        with open(wnodes, "w", encoding="utf-8") as filew:
            filew.write("ID,Label,FB_ID\n")
            for node in self.get_nodes().all():
                filew.write("%d,%s,%s\n" % (node.id, node.name, node.facebook_id))
        with open(wedges, "w", encoding="utf-8") as filew:
            filew.write("Source,Target\n")
            for source, target in self.get_edges().all():
                filew.write("%d,%d\n" % (source, target))

    def read_friends_from_file(self, user, file):
        with open(file, "r", encoding="urf-8") as data_file:
            content = data_file.readlines()

            length_half = len(content) // 2

            for index in range(length_half):
                name = content[index * 2]
                facebook_id = self.id_from_url(content[index * 2 + 1])

                new_node = self.add_node(name=name, facebook_id=facebook_id)
                user.add_friend(new_node)

                # engine = db.create_engine('sqlite:///one.db')

                # Base.metadata.drop_all(engine)
                # Base.metadata.create_all(engine)

                # print(len(session.query(Node).all()))

                # session.query(Node).filter("A" == Node.name).delete()
                # session.commit()

                # print(session.query(Node).all())
                # a = NetworkGraph("one.db")


                # print(a.session.query(NetworkGraph.Node).all())
                # print(a, a.session.query(a.Node).all())

                # def read_from_files(file_name, db_file_name, reload=True):
                #     data_base = NetworkGraph(db_file_name)
                # a = NetworkGraph("one.db")
                # a.clear()
                # a.session.add(Node(name="KOSTYA", facebook_id="12345"))
                # a.session.commit()
                # print(a.delete_node(a.get_nodes().filter(Node.name=="KOSTYA")[0]))
                # a.clear()
                # print(a.is_empty())
                # b = a.add_node(name="Kostya", facebook_id="kostia")
                # a.read_friends_from_file(b, "../db_interested/Kostya Liepieshov.txt")
                # print(a.get_edges().all())
                # print(NetworkGraph.id_from_url("https://www.facebook.com/sirenko.anastasia/about?lst=100007370378704%3A100000265076800%3A1496709410"))
                # print(NetworkGraph.id_from_url("https://www.facebook.com/profile.php?id=100004425577587&lst=100007370378704%3A100004425577587%3A1496708749&sk=friends&source_ref=pb_friends_tl"))
                # a = NetworkGraph("one.db")
                # a.clear()
                # A = a.add_node(name="A", facebook_id="a")
                # B = a.add_node(name="B", facebook_id="b")
                # C = a.add_node(name="C", facebook_id="c")
                # a.add_edge(A, B)
                # a.add_edge(B, C)
                # print(a.get_nodes().all(), a.get_edges().all())
                # print(a.find_path(A, C))
                # a.write_gephi()
