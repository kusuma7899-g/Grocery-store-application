def get_user(connection, username):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT username, hashed_password FROM users WHERE username = %s",
        (username,)
    )
    row = cursor.fetchone()
    cursor.close()
    if row:
        return {"username": row[0], "hashed_password": row[1]}
    return None

def insert_user(connection, username, hashed_password):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
        (username, hashed_password)
    )
    connection.commit()
    cursor.close()