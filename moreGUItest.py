import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from alchemyBase import Base, ListEntry, User, Message, Game, FriendList, GameList, UserLibrary, Review


# Database setup
engine = create_engine('sqlite:///backloggd.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create the main application class
class App:
    def __init__(self, root):
        self.root = root
        self.logged_in_user = None
        
        self.root.geometry("350x450")
        # Set up the initial login screen
        self.create_login_screen()
    
    def create_login_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack(pady=10)
        
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        
        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack(pady=10)
        
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=20)
        
        self.create_user_button = tk.Button(self.root, text="Create New User", command=self.create_new_user)
        self.create_user_button.pack(pady=10)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        self.logged_in_user = user_login(username, password)
        if self.logged_in_user:
            self.create_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
    
    def create_new_user(self):
        self.create_user_screen()
    
    def create_user_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.new_username_label = tk.Label(self.root, text="New Username:")
        self.new_username_label.pack(pady=10)
        
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack(pady=5)
        
        self.new_email_label = tk.Label(self.root, text="Email:")
        self.new_email_label.pack(pady=10)
        
        self.new_email_entry = tk.Entry(self.root)
        self.new_email_entry.pack(pady=5)
        
        self.new_password_label = tk.Label(self.root, text="Password:")
        self.new_password_label.pack(pady=10)
        
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=5)
        
        self.add_user_button = tk.Button(self.root, text="Add User", command=self.add_user)
        self.add_user_button.pack(pady=20)
    
    def add_user(self):
        username = self.new_username_entry.get()
        email = self.new_email_entry.get()
        password = self.new_password_entry.get()
        
        # Create a new user in the database
        add_user_to_db(username, email, password)
        
        messagebox.showinfo("User Created", "New user created successfully!")
        self.create_login_screen()

    def create_main_menu(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main menu with options
        self.menu_label = tk.Label(self.root, text=f"Welcome, {self.logged_in_user.user_name}")
        self.menu_label.pack(pady=10)
        
        self.view_library_button = tk.Button(self.root, text="View Library", command=self.view_library)
        self.view_library_button.pack(pady=10)
        
        self.edit_profile_button = tk.Button(self.root, text="Edit Profile", command=self.edit_profile)
        self.edit_profile_button.pack(pady=10)
        
        self.add_game_button = tk.Button(self.root, text="Add Game to Library", command=self.add_game_to_library)
        self.add_game_button.pack(pady=10)
        
        self.view_friends_button = tk.Button(self.root, text="View Friends List", command=self.view_friends_list)
        self.view_friends_button.pack(pady=10)
        
        self.add_friend_button = tk.Button(self.root, text="Add Friend", command=self.add_friend)
        self.add_friend_button.pack(pady=10)
        
        self.check_pending_button = tk.Button(self.root, text="Check Pending Friend Requests", command=self.check_pending_requests)
        self.check_pending_button.pack(pady=10)
        
        self.view_messages_button = tk.Button(self.root, text="View Messages", command=self.view_messages)
        self.view_messages_button.pack(pady=10)
        
        
        
        self.logout_button = tk.Button(self.root, text="Log Out", command=self.logout)
        self.logout_button.pack(pady=20)

    def view_library(self):
        # Generate and display the user's game library
        library = generate_user_library(self.logged_in_user.user_id)
        library_window = tk.Toplevel(self.root)
        library_window.title("Your Game Library")
        
        for game in library:
            game_label = tk.Label(library_window, text=f"{game['title']} (Platform: {game['platform']}, Score: {game['user_score']})")
            game_label.pack(pady=5)
        
    def edit_profile(self):
        # Allow the user to change their profile settings
        self.create_edit_profile_screen()
    
    def create_edit_profile_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.change_username_button = tk.Button(self.root, text="Change Username", command=self.change_username)
        self.change_username_button.pack(pady=10)
        
        self.change_password_button = tk.Button(self.root, text="Change Password", command=self.change_password)
        self.change_password_button.pack(pady=10)
        
        self.delete_account_button = tk.Button(self.root, text="Delete Account", command=self.delete_account)
        self.delete_account_button.pack(pady=10)
        
        self.back_button = tk.Button(self.root, text="Back to Menu", command=self.create_main_menu)
        self.back_button.pack(pady=20)
    
    def change_username(self):
        new_username = tk.simpledialog.askstring("Change Username", "Enter your new username:")
        if new_username:
            change_username(self.logged_in_user.user_id, new_username)
            messagebox.showinfo("Success", "Username updated successfully.")
    
    def change_password(self):
        new_password = tk.simpledialog.askstring("Change Password", "Enter your new password:", show="*")
        if new_password:
            change_password_plain(self.logged_in_user.user_id, new_password)
            messagebox.showinfo("Success", "Password updated successfully.")
    
    def delete_account(self):
        confirm = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account?")
        if confirm:
            delete_user_account(self.logged_in_user.user_id)
            messagebox.showinfo("Success", "Account deleted successfully.")
            self.logged_in_user = None
            self.create_login_screen()

    def add_game_to_library(self):
        game_name = tk.simpledialog.askstring("Add Game", "Enter the name of the game:")
        
        
        if game_name:
            # Search for the game by its name
            game = session.query(Game).filter(Game.title.ilike(game_name)).first()  # case-insensitive search
            
            if game:
                # If the game exists, check if it is already in the user's library
                existing_entry = session.query(UserLibrary).filter(
                    UserLibrary.user_id == self.logged_in_user.user_id,
                    UserLibrary.game_id == game.game_id
                ).first()

                if existing_entry:
                    messagebox.showinfo("Game Already in Library", f"You already have {game_name} in your library.")
                else:
                    # If not in the library, add the game
                    score = tk.simpledialog.askstring("Add Score", "Enter your score for the game:")
                    user_score = float(score) if score.strip() else None
                    
                    # Add the game to the user's library
                    new_entry = UserLibrary(user_id=self.logged_in_user.user_id, game_id=game.game_id, user_score=user_score)
                    session.add(new_entry)
                    session.commit()
                    messagebox.showinfo("Game Added", f"Successfully added {game_name} to your library!")
            else:
                # If the game does not exist in the Games table
                messagebox.showerror("Game Not Found", f"The game '{game_name}' was not found in the database.")

    def view_friends_list(self):
        try:
            # Query for friends where 'accepted' is True (both requestor and recipient)
            friends = session.query(FriendList).filter(
                FriendList.accepted == True,
                (FriendList.requestor_id == self.logged_in_user.user_id) | 
                (FriendList.recipient_id == self.logged_in_user.user_id)
            ).all()
            
            if friends:
                # Create a new window for the friends list
                friends_window = tk.Toplevel(self.root)
                friends_window.title("Your Friends List")
                
                for friend in friends:
                    # Determine who is the friend (requestor or recipient)
                    friend_id = friend.recipient_id if friend.requestor_id == self.logged_in_user.user_id else friend.requestor_id
                    friend_user = session.query(User).filter_by(user_id=friend_id).first()
                    
                    # Create a frame for the friend row (name and remove button in the same row)
                    friend_frame = tk.Frame(friends_window)
                    friend_frame.pack(pady=5, fill="x")  # fill="x" makes the frame take the full width
                    
                    # Label displaying the friend's name
                    friend_label = tk.Label(friend_frame, text=friend_user.user_name, width=30, anchor="w")
                    friend_label.pack(side="left", padx=10)  # Pack to the left
                    
                    # Button to remove the friend
                    remove_button = tk.Button(friend_frame, text="Remove Friend", command=lambda friend=friend: self.remove_friend(friend, friends_window))
                    remove_button.pack(side="right")  # Pack to the right

            else:
                messagebox.showinfo("No Friends", "You have no friends yet.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching your friends list: {e}")
    
    def remove_friend(self, friend, friends_window):
        # Remove the friend from the FriendList table
        try:
            # Delete the friend entry from FriendList table
            session.delete(friend)
            session.commit()
            
            # Close the friends window
            friends_window.destroy()

            # Recreate the main menu with updated list
            messagebox.showinfo("Success", "Friend removed successfully.")
            self.view_friends_list()  # Refresh friends list window
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while removing the friend: {e}")

    def add_friend(self):
        friend_username = tk.simpledialog.askstring("Add Friend", "Enter the username of the friend:")
        if friend_username:
            add_friend(self.logged_in_user.user_id, friend_username)
            messagebox.showinfo("Success", f"Friend request sent to {friend_username}.")

    def check_pending_requests(self):
        # Query for pending friend requests (requests where 'accepted' is False)
        try:
            pending_requests = session.query(FriendList).filter(FriendList.accepted == False, 
                                                                FriendList.recipient_id == self.logged_in_user.user_id).all()
            
            if pending_requests:
                # Create a new window for pending requests
                pending_window = tk.Toplevel(self.root)
                pending_window.title("Pending Friend Requests")
                
                for req in pending_requests:
                    requestor = session.query(User).filter_by(user_id=req.requestor_id).first()
                    
                    request_label = tk.Label(pending_window, text=f"Request from {requestor.user_name}")
                    request_label.pack(pady=5)
                    
                    accept_button = tk.Button(pending_window, text="Accept", 
                                              command=lambda req=req: self.accept_friend_request(req, pending_window))
                    accept_button.pack(pady=5)
                
            else:
                messagebox.showinfo("Pending Friend Requests", "No pending friend requests.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def accept_friend_request(self, request, pending_window):
        try:
            # Update the 'accepted' field to True for the friend request
            request.accepted = True
            session.commit()
            
            # Notify the user that the request was accepted
            messagebox.showinfo("Friend Request Accepted", "You have accepted the friend request.")
            
            # Close the pending requests window
            pending_window.destroy()
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while accepting the request: {e}")


    def view_messages(self):
        messages = generate_user_messages(self.logged_in_user.user_id)
        library_window = tk.Toplevel(self.root)
        library_window.title("Your Messages")
        for message in messages:
            message_label = tk.Label(library_window, text=f"Recipient: {message['recipient']}\nSender: {message['sender']}\nMessage: {message['content']}")
            message_label.pack(pady=5)
    
    def logout(self):
        self.logged_in_user = None
        self.create_login_screen()


def user_login(username, password):
    try:
        user = session.query(User).filter_by(user_name=username, password=password).one()
        return user
    except NoResultFound:
        return None

def add_user_to_db(username, email, password):
    new_user = User(user_name=username, email=email, password=password)
    session.add(new_user)
    session.commit()

def add_game_to_library(user_id, game_name, user_score):
    # Step 1: Retrieve the user from the database using the username
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        print("User not found. Please check the username and try again.")
        return

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
            # user_score = input("Enter your score for the game (optional, press Enter to skip): ")
            user_score = float(user_score) if user_score.strip() else None
            
            # Add the game to the user's library
            new_entry = UserLibrary(user_id=user.user_id, game_id=game.game_id, user_score=user_score)
            session.add(new_entry)
            session.commit()
            print(f"\nSuccessfully added {game_name} to your library!")
    else:
        print(f"\nGame '{game_name}' not found!")

def generate_user_library(user_id):
    user_library = session.query(UserLibrary).join(Game, UserLibrary.game_id == Game.game_id).filter(UserLibrary.user_id == user_id).all()
    library = []
    for entry in user_library:
        game_details = {
            "game_id": entry.game.game_id,
            "title": entry.game.title,
            "platform": entry.game.platform,
            "user_score": entry.user_score
        }
        library.append(game_details)
    return library

def change_username(user_id, new_username):
    user = session.query(User).filter_by(user_id=user_id).one()
    user.user_name = new_username
    session.commit()

def change_password_plain(user_id, new_password):
    user = session.query(User).filter_by(user_id=user_id).one()
    user.password = new_password
    session.commit()

def delete_user_account(user_id):
    user = session.query(User).filter_by(user_id=user_id).one()
    session.delete(user)
    session.commit()

def add_friend(requestor_id, recipient_user_name):
    recipient = session.query(User).filter_by(user_name=recipient_user_name).first()
    if recipient:
        recipient_id = recipient.user_id
        new_friend_request = FriendList(requestor_id=requestor_id, recipient_id=recipient_id, accepted=False)
        session.add(new_friend_request)
        session.commit()

def generate_user_messages(user_id):
    # Query to fetch messages for the given user
    user_messages = session.query(Message).filter((Message.recipient_id == user_id) | (Message.sender_id == user_id)).all()
    
    messages = []
    for message in user_messages:
        # Create a dictionary for each message
        message_details = {
            "recipient": message.recipient.user_name,
            "sender": message.sender.user_name,
            "content": message.content
 # Assuming there is a timestamp for when the message was sent
        }
        messages.append(message_details)
    print(messages[0])
    
    return messages


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
