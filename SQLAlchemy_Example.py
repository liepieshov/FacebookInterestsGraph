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
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    friends = orm.relationship('Node',
                               secondary=Edge,
                               primaryjoin=id == Edge.c.source,
                               secondaryjoin=id == Edge.c.target,
                               backref='source'
                               )

    def __repr__(self):
        return "<%s>" % self.label
engine = db.create_engine('sqlite:///one.db')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session = orm.sessionmaker(bind=engine)()
a = Node(label="A")
b = Node(label="ABC")
a.friends = [b]
session.add_all([a, b])
session.commit()
print(len(session.query(Node).all()))
print(session.query(Node).filter("KostyaASD" == Node.label).delete())
print(session.query(Node).all())
