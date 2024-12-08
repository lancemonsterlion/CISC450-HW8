from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# from sqlalchemy.exc import NoResultFound
# from alchemyBase import Base, ListEntry, User, Message, Game, FriendList, GameList, UserLibrary, Review
from menu_functions import user_login, main_menu, add_user

if __name__ == "__main__":
    engine = create_engine('sqlite:///backloggd.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    logged_in_user = None

    while True:
            user_input = input("\nMenu Options:\nOption 1: Login\nOption 2: Create New User\nOption 3: Quit\nEnter: ")
            match(user_input):
                case "1":
                    print("You selected option 1: Login")
                    username = input("\nEnter your username: ")
                    password = input("Enter your password: ")
                    logged_in_user = user_login(username, password)
                    if logged_in_user:
                        main_menu(logged_in_user)
                case "2":
                    print("You selected option 2: Create New User")
                    add_user()
                case "3":
                    print("You selected option 3: Quit")
                    break
                case _:
                    print("Invalid option. Please try again.")

