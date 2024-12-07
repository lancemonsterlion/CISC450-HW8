from sqlalchemy import create_engine

# import our models from the other file
from alchemyBase import Base, ListEntry, User, Message, Game, FriendList, GameList, UserLibrary, Review

# to show the sql that is running
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Create database
engine = create_engine('sqlite:///backloggd.db')

# this will actually construct the tables from the objects
Base.metadata.create_all(engine)