import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm

Base = declarative_base()

# Edges table - represents the pairs of Nodes
Edge = db.Table(
    "edges", Base.metadata,
    db.Column('source', db.Integer, db.ForeignKey('nodes.id'), primary_key=True),
    db.Column('target', db.Integer, db.ForeignKey('nodes.id'), primary_key=True)
)

# likes_association table - is a help table for relationships between comms and users
association_Likes = db.Table(
    'likes_association',
    Base.metadata,
    db.Column('likes_id', db.Integer, db.ForeignKey('likes.id')),
    db.Column('nodes_id', db.Integer, db.ForeignKey('nodes.id'))
)


class Like(Base):
    """
    Class representing the facebook page, community etc.
    """
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    facebook_id = db.Column(db.String)
    likers = orm.relationship(
        "Node",
        secondary=association_Likes,
        backref="likes_id"
    )

    def delete_all_likers(self):
        """Deletes the connection between like_page and the users"""
        while self.likers:
            self.likers.pop()


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

    likes = orm.relationship(
        "Like",
        secondary=association_Likes,
        backref="nodes_id"
    )

    def like_page(self, page):
        """Adds page to the user's list of likes"""
        if page not in self.likes:
            self.likes.append(page)

    def unlike_page(self, page):
        """Removes page from the user's list of likes"""
        if page in self.likes:
            self.likes.remove(page)

    def unlike_all_pages(self):
        """Removes all pages from the user's list of likes"""
        for like_page in self.likes:
            self.unlike_page(like_page)

    def add_friend(self, node):
        """Adds the node as a friend of the current Node"""
        if node not in self.friends:
            self.friends.append(node)
        if self not in node.friends:
            node.friends.append(self)

    def remove_all_friends(self):
        """Removes all friends pairs of the Node"""
        for friend in self.friends:
            # print(friend, friend.name)
            self.remove_friend(friend)

    def remove_friend(self, node):
        """Remove the friends pair"""
        if node in self.friends:
            self.friends.remove(node)
        if self in node.friends:
            node.friends.remove(self)

    def __eq__(self, other):
        """Checks if two Nodes are equal"""
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
        """Representation of the Node"""
        return "<Facebook user(Name: %s, Facebook ID: %s)>" % (self.name, self.facebook_id)


