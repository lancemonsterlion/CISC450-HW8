from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from alchemyBase import Base, ListEntry, User, Message, Game, FriendList, GameList, UserLibrary, Review


# Replace 'sqlite:///example.db' with your database URL
engine = create_engine('sqlite:///backloggd.db')
Session = sessionmaker(bind=engine)
session = Session()

def user_login(username, password):
    try:
        # Query the database for a user with the given username and password
        user = session.query(User).filter_by(user_name=username, password=password).one()
        print(f"\nWelcome, {user.user_name}! Login successful.")
        return user
    except NoResultFound:
        print("Invalid username or password. Please try again.")
        return None
    
def add_user():
    while True:
        # Collect input from the user
        user_name = input("\nEnter user name: ")
        
        # Check if the username already exists
        existing_user = session.query(User).filter_by(user_name=user_name).first()
        if existing_user:
            print("This username is already in use. Please choose a different one.")
            continue  # Prompt the user to try again
        
        email = input("Enter email: ")
        password = input("Enter password: ")
        
        # Create a new User instance
        new_user = User(
            user_name=user_name,
            email=email,
            password=password
        )
        
        # Add the new user to the session and commit
        session.add(new_user)
        session.commit()
        print("\nUser added successfully!")
        break  # Exit the loop after successful addition

