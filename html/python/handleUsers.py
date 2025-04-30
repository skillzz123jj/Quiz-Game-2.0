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












