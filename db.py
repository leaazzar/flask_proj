#!/usr/bin/python
import sqlite3
def connect_to_db():
    conn = sqlite3.connect('Users.db')
    return conn
def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("User table created successfully")
    except Exception as e:
        print("User table creation failed:", e)
    finally:
        conn.close()

def insert_user(user):
    inserted_user = {}
    try:
        print("Inserting user:", user)  # Log the user being inserted
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)", 
                    (user['name'], user['email'], user['phone'], user['address'], user['country']))
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        print("Error inserting user:", e)  # Log any error during insertion
        conn.rollback()
    finally:
        conn.close()
    return inserted_user

def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")  # Query to fetch all users
        rows = cur.fetchall()
        print(f"Fetched {len(rows)} users")  # Debugging statement
        # Convert each row to a dictionary and append it to the users list
        for row in rows:
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"]
            }
            users.append(user)
    except Exception as e:
        print("Error fetching users:", e)  # Log any errors
        users = []
    finally:
        conn.close()
    return users

def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?",(user_id,))
        row = cur.fetchone()
        # convert row object to dictionary
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["address"] = row["address"]
        user["country"] = row["country"]
    except:
        user = {}
    return user 
def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?,phone=?, address = ?, country = ? WHERE user_id=?",(user["name"], user["email"], user["phone"],user["address"], user["country"],
        user["user_id"],))
        conn.commit()
        #return the user
        updated_user = get_user_by_id(user["user_id"])
    except:
        conn.rollback()
        updated_user = {}
    finally:
        conn.close()
    return updated_user
def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from users WHERE user_id = ?",(user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message