def change_username(user_id):
    try:
        # Fetch the user by user_id
        new_username = input("\nEnter your new username: ")
        user = session.query(User).filter_by(user_id=user_id).one()
        user.user_name = new_username  # Update the username
        session.commit()  # Save changes
        print(f"Username successfully updated to '{new_username}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_user_library(user_id):
    try:
        # Query UserLibrary for all games belonging to the logged-in user
        user_library = (
            session.query(UserLibrary)
            .join(Game, UserLibrary.game_id == Game.game_id)
            .filter(UserLibrary.user_id == user_id)
            .all()
        )
        
        if not user_library:
            print("\nYour library is empty!")
            return []
        
        # Display user's library
        print("\nYour Game Library:")
        library = []
        for entry in user_library:
            game_details = {
                "game_id": entry.game.game_id,
                "title": entry.game.title,
                "platform": entry.game.platform,
                "user_score": entry.user_score
            }
            library.append(game_details)
            print(f"- {entry.game.title} (Platform: {entry.game.platform}, Your Score: {entry.user_score})")
        
        return library
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def change_password_plain(user_id):
    try:
        # Fetch the user by user_id
        current_password = input("Enter your current password: ")
        new_password = input("Enter your new password: ")
        user = session.query(User).filter_by(user_id=user_id).one()
        
        # Verify the current password
        if user.password != current_password:
            print("The current password is incorrect.")
            return
        
        # Update the password
        user.password = new_password
        session.commit()  # Save changes
        print("Password successfully updated.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_user_account(user_id):
    try:
        # Fetch the user by user_id
        user = session.query(User).filter_by(user_id=user_id).one()

        # Optionally delete associated data
        # Delete user's libraries
        session.query(UserLibrary).filter_by(user_id=user_id).delete()

        # Delete user's game lists
        session.query(GameList).filter_by(user_id=user_id).delete()

        # Delete user's reviews
        session.query(Review).filter_by(user_id=user_id).delete()

        # Delete user's messages
        session.query(Message).filter(
            (Message.sender_id == user_id) | (Message.recipient_id == user_id)
        ).delete()

        # Delete user's friend requests
        session.query(FriendList).filter(
            (FriendList.requestor_id == user_id) | (FriendList.recipient_id == user_id)
        ).delete()

        # Finally, delete the user
        session.delete(user)
        session.commit()

        print(f"\nUser with ID {user_id} and their associated data have been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")


def add_friend(requestor_id, recipient_user_name):
    try:
        # Fetch the recipient's user_id by their username
        recipient = session.query(User).filter_by(user_name=recipient_user_name).first()
        
        if not recipient:
            print(f"\nNo user found with the username '{recipient_user_name}'.")
            return
        
        recipient_id = recipient.user_id  # Get the recipient's user_id
        
        # Check if the requestor is trying to add themselves
        if requestor_id == recipient_id:
            print("\nYou cannot add yourself as a friend.")
            return
        
        # Check if the friendship already exists
        existing_friendship = session.query(FriendList).filter_by(
            requestor_id=requestor_id, recipient_id=recipient_id
        ).first()
        
        if existing_friendship:
            print("This user is already in your friends list or a request is pending.")
            return
        
        # Add the friend request
        new_friend_request = FriendList(
            requestor_id=requestor_id,
            recipient_id=recipient_id,
            accepted=False  # Initially, the friend request is not accepted
        )
        session.add(new_friend_request)
        session.commit()
        print(f"\nFriend request sent to {recipient_user_name} (ID: {recipient_id}).")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
def display_friends_list(user_id):
    try:
        # Query for accepted friendships where the user is the requestor or recipient
        friends = session.query(FriendList).filter(
            ((FriendList.requestor_id == user_id) | (FriendList.recipient_id == user_id)) &
            (FriendList.accepted == True)
        ).all()
        
        if not friends:
            print("\nYou have no friends in your list.")
            return []
        
        # Display friend IDs
        print("\nYour Friends List:")
        friends_list = []
        for friendship in friends:
            # Determine the friend ID (opposite of the logged-in user)
            friend_id = (
                friendship.recipient_id if friendship.requestor_id == user_id else friendship.requestor_id
            )
            # Optionally fetch friend's details
            friend = session.query(User).filter_by(user_id=friend_id).first()
            friend_name = friend.user_name if friend else f"Unknown (ID: {friend_id})"
            friends_list.append({"user_id": friend_id, "user_name": friend_name})
            print(f"- {friend_name} (ID: {friend_id})")
        
        return friends_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    
def check_and_accept_friend_requests(user_id):
    try:
        # Fetch all pending friend requests where the user is the recipient
        pending_requests = session.query(FriendList).filter_by(
            recipient_id=user_id, accepted=False
        ).all()
        
        if not pending_requests:
            print("\nYou have no pending friend requests.")
            return
        
        # Display the pending friend requests
        print("Pending Friend Requests:")
        for request in pending_requests:
            requestor = session.query(User).filter_by(user_id=request.requestor_id).first()
            print(f"- {requestor.user_name} (ID: {requestor.user_id})")
        
        # Ask user to accept a request
        recipient_confirmation = input("Enter the ID of the user you want to accept or 'exit' to cancel: ")
        
        if recipient_confirmation.lower() == 'exit':
            print("\nNo requests accepted.")
            return
        
        try:
            recipient_id_to_accept = int(recipient_confirmation)
        except ValueError:
            print("Invalid input.")
            return
        
        # Find the matching request and accept it
        request_to_accept = session.query(FriendList).filter_by(
            recipient_id=user_id, requestor_id=recipient_id_to_accept, accepted=False
        ).first()
        
        if not request_to_accept:
            print(f"No pending request from user ID {recipient_id_to_accept}.")
            return
        
        # Accept the friend request by updating the 'accepted' status
        request_to_accept.accepted = True
        session.commit()
        print(f"Friend request from user ID {recipient_id_to_accept} accepted.")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def send_message(sender_id, recipient_user_name):
    try:
        # Fetch the recipient's user_id by their username
        recipient = session.query(User).filter_by(user_name=recipient_user_name).first()
        
        if not recipient:
            print(f"No user found with the username '{recipient_user_name}'.")
            return
        
        recipient_id = recipient.user_id  # Get the recipient's user_id
        message_content = input("Enter your message to " + recipient_user_name + ": ")
        # Create a new message
        new_message = Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=message_content
        )
        
        # Add and commit the new message to the database
        session.add(new_message)
        session.commit()
        
        print(f"Message sent to {recipient_user_name} (ID: {recipient_id}).")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def view_messages(user_id):
    try:
        # Fetch all messages where the user is the sender or the recipient
        messages_sent = session.query(Message).filter_by(sender_id=user_id).all()
        messages_received = session.query(Message).filter_by(recipient_id=user_id).all()
        
        if not messages_sent and not messages_received:
            print("You have no messages.")
            return
        
        # Display Sent Messages
        if messages_sent:
            print("\nSent Messages:")
            for message in messages_sent:
                recipient = session.query(User).filter_by(user_id=message.recipient_id).first()
                print(f"To: {recipient.user_name} (ID: {message.recipient_id})")
                print(f"Message: {message.content}\n")
        
        # Display Received Messages
        if messages_received:
            print("\nReceived Messages:")
            for message in messages_received:
                sender = session.query(User).filter_by(user_id=message.sender_id).first()
                print(f"From: {sender.user_name} (ID: {message.sender_id})")
                print(f"Message: {message.content}\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")



def main_menu(logged_in_user):
    if logged_in_user:
        while True:
            user_input = input("\nMenu Options:\nOption 1: View Library\nOption 2: Edit Profile\nOption 3: Add Game to Library"
                            "\nOption 4: Add a friend\nOption 5: Display Friend List\nOption 6: Check for pending friend requests"
                            "\nOption 7: Message Options"
                            "\nOption 8: Log Out\nEnter: ")
            match(user_input):
                case "1":
                    print("You selected option 1: View Profile")
                    generate_user_library(logged_in_user.user_id)
                case "2":
                    print("You selected option 2: Edit Profile")
                    while True:
                        user_input = input("\nEdit Profile Options:\nOption 1: Change Username\nOption 2: Change Password\nOption 3: Delete Account\nOption 4: Back to Previous Menu\nEnter: ")
                        match(user_input):
                            case "1":
                                change_username(logged_in_user.user_id)
                            case "2":
                                change_password_plain(logged_in_user.user_id)
                            case "3":
                                delete_user_account(logged_in_user.user_id)
                                return
                            case "4":
                                break
                            case _:
                                print("Invalid option. Please try again.")
                case "3":
                    print("You selected option 3: Add game to Library")
                    add_game_to_library(logged_in_user.user_id)
                case "4":
                    print("You selected option 4: Add friend to friends list")
                    friend_name = input("Enter your friends username to add them to your friends list: ")
                    add_friend(logged_in_user.user_id, friend_name)
                case "5":
                    print("You selected option 5: Display friends list")
                    display_friends_list(logged_in_user.user_id)
                case "6":
                    print("You selected option 6: Check for pending friend requests")
                    check_and_accept_friend_requests(logged_in_user.user_id)
                case "7":
                    print("You selected option 7: Message Options")
                    while True:
                        user_input = input("\nMenu Options:\nOption 1: View Messages\nOption 2: Send Message\nOption 3: Previous Menu\nEnter: ")
                        match(user_input):
                            case "1":
                                view_messages(logged_in_user.user_id)
                            case "2":
                                recipient = input("Enter the username of the recipient: ")
                                send_message(logged_in_user.user_id, recipient)
                            case "3":
                                break
                            case _:
                                print("Invalid option. Please try again.")
                case "8":
                    print("\nYou selected option 7: Log Out\n")
                    break
                case _:
                    print("Invalid option. Please try again.")
    else:
        print("Error: Not logged in")
        return

def add_game_to_library(user, game_name, user_score=None):
    # Step 1: Search for the game by its name
    game = session.query(Game).filter(Game.game_name.ilike(game_name)).first()  # case-insensitive search
    
    if game:
        # Step 2: Check if the user already has this game in their library
        existing_entry = session.query(UserLibrary).filter(UserLibrary.user_id == user.user_id, 
                                                            UserLibrary.game_id == game.game_id).first()
        
        if existing_entry:
            print(f"You already have {game_name} in your library!")
        else:
            # Step 3: Add the game to the user's library
            new_entry = UserLibrary(user_id=user.user_id, game_id=game.game_id, user_score=user_score)
            session.add(new_entry)
            session.commit()
            print(f"Successfully added {game_name} to your library!")
    else:
        print(f"Game '{game_name}' not found!")
        
        
def add_game_to_library(user_id):
    # Step 1: Retrieve the user from the database using the username
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        print("User not found. Please check the username and try again.")
        return
    
    # Step 2: Prompt the user for the game name
    game_name = input("Enter the name of the game you want to add: ")
    
    # Search for the game by its name
    game = session.query(Game).filter(Game.title.ilike(game_name)).first()  # case-insensitive search
    
    if game:
        # Step 3: Check if the user already has this game in their library
        existing_entry = session.query(UserLibrary).filter(UserLibrary.user_id == user.user_id, 
                                                            UserLibrary.game_id == game.game_id).first()
        
        if existing_entry:
            print(f"\nYou already have {game_name} in your library!")
        else:
            # Step 4: Optionally prompt the user for a score
            user_score = input("Enter your score for the game (optional, press Enter to skip): ")
            user_score = float(user_score) if user_score.strip() else None
            
            # Add the game to the user's library
            new_entry = UserLibrary(user_id=user.user_id, game_id=game.game_id, user_score=user_score)
            session.add(new_entry)
            session.commit()
            print(f"\nSuccessfully added {game_name} to your library!")
    else:
        print(f"\nGame '{game_name}' not found!")
