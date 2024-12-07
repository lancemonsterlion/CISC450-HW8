--
-- File generated with SQLiteStudio v3.4.4 on Wed Dec 4 10:37:20 2024
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: friend_list
CREATE TABLE IF NOT EXISTS friend_list (
	requestor_id INTEGER NOT NULL, 
	recipient_id INTEGER NOT NULL, 
	accepted BOOLEAN, 
	PRIMARY KEY (requestor_id, recipient_id), 
	FOREIGN KEY(requestor_id) REFERENCES "Users" (user_id), 
	FOREIGN KEY(recipient_id) REFERENCES "Users" (user_id)
);

-- Table: Game Lists
CREATE TABLE IF NOT EXISTS "Game Lists" (
	list_id INTEGER NOT NULL, 
	user_id INTEGER, 
	list_name TEXT, 
	list_type TEXT, 
	likes INTEGER, 
	PRIMARY KEY (list_id), 
	FOREIGN KEY(list_id) REFERENCES "List Entries" (list_id), 
	FOREIGN KEY(user_id) REFERENCES "Users" (user_id)
);

-- Table: Games
CREATE TABLE IF NOT EXISTS "Games" (
	game_id INTEGER NOT NULL, 
	title TEXT, 
	platform TEXT, 
	metacritic_score INTEGER, 
	genre TEXT, 
	PRIMARY KEY (game_id)
);
INSERT INTO Games (game_id, title, platform, metacritic_score, genre) VALUES (1, 'The Witcher 3: Wild Hunt', 'PC', 93, 'RPG');
INSERT INTO Games (game_id, title, platform, metacritic_score, genre) VALUES (2, 'Red Dead Redemption 2', 'PlayStation 4', 97, 'Action-Adventure');
INSERT INTO Games (game_id, title, platform, metacritic_score, genre) VALUES (3, 'Celeste', 'Nintendo Switch', 92, 'Platformer');
INSERT INTO Games (game_id, title, platform, metacritic_score, genre) VALUES (4, 'Dark Souls III', 'Xbox One', 89, 'RPG');
INSERT INTO Games (game_id, title, platform, metacritic_score, genre) VALUES (5, 'Hollow Knight', 'PC', 90, 'Metroidvania');

-- Table: List Entries
CREATE TABLE IF NOT EXISTS "List Entries" (
	list_id INTEGER NOT NULL, 
	game_id INTEGER, 
	rating INTEGER, 
	comments TEXT, 
	PRIMARY KEY (list_id), 
	FOREIGN KEY(game_id) REFERENCES "Games" (game_id)
);

-- Table: Messages
CREATE TABLE IF NOT EXISTS "Messages" (
	message_id INTEGER NOT NULL, 
	sender_id INTEGER, 
	recipient_id INTEGER, 
	content TEXT, 
	PRIMARY KEY (message_id), 
	FOREIGN KEY(sender_id) REFERENCES "Users" (user_id), 
	FOREIGN KEY(recipient_id) REFERENCES "Users" (user_id)
);

-- Table: Reviews
CREATE TABLE IF NOT EXISTS "Reviews" (
	review_id INTEGER NOT NULL, 
	game_id INTEGER, 
	user_id INTEGER, 
	review_body TEXT, 
	review_score INTEGER, 
	PRIMARY KEY (review_id), 
	FOREIGN KEY(game_id) REFERENCES "Games" (game_id), 
	FOREIGN KEY(user_id) REFERENCES "Users" (user_id)
);

-- Table: User Library
CREATE TABLE IF NOT EXISTS "User Library" (
	user_id INTEGER NOT NULL, 
	game_id INTEGER NOT NULL, 
	user_score INTEGER, 
	PRIMARY KEY (user_id, game_id), 
	FOREIGN KEY(user_id) REFERENCES "Users" (user_id), 
	FOREIGN KEY(game_id) REFERENCES "Games" (game_id)
);

-- Table: Users
CREATE TABLE IF NOT EXISTS "Users" (
	user_id INTEGER NOT NULL, 
	user_name TEXT, 
	email TEXT, 
	password TEXT, 
	PRIMARY KEY (user_id)
);
INSERT INTO Users (user_id, user_name, email, password) VALUES (1, 'samlargaespada', 'sam.largaespada@stthomas.edu', 'password1');
INSERT INTO Users (user_id, user_name, email, password) VALUES (2, 'antonlacson', 'anton.lacson@stthomas.edu', 'password2');
INSERT INTO Users (user_id, user_name, email, password) VALUES (3, 'lancemunsterteiger', 'lance.munsterteiger@stthomas.edu', 'password3');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
