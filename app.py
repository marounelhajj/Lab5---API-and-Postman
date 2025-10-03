#!/usr/bin/env python3
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

def connect_to_db():
    conn = sqlite3.connect("database.db")
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
            """
        )
        conn.commit()
        print("User table ready")
    except Exception as e:
        print("User table creation failed:", e)
    finally:
        conn.close()

def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            (
                user["name"],
                user["email"],
                user["phone"],
                user["address"],
                user["country"],
            ),
        )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        conn.rollback()
        print("Insert failed:", e)
    finally:
        conn.close()
    return inserted_user

def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for i in rows:
            user = {
                "user_id": i["user_id"],
                "name": i["name"],
                "email": i["email"],
                "phone": i["phone"],
                "address": i["address"],
                "country": i["country"],
            }
            users.append(user)
    except Exception as e:
        print("Get users failed:", e)
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
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"],
            }
    except Exception as e:
        print("Get user by id failed:", e)
        user = {}
    finally:
        conn.close()
    return user

def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE users
               SET name = ?, email = ?, phone = ?, address = ?, country = ?
             WHERE user_id = ?
            """,
            (
                user["name"],
                user["email"],
                user["phone"],
                user["address"],
                user["country"],
                user["user_id"],
            ),
        )
        conn.commit()
        updated_user = get_user_by_id(user["user_id"])
    except Exception as e:
        conn.rollback()
        print("Update failed:", e)
    finally:
        conn.close()
    return updated_user

def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        conn.rollback()
        message["status"] = f"Cannot delete user: {e}"
    finally:
        conn.close()
    return message

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/api/users", methods=["GET"])
def api_get_users():
    return jsonify(get_users())

@app.route("/api/users/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))

@app.route("/api/users/add", methods=["POST"])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route("/api/users/update", methods=["PUT"])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

@app.route("/api/users/delete/<int:user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))

if __name__ == "__main__":
    create_db_table()   
    app.run()           