class NetworkGraph:
    """
    Class representing the facebook network graph
    """
    def __init__(self, file_name="default_file.db"):
        """
        Connects to the database in a new session
        :param file_name: the name of the database file
        """
        self.engine = db.create_engine('sqlite:///%s' % file_name)
        Base.metadata.create_all(self.engine)
        self.session = orm.sessionmaker(bind=self.engine)()

    def isNode(self, name, facebook_id):
        """Checks if the element with such name and facebook_id is in the database"""
        return self.session.query(Node).filter(Node.name == name,
                                               Node.facebook_id == facebook_id).count() >= 1

    def add_like_edge(self, node_user, like_page):
        """Adds like_page to node_user's list of likes"""
        if not isinstance(node_user, Node):
            raise(ValueError("node_user must be instance of Node"))
        if not isinstance(like_page, Like):
            raise(ValueError("like_page must me instance of Like"))
        page_identifier = self.session.query(Like).filter(Like.name == like_page.name,
                                                          Like.facebook_id == like_page.facebook_id)
        if page_identifier and page_identifier.count() < 1:
            raise(ValueError("like_page is not in database"))

        node_user.like_page(like_page)
        self.session.commit()

    def get_like_pages(self):
        """
        Returns the query instance of all like pages from database
        :return: query instance of Like.
        """
        return self.session.query(Like)

    def get_like_edges(self):
        """
        Returns the query instance of all like edges from database
        :return: query instance. Each tuple represents a like edge
        """
        return self.session.query(association_Likes)

    def delete_like_edge(self, node_user, like_page):
        """Removes like_page from node_user's list of likes"""
        if not isinstance(node_user, Node):
            raise(ValueError("node_user must be instance of Node"))
        if not isinstance(like_page, Like):
            raise(ValueError("like_page must me instance of Like"))
        node_user.unlike_page(like_page)
        # self.session.delete(like_page)
        self.session.commit()

    def findNode(self, name, facebook_id):
        """if exists returns the element from database
         with the name and facebook_id as given
         otherwise returns None"""
        if not self.isNode(name, facebook_id):
            return None
        return self.session.query(Node).filter(Node.name == name,
                                               Node.facebook_id == facebook_id).first()

    def add_like_page(self, name=None, facebook_id=None):
        """Adds a new like page into database"""
        page_identifier = self.session.query(Like).filter(Like.name == name,
                                                          Like.facebook_id == facebook_id)
        if page_identifier and page_identifier.count() > 0:
            return page_identifier.first()
        new_like_page = Like(name=name, facebook_id=facebook_id)
        self.session.add(new_like_page)
        self.session.commit()
        return new_like_page

    def delete_edge(self, source, target):
        """Deletes edge connection from database"""
        if not (isinstance(source, Node) and isinstance(target, Node)):
            raise TypeError("source and target must be Node")
        if not (self.isNode(source.name, source.facebook_id)
                and self.isNode(target.name, target.facebook_id)):
            raise ValueError("source and target must be in DB")
        source.remove_friend(target)
        self.session.commit()

    def delete_like_page(self, page):
        """Deletes like page"""
        if not isinstance(page, Like):
            raise ValueError("page must be an istance of Like")
        page_identifier = self.session.query(Like).filter(Like.name == page.name,
                                                          Like.facebook_id == page.facebook_id)
        if page_identifier and page_identifier.count() < 1:
            raise (ValueError("page is not in Database"))
        page = page_identifier.first()
        page.delete_all_likers()
        page_identifier.delete()
        self.session.commit()

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
        if node_identifier and node_identifier.count() > 0:
            return node_identifier.first()
        new_node = Node(name=name, facebook_id=facebook_id)
        self.session.add(new_node)
        self.session.commit()
        return new_node

    def add_edge(self, source, target):
        """Adds the edge with the left point source and the right point target"""
        if not (isinstance(source, Node) and isinstance(target, Node)):
            raise TypeError("source and target must be Node")
        if not (self.isNode(source.name, source.facebook_id)
                and self.isNode(target.name, target.facebook_id)):
            raise ValueError("source and target must be in DB")
        source.add_friend(target)
        self.session.commit()

    def delete_node(self, source=None, name=None, facebook_id=None):
        """
        Deletes the source Node from database
        :param source: instance of Node class
        :param name: name of the Node
        :param facebook_id: fb id of the Node
        """
        if source:
            source_identifier = self.get_nodes().filter(
                Node.name == source.name,
                Node.facebook_id == source.facebook_id
            )
        elif name and facebook_id:
            source_identifier = self.get_nodes().filter(
                Node.name == name,
                Node.facebook_id == facebook_id
            )
        else:
            source_identifier = None
        if source_identifier and source_identifier.count() > 0:
            source_identifier.first().remove_all_friends()
            source_identifier.first().unlike_all_pages()
            source_identifier.delete()
            self.session.commit()

    def get_nodes(self):
        """
        Returns the query instance of all nodes from database
        :return: query instance of nodes, each of them is instance of class Node
        """
        return self.session.query(Node)

    def get_edges(self):
        """
        Returns the query instance of all edges from database
        :return: query instance. Each tuple represents an edge
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
        """Gets the id from the url"""
        res_id = ""
        link = link.strip()
        if "profile.php" in link:
            id_index = link.find("id=") + 3
            for index in range(id_index, len(link)):
                if link[index] in "0123456789":
                    res_id += link[index]
                else:
                    return res_id
        elif "facebook.com/" in link:
            id_index = link.find("facebook.com/") + 13
            for index in range(id_index, len(link)):
                if link[index] in "/?&":
                    return res_id
                else:
                    res_id += link[index]
        else:
            res_id = link
        return res_id

    def export_graph(self, wnodes="nodes.csv", wedges="edges.csv"):
        """Writes the list of nodes into wnodes file and the list of edges
        into edges file in type of csv"""
        with open(wnodes, "w", encoding="utf-8") as filew:
            filew.write("ID,Label,FacebookId,Mode,Amount\n")
            for node in self.get_nodes().all():

                filew.write("%d,%s,%s,%d,%d\n" % (node.id, node.name, node.facebook_id, 0, 1))
            for like_page in self.get_like_pages().all():
                filew.write("%s,%s,%s,%d,%d\n" % ("L" + str(like_page.id), like_page.name.replace(",", " "), like_page.facebook_id, 1, len(like_page.likers)))
        with open(wedges, "w", encoding="utf-8") as filew:
            filew.write("Source,Target,Type\n")
            #for source, target in self.get_edges().all():
            #    filew.write("%d,%d,undirected\n" % (source, target))
            for source, target in self.get_like_edges().all():
                filew.write("L%d,%d,undirected\n" % (source, target))

    def read_friends_from_file(self, user, file, adding_new=True):
        """Reads the user friends from files of type: each name is followed by its
        facebook id in the next line. adding_new arg controls if the new arguments
        could be added or only existing could make new nodes"""
        with open(file, "r", encoding="utf-8") as data_file:
            content = data_file.readlines()

            length_half = len(content) // 2

            for index in range(length_half):
                name = content[index * 2].strip()
                facebook_id = self.id_from_url(content[index * 2 + 1].strip())

                new_node = self.findNode(name, facebook_id)
                if new_node is None:
                    if adding_new:
                        new_node = self.add_node(name=name, facebook_id=facebook_id)
                        self.add_edge(user, new_node)
                else:
                    self.add_edge(user, new_node)

    def users_from_file(self, file):
        """Reads the users from file of type: each name is followed by its
        facebook id in the next line"""
        with open(file, "r", encoding="utf-8") as data_file:
            content = data_file.readlines()

            length_half = len(content) // 2

            for index in range(length_half):
                name = content[index * 2].strip()
                facebook_id = self.id_from_url(content[index * 2 + 1].strip())
                if name and facebook_id:
                    self.add_node(name=name, facebook_id=facebook_id)
a= NetworkGraph(file_name="data/nm.db")
a.export_graph()
# print(a.get_like_pages().all())