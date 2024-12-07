import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemyBase import User, Base  # Import the User class from the module you defined it in

# Create an engine and session
engine = create_engine('sqlite:///backloggd.db', echo=True)  # Replace with your actual database URI
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
logging.disable(logging.CRITICAL)
logged_in_user = None

# Function to add a new user
def add_user():
    # Collect input from the user
    user_name = input("Enter user name: ")
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

    print("User added successfully!")

def menu(user):
    while True:
        user_input = input("Menu Options:\nOption 1: View Library\nOption 2: Edit Profile\nOption 3: Delete Account\nOption 4: Log Out\nEnter: ")
        match(user_input):
            case "1":
                print("You selected option 1: View Profile")
                generate_user_library(user.user_id)
            case "2":
                print("You selected option 2: Edit Profile")
            case "3":
                print("You selected option 3: Delete Account")
            case "4":
                print("You selected option 4: Log Out")
                break
            case _:
                print("Invalid option. Please try again.")

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
            print("Your library is empty!")
            return []
        
        # Display user's library
        print("Your Game Library:")
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

def userInput(lowerBound, upperBound, text):
    inputField = input(text)
    while(int(inputField) < lowerBound or int(inputField) > upperBound):
        inputField = input("that is not a valid input. Please enter a value from "+str(lowerBound)+" to "+str(upperBound)+".\n")
    return inputField

def authenticate_user(username, password):

    user = session.query(User).filter(User.user_name == username, User.password == password).first()
    if user:
        return user
    else:
        print("Invalid username or password.")
        username = input("Username:\n")
        password = input("Password:\n")
        authenticate_user(username, password)
        return False

def homepage ():
    #runs when user starts script
    print("Welcome to Backloggd!\nEnter [1] to sign in or \nEnter [2] to create a new user or\nEnter [3] to quit.\n")
    response = userInput(1,3,"\n")
    match response:
        case "1": 
            username = input("Username:\n")
            password = input("Password:\n")
            logged_in_user = authenticate_user(username, password)
            print("Login Successful!")
            menu(logged_in_user)
        case "2": 
            add_user()
        case "3": 
            exit()



# Run the function
if __name__ == '__main__':
    
    homepage()
    # add_user()

    # Close the session
    session.close()