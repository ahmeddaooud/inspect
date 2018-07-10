from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///inspector.db', echo=True)
Base = declarative_base()


########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    userpolicy = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, username, password, userpolicy):
        """"""
        self.username = username
        self.password = password
        self.userpolicy = userpolicy


# create tables
# Base.metadata.create_all(engine)

engine = create_engine('sqlite:///inspector.db', echo=True)

# create a Session
# Sessionmaker = sessionmaker(bind=engine)
# sessionmaker = Sessionmaker()
#
# user = User("admin@payfort.com", "ccee544c307acebbe2d1a1f3ca6f1b9f6519384c40789c04fdf42cfb0516b510", "admin")
# sessionmaker.add(user)
#
# user = User("adaoud@payfort.com", "93cd8446013be804e0c9a69741aa13be76ac696f9a274789519d40bf19fe723a", "super_user")
# sessionmaker.add(user)
#
# user = User("test@payfort.com", "dd4c210f4869889bd81d9e28391d36e709b89d51d98d8745cffefc2774102d2a", "user")
# sessionmaker.add(user)
#
# # commit the record the database
# sessionmaker.commit()
#
# sessionmaker.commit()