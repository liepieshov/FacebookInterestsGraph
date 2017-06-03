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
            raise(ValueError("%s must be Node or dict" % str(other)))

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

    def add_node(self, name=None, facebook_id=None):
        """
        Adds a new Node with name and facebook_id into the database
        :param name: (str) name of the user
        :param facebook_id: (str) id of the user's facebook page
        """
        new_node = Node(name=name, facebook_id=facebook_id)
        self.session.add(new_node)
        self.session.commit()

    def delete_node(self, source):
        """
        Deletes the source Node from database
        :param source: instance of Node class
        """
        pass

    def get_nodes(self):
        """
        Returns the list of all nodes from database
        :return: list of nodes, each of them is instance of class Node
        """
        return self.session.query(Node).all()

    def get_edges(self):
        """
        Returns the list of all edges from database
        :return: list of tuples of ids. Each tuple represents an edge
        """
        return self.session.query(Edge).all()

    def find_neighbours(self, source):
        """
        Finds the neighbours of the source Node
        :param source: instance of Node class
        :return: the list of Nodes
        """
        pass

    def find_path(self, source, target):
        """
        Finds the shortest path between two Nodes
        :param source: instance of Node class, from which the path is starting
        :param target: instance of Node class, where the path finishes
        :return: generator of nodes of the path if the path exists otherwise False
        """
        pass

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
