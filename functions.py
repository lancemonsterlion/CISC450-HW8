# Function to send a message
def send_message(sender, recipient_username):
    # Ask the user to input the message
    message_content = input("Enter your message: ")

    # Check if the recipient exists in the database
    recipient = session.query(User).filter(User.user_name == recipient_username).first()

    if recipient:
        # Create a new message object
        new_message = Message(sender_id=sender.id, recipient_id=recipient.id, message=message_content)

        # Add the message to the session and commit to the database
        session.add(new_message)
        session.commit()

        print(f"Message sent to {recipient.user_name}.")
    else:
        print("Recipient username not found.")
#  add games to library
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
      
#  add games to list
def add_game_to_user_list(user, game_name):
    # Step 1: Search for the game by name
    game_id = search_game_by_name(game_name)
    if not game_id:
        return  # If the game wasn't found, exit the function
    
    # Step 2: Ask the user for the name of the list to add the game to
    list_name = input("Enter the name of the list you want to add this game to: ")
    
    # Step 3: Check if the user already has a list with that name
    existing_list = session.query(GameList).filter(GameList.user_id == user.user_id, GameList.list_name == list_name).first()
    
    if existing_list:
        # If the list already exists, add the game to the list
        print(f"Adding {game_name} to the list '{list_name}'")
        
        # Create the new ListEntry
        new_entry = ListEntry(game_id=game_id, list_id=existing_list.list_id)
        session.add(new_entry)
        session.commit()
        print(f"{game_name} has been added to the list '{list_name}'.")
    else:
        # If no such list exists, create a new one
        print(f"Creating a new list '{list_name}' and adding {game_name}.")
        
        # Create a new game list
        new_list = GameList(user_id=user.user_id, list_name=list_name, list_type="custom", likes=0)
        session.add(new_list)
        session.commit()

        # Create the new ListEntry to add the game to this new list
        new_entry = ListEntry(game_id=game_id, list_id=new_list.list_id)
        session.add(new_entry)
        session.commit()
        print(f"{game_name} has been added to the newly created list '{list_name}'.")

#  create reviews
def create_review(username):
    # Step 1: Search for the user by username
    user = session.query(User).filter(User.user_name == username).first()
    
    if not user:
        print(f"User '{username}' not found.")
        return
    
    # Step 2: Search for the game by its title
    game_title = input("Enter the title of the game you want to review: ")
    game = session.query(Game).filter(Game.title == game_title).first()
    
    if not game:
        print(f"Game '{game_title}' not found.")
        return
    
    # Step 3: Get the review score and review body from the user
    try:
        review_score = int(input("Enter your review score (1-10): "))
        if review_score < 1 or review_score > 10:
            print("Please enter a score between 1 and 10.")
            return
    except ValueError:
        print("Invalid score. Please enter a number between 1 and 10.")
        return
    
    review_body = input("Enter your review: ")

    # Step 4: Create a new Review object
    new_review = Review(
        user_id=user.user_id,
        game_id=game.game_id,
        review_score=review_score,
        review_body=review_body
    )

    # Step 5: Add the review to the session and commit it to the database
    session.add(new_review)
    session.commit()

    print(f"Review for '{game_title}' successfully submitted!")


#  view messages
def send_message(sender_id, recipient_id, content):
    """
    Function to send a message from one user to another.
    
    Args:
        sender_id (int): The ID of the user sending the message.
        recipient_id (int): The ID of the user receiving the message.
        content (str): The content of the message.
    
    Returns:
        None
    """
    # Check if the users are friends (Optional, requires a friend relationship)
    friend_relationship = session.query(FriendList).filter(
        FriendList.requestor_id == sender_id,
        FriendList.recipient_id == recipient_id,
        FriendList.accepted == True
    ).first()
    
    if friend_relationship:
        # Create the message
        new_message = Message(sender_id=sender_id, recipient_id=recipient_id, content=content)
        session.add(new_message)
        session.commit()
        print("Message sent successfully!")
    else:
        print("You can only send messages to your friends.")

# Example usage
send_message(sender_id=1, recipient_id=2, content="Hey, how are you?")
#  view friends
#  view reviews
# Function to view reviews by searching username
def view_reviews_by_username(username):
    # Search for the user by username
    user = session.query(User).filter(User.user_name == username).first()
    
    if not user:
        print(f"User '{username}' not found.")
        return
    
    # Fetch all reviews written by the user
    reviews = session.query(Review).filter(Review.user_id == user.user_id).all()
    
    if reviews:
        print(f"Reviews by {username}:")
        for review in reviews:
            game_title = session.query(Game).filter(Game.game_id == review.game_id).first().title
            print(f"Game: {game_title}")
            print(f"Review Score: {review.review_score}")
            print(f"Review: {review.review_body}\n")
    else:
        print(f"{username} has not written any reviews.")
#  view list
# Function to view lists and the games in them by searching username
def view_lists_by_username(username):
    # Search for the user by username
    user = session.query(User).filter(User.user_name == username).first()
    
    if not user:
        print(f"User '{username}' not found.")
        return
    
    # Fetch all game lists created by the user, including the associated ListEntry and Game information
    game_lists = session.query(GameList).filter(GameList.user_id == user.user_id).all()
    
    if game_lists:
        print(f"Game Lists created by {username}:")

        for game_list in game_lists:
            # Display list details
            print(f"\nList Name: {game_list.list_name}")
            print(f"List Type: {game_list.list_type}")
            print(f"Likes: {game_list.likes}")
            
            # Get the games in this list by joining ListEntry and Game
            games_in_list = session.query(Game).join(ListEntry).filter(ListEntry.list_id == game_list.list_id).all()
            
            if games_in_list:
                print("Games in this list:")
                for game in games_in_list:
                    print(f"- {game.title}")
            else:
                print("No games in this list.")
            
    else:
        print(f"{username} has not created any game lists.")

# search games
def search_game_by_name(game_name):
    # Search for the game by name (case-insensitive search)
    game = session.query(Game).filter(Game.game_name.ilike(game_name)).first()  # ilike for case-insensitive search
    
    if game:
        return game.game_id  # Return the game_id of the found game
    else:
        print(f"Game '{game_name}' not found.")
        return None
