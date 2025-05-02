import DatabaseConnector

#Creates a users table in the database if it doesn't exist
def create_users_table():
    query = """
     CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
    """
    DatabaseConnector.execute_query(DatabaseConnector.connection, query)


def create_user(username):
    create_users_table()
    query = "INSERT INTO users (username) VALUES (%s)"
    params = (username,)  #Adding parameters this way makes sure that querys are safe
    DatabaseConnector.execute_query(DatabaseConnector.connection, query, params)
    create_savefile()

def login_user(username):
    query = "SELECT id, username FROM users WHERE username = %s"
    params = (username,)  #Adding parameters this way makes sure that querys are safe
    DatabaseConnector.execute_query(DatabaseConnector.connection, query, params)


def create_savefile():
    query = """
    CREATE TABLE IF NOT EXISTS game_progress(
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    game_state JSON NOT NULL,
    game_started BOOLEAN DEFAULT FALSE,
    game_score INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    ); """
    DatabaseConnector.execute_query(DatabaseConnector.connection, query)











