# import our models from the other file
from alchemyBase import Base, ListEntry, User, Message, Game, FriendList, GameList, UserLibrary, Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# to show the sql that is running
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# this is our "connection" to the database
engine = create_engine('sqlite:///backloggd.db')

# Now a session to start working with the database
Session = sessionmaker(bind=engine)
session = Session(expire_on_commit=False) # This parameter can reduce unnecessary SQL calls in some cases

users = [
    User(user_name="samlargaespada", email="sam.largaespada@stthomas.edu", password="password1"),
    User(user_name="antonlacson", email="anton.lacson@stthomas.edu", password="password2"),
    User(user_name="lancemunsterteiger", email="lance.munsterteiger@stthomas.edu", password="password3"),
]
session.add_all(users)


games = [
    Game(title="The Witcher 3: Wild Hunt", platform="PC", metacritic_score=93, genre="RPG"),
    Game(title="Red Dead Redemption 2", platform="PlayStation 4", metacritic_score=97, genre="Action-Adventure"),
    Game(title="Celeste", platform="Nintendo Switch", metacritic_score=92, genre="Platformer"),
    Game(title="Dark Souls III", platform="Xbox One", metacritic_score=89, genre="RPG"),
    Game(title="Hollow Knight", platform="PC", metacritic_score=90, genre="Metroidvania"),
]

# Add and commit the games to the database
session.add_all(games)


# Commit to db
session.commit()
