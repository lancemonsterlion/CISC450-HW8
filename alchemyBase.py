from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(Text)
    email = Column(Text)
    password = Column(Text)

    # relationship with UserLibrary and GameLists
    user_libraries = relationship("UserLibrary", back_populates="user")
    game_lists = relationship("GameList", back_populates="user")
    reviews = relationship("Review", back_populates="user")


class Game(Base):
    __tablename__ = "Games"

    game_id = Column(Integer, primary_key=True)
    title = Column(Text)
    platform = Column(Text)
    metacritic_score = Column(Integer)
    genre = Column(Text)

    # Foreign key relationship to ListEntries
    list_entries = relationship("ListEntry", back_populates="game")
    reviews = relationship("Review", back_populates="game")


class ListEntry(Base):
    __tablename__ = "List Entries"

    list_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("Games.game_id"))
    rating = Column(Integer)
    comments = Column(Text)

    # Foreign key references
    game = relationship("Game", back_populates="list_entries")  # Corrected here
    game_list = relationship("GameList", back_populates="list_entries")


class Message(Base):
    __tablename__ = "Messages"

    message_id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("Users.user_id"))
    recipient_id = Column(Integer, ForeignKey("Users.user_id"))
    content = Column(Text)

    sender = relationship("User", foreign_keys=[sender_id], backref="sent_messages")
    recipient = relationship(
        "User", foreign_keys=[recipient_id], backref="received_messages"
    )


class FriendList(Base):
    __tablename__ = "friend_list"

    requestor_id = Column(Integer, ForeignKey("Users.user_id"), primary_key=True)
    recipient_id = Column(Integer, ForeignKey("Users.user_id"), primary_key=True)
    accepted = Column(Boolean)

    requestor = relationship(
        "User", foreign_keys=[requestor_id], backref="sent_friend_requests"
    )
    recipient = relationship(
        "User", foreign_keys=[recipient_id], backref="received_friend_requests"
    )


class GameList(Base):
    __tablename__ = "Game Lists"

    list_id = Column(Integer, ForeignKey("List Entries.list_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    list_name = Column(Text)
    list_type = Column(Text)
    likes = Column(Integer)

    # relationships
    list_entries = relationship("ListEntry", back_populates="game_list")  # Corrected here
    user = relationship("User", back_populates="game_lists")


class UserLibrary(Base):
    __tablename__ = "User Library"

    user_id = Column(Integer, ForeignKey("Users.user_id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("Games.game_id"), primary_key=True)
    user_score = Column(Integer)

    # relationships
    user = relationship("User", back_populates="user_libraries")
    game = relationship("Game", backref="user_libraries")


class Review(Base):
    __tablename__ = "Reviews"

    review_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("Games.game_id"))
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    review_body = Column(Text)
    review_score = Column(Integer)

    game = relationship("Game", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


# Create the database engine (replace with your own connection string)

engine = create_engine(
    "sqlite:///:memory:"
)  # Example using an in-memory SQLite database


# Create all the tables in the database

Base.metadata.create_all(engine)
