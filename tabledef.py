from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from inspector import config

engine = create_engine(config.DATABASE_URL, echo=True)
Base = declarative_base()


########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer)
    name = Column(String)
    username = Column(String, primary_key=True)
    password = Column(String)
    user_policy = Column(String)
    creation_date = Column(String)
    active = Column(Boolean)

    # ----------------------------------------------------------------------
    def __init__(self, name, username, password, user_policy, creation_date, active):
        """"""
        self.name = name
        self.username = username
        self.password = password
        self.user_policy = user_policy
        self.creation_date = creation_date
        self.active = active


# #  create tables
#         Base.metadata.create_all(engine)

#         engine = create_engine(config.DATABASE_URL, echo=True)

# #  create a Session
#         Sessionmaker = sessionmaker(bind=engine)
#         sessionmaker = Sessionmaker()

#         user = User("Admin User", "admin@payfort.com", "85abcec2435819f27b76fc72eb9574d49b4d6fe19f70d96ecfbb7ca0efcf7f47", "admin", "08-02-2020", True)
#         sessionmaker.add(user)


        user = User("Admin User", "user@payfort.com", "85abcec2435819f27b76fc72eb9574d49b4d6fe19f70d96ecfbb7ca0efcf7f47", "admin", "08-02-2020", True)
        sessionmaker.add(user)

# user = User("adaoud@payfort.com", "ccee544c307acebbe2d1a1f3ca6f1b9f6519384c40789c04fdf42cfb0516b510", "admin", "08-02-2020", False)
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
        sessionmaker.commit()
