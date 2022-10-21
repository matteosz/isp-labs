import binascii
import hashlib
import random
import string

from pymysql.cursors import Cursor

seed = "randomseed"
entries = 20
message_length = 10  # words

wordlist = open('words.txt', 'r').readlines()
words = []
for i in range(len(wordlist)):
    words.append(wordlist[i].strip('\n'))


def random_word():
    """Return one random word."""
    return random.choice(words)


def random_message(r: random.Random):
    """Return n random words, between 5 and "message_length (seeded)."""
    return " ".join(r.sample(words, r.randint(5, message_length)))


def names(r: random.Random):
    """Return n random words, between 5 and "entries" (seeded)."""
    length = r.randint(5, entries)
    return r.sample(words, length)


def pwd(r: random.Random, user: str):
    h = hashlib.sha256()
    letters = r.sample(string.ascii_lowercase, 10)
    h.update("".join(letters).encode())
    h.update(user.encode())
    return binascii.hexlify(h.digest()).decode()


def get_data():
    """From a seed, return a random sample of users and messages.

    Args:
        seed (str): a random seed

    Returns:
        tuple: tuple of lists, respectively users and messages
    """
    r = random.Random()
    r.seed(seed.encode())
    list_names = names(r)
    users = [[name, pwd(r, name)] for name in list_names]
    msgs = [(u, random_message(r)) for u in list_names]
    return users, msgs


def empty_database(cursor: Cursor):
    """Empty the tables users and messages."""
    empty_users = "DELETE FROM users"
    empty_messages = "DELETE FROM messages"
    cursor.execute(empty_users)
    cursor.execute(empty_messages)


def populate_db(cursor: Cursor):
    """Empty the database then populate it with random data.

    Args:
        seed (str): random seed
        cursor (Cursor): Cursor to database
    """
    print("Emptying database")
    empty_database(cursor)

    users, msgs = get_data()

    sql_users = "INSERT INTO users (name,password) VALUES "
    sql_users += ",".join(["('" + u + "','" + p + "')" for u, p in users])

    sql_msgs = "INSERT INTO messages (name, message) VALUES "
    sql_msgs += ",".join(["('" + u + "','" + m + "')" for u, m in msgs])

    print("Filling DB with random users and messages")
    cursor.execute(sql_users)
    cursor.execute(sql_msgs)