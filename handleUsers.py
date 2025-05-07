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

    query = "INSERT INTO users (username) VALUE (%s)"
    params = (username,)
    try:
        DatabaseConnector.execute_query(DatabaseConnector.connection, query, params)
        print(f"User '{username}' inserted.")
    except Exception as e:
        print(f"Error inserting user: {e}")
        return

    query = "SELECT user_id FROM users WHERE username = %s"
    result = DatabaseConnector.fetch_one(DatabaseConnector.connection, query, params)
    print(f"Fetch result: {result}")

    if result:
        user_id = result[0]
        create_savefile(user_id)
    else:
        print("No user_id found, skipping savefile.")


def user_exists(username):
    query = "SELECT user_id FROM users WHERE username = %s"
    params = (username,)  #Adding parameters this way makes sure that querys are safe
    result = DatabaseConnector.fetch_one(DatabaseConnector.connection, query, params)
    return result is not None


def create_savefile(user_id):
    try:
        query = """
        CREATE TABLE IF NOT EXISTS game_progress(
            user_id INT PRIMARY KEY,
            game_state JSON NOT NULL,
            game_started BOOLEAN DEFAULT FALSE,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        );
        """
        DatabaseConnector.execute_query(DatabaseConnector.connection, query)

        query = """
        INSERT INTO game_progress(user_id, game_state, game_started)
        VALUES(%s, '{"lives": 3, "score": 0, "countries": []}', TRUE);
        """
        params = (user_id,)
        DatabaseConnector.execute_query(DatabaseConnector.connection, query, params)
    except Exception as e:
        print(f"Error creating savefile: {e}")















