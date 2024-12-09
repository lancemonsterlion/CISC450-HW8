from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from alchemyBase import Base, ListEntry, User, Message, Game, FriendList, GameList, UserLibrary, Review

def add_more_games():
    try:
        # List of new games to add
        games = [
            {"title": "The Witcher 3: Wild Hunt", "platform": "PC", "metacritic_score": 93, "genre": "RPG"},
            {"title": "God of War", "platform": "PlayStation", "metacritic_score": 94, "genre": "Action"},
            {"title": "Red Dead Redemption 2", "platform": "Xbox", "metacritic_score": 97, "genre": "Adventure"},
            {"title": "Celeste", "platform": "PC", "metacritic_score": 91, "genre": "Platformer"},
            {"title": "Hades", "platform": "PC", "metacritic_score": 93, "genre": "Roguelike"},
            {"title": "Hollow Knight", "platform": "PC", "metacritic_score": 90, "genre": "Metroidvania"},
            {"title": "Elden Ring", "platform": "PlayStation", "metacritic_score": 96, "genre": "Action RPG"},
            {"title": "The Legend of Zelda: Breath of the Wild", "platform": "Nintendo Switch", "metacritic_score": 97, "genre": "Action-Adventure"},
            {"title": "Stardew Valley", "platform": "PC", "metacritic_score": 89, "genre": "Simulation"},
            {"title": "Minecraft", "platform": "PC", "metacritic_score": 93, "genre": "Sandbox"},
        ]

        # Add games to the session
        for game in games:
            new_game = Game(
                title=game["title"],
                platform=game["platform"],
                metacritic_score=game["metacritic_score"],
                genre=game["genre"],
            )
            session.add(new_game)
        
        # Commit to the database
        session.commit()
        print("10 new games have been successfully added to the database.")
    
    except Exception as e:
        print(f"An error occurred while adding games: {e}")

# Replace 'sqlite:///example.db' with your database URL
engine = create_engine('sqlite:///backloggd.db')
Session = sessionmaker(bind=engine)
session = Session()

# Insert data into Users table
users = [
    {"user_name": "Alice", "email": "alice@example.com", "password": "password123"},
    {"user_name": "Bob", "email": "bob@example.com", "password": "securepass"},
    {"user_name": "Charlie", "email": "charlie@example.com", "password": "passw0rd"},
    {"user_name": "Diana", "email": "diana@example.com", "password": "myp@ssword"},
    {"user_name": "Eve", "email": "eve@example.com", "password": "12345secure"},
]
session.bulk_insert_mappings(User, users)

# Insert data into Games table
games = [
    {"title": "The Legend of Zelda", "platform": "Nintendo Switch", "metacritic_score": 96, "genre": "Action-Adventure"},
    {"title": "God of War", "platform": "PlayStation", "metacritic_score": 94, "genre": "Action"},
    {"title": "Minecraft", "platform": "PC", "metacritic_score": 86, "genre": "Sandbox"},
    {"title": "Fortnite", "platform": "PC", "metacritic_score": 81, "genre": "Battle Royale"},
    {"title": "Overwatch 2", "platform": "PC", "metacritic_score": 79, "genre": "Shooter"},
]
session.bulk_insert_mappings(Game, games)

# Insert data into List Entries table
list_entries = [
    {"list_id": 1, "game_id": 1, "rating": 10, "comments": "A masterpiece of game design."},
    {"list_id": 2, "game_id": 2, "rating": 9, "comments": "Amazing graphics and gameplay."},
    {"list_id": 3, "game_id": 3, "rating": 8, "comments": "Very creative and fun to play."},
    {"list_id": 4, "game_id": 4, "rating": 7, "comments": "Fun with friends, but repetitive."},
    {"list_id": 5, "game_id": 5, "rating": 7, "comments": "Good mechanics, but not groundbreaking."},
]
session.bulk_insert_mappings(ListEntry, list_entries)

# Insert data into Messages table
messages = [
    {"message_id": 1, "sender_id": 1, "recipient_id": 2, "content": "Hey Bob, what's up?"},
    {"message_id": 2, "sender_id": 2, "recipient_id": 3, "content": "Charlie, did you check this out?"},
    {"message_id": 3, "sender_id": 3, "recipient_id": 4, "content": "Hi Diana, long time no see!"},
    {"message_id": 4, "sender_id": 4, "recipient_id": 5, "content": "Eve, great to connect again."},
    {"message_id": 5, "sender_id": 5, "recipient_id": 1, "content": "Alice, let's catch up soon."},
]
session.bulk_insert_mappings(Message, messages)

# Insert data into Friend List table
friend_lists = [
    {"requestor_id": 1, "recipient_id": 2, "accepted": True},
    {"requestor_id": 1, "recipient_id": 3, "accepted": True},
    {"requestor_id": 2, "recipient_id": 4, "accepted": True},
    {"requestor_id": 3, "recipient_id": 5, "accepted": False},
    {"requestor_id": 4, "recipient_id": 5, "accepted": True},
]
session.bulk_insert_mappings(FriendList, friend_lists)

# Insert data into Game Lists table
game_lists = [
    {"user_id": 1, "list_name": "Favorite Games", "list_type": "Favorites", "likes": 15},
    {"user_id": 2, "list_name": "To Play", "list_type": "Wishlist", "likes": 10},
    {"user_id": 3, "list_name": "Completed", "list_type": "Completed", "likes": 8},
    {"user_id": 4, "list_name": "Multiplayer Games", "list_type": "Favorites", "likes": 20},
    {"user_id": 5, "list_name": "Indie Favorites", "list_type": "Favorites", "likes": 12},
]
session.bulk_insert_mappings(GameList, game_lists)

# Insert data into User Library table
user_libraries = [
    {"user_id": 1, "game_id": 1, "user_score": 10},
    {"user_id": 1, "game_id": 2, "user_score": 9},
    {"user_id": 2, "game_id": 3, "user_score": 8},
    {"user_id": 3, "game_id": 4, "user_score": 7},
    {"user_id": 4, "game_id": 5, "user_score": 7},
]
session.bulk_insert_mappings(UserLibrary, user_libraries)

# Insert data into Reviews table
reviews = [
    {"game_id": 1, "user_id": 1, "review_body": "An absolute classic!", "review_score": 10},
    {"game_id": 2, "user_id": 2, "review_body": "Loved the story and characters.", "review_score": 9},
    {"game_id": 3, "user_id": 3, "review_body": "A creative sandbox experience.", "review_score": 8},
    {"game_id": 4, "user_id": 4, "review_body": "Fun with friends, but can get old fast.", "review_score": 7},
    {"game_id": 5, "user_id": 5, "review_body": "Great mechanics but lacking polish.", "review_score": 7},
]
session.bulk_insert_mappings(Review, reviews)

# Commit the session to persist data
session.commit()
print("Dummy data inserted successfully!")

add_more_games()