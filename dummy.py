from tabledef import *

engine = create_engine(config.DATABASE_URL, echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("Admin User", "adaoud@payfort.com", "85abcec2435819f27b76fc72eb9574d49b4d6fe19f70d96ecfbb7ca0efcf7f47", "admin", "08-02-2020", True)
session.add(user)

# user = User("adaoud@payfort.com", "93cd8446013be804e0c9a69741aa13be76ac696f9a274789519d40bf19fe723a", "super_user")
# session.add(user)
#
# user = User("test@payfort.com", "dd4c210f4869889bd81d9e28391d36e709b89d51d98d8745cffefc2774102d2a", "user")
# session.add(user)
#
# # commit the record the database
# session.commit()


