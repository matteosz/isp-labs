#!/usr/bin/env python3

import populate
from flask import Flask
from flask import request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw5_ex2"

# This method returns a list of messages in a json format such as
# [
# { "name": <name>, "message": <message> },
# { "name": <name>, "message": <message> },
# ...
# ]
# If this is a POST request and there is a parameter "name" given, then only
# messages of the given name should be returned.
# If the POST parameter is invalid, then the response code must be 500.


@app.route("/messages", methods=["GET", "POST"])
def messages():
    with db.cursor() as cursor:
        
        try:
            json = []

            if request.method == 'GET':

                query = "SELECT name, message FROM messages"
                cursor.execute(query)

            elif request.method == 'POST':
                
                name = request.form.get("name", None)

                if name is None:
                    return "No name provided", 500

                # Prepared statement, the content of the query cannot be changed
                query = "SELECT name, message FROM messages WHERE name LIKE %s"
                cursor.execute(query, name)

            for name, message in cursor.fetchall():
                json.append({"name":name, "message":message})

        except pymysql.err.ProgrammingError:
            return "Malicious attempt revelead", 500

        return jsonify(json), 200


# This method returns the list of users in a json format such as
# { "users": [ <user1>, <user2>, ... ] }
# This methods should limit the number of users if a GET URL parameter is given
# named limit. For example, /users?limit=4 should only return the first four
# users.
# If the paramer given is invalid, then the response code must be 500.


@app.route("/users", methods=["GET"])
def contact():
    with db.cursor() as cursor:
        
        try:
            json = {"users" : []}
            query = "SELECT name FROM users"

            limit = request.args.get("limit", None)

            if limit is None:
                cursor.execute(query)
            else:
                cursor.execute(query + " LIMIT 0, %s", int(limit))

            for name in cursor.fetchall():
                json["users"].append(name[0])

        except (pymysql.err.ProgrammingError, ValueError):
            return "Malicious attempt revelead", 500

        return jsonify(json), 200


if __name__ == "__main__":
    db = pymysql.connect(host="localhost",
                         user=username,
                         password=password,
                         database=database,
                         charset="utf8mb4")
    with db.cursor() as cursor:
        populate.populate_db(cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0', port=80)