import sqlite3 as sql
from hashlib import sha256
import re

class Database:
    def __init__(self, dbName='./db/users.db'):
        self.dbName = dbName

    def SHA256_Encoder(self, password):
        return sha256(password.encode()).hexdigest()

    def login(self, credentials: list()) -> bool:
        #self.user       = credentials[0]
        #self.password   = credentials[1]
        #self.cursor.execute(f'SELECT * from user WHERE username="{self.user}" AND password="{self.password}"')
        #return len(self.cursor.fetchall()) > 0
        pass

    def connect(self):
        self.manipulator = sql.connect(self.dbName)
        self.manipulator.create_function('sha256', 1, self.SHA256_Encoder)
        self.cursor      = self.manipulator.cursor()

    def disconnect(self):
        self.manipulator.close()

    def insert_user(self, data_user: list()):
        self.cursor.execute(f'INSERT INTO user VALUES (?, ?, sha256(?), ?)', data_user)
        self.manipulator.commit()

    def get_all(self):
        self.cursor.execute(f'SELECT * FROM user')
        return self.cursor.fetchall()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def seed(self):
        self.manipulator = sql.connect(self.dbName)
        self.cursor      = self.manipulator.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username CHAR(30) NOT NULL,
        password CHAR(200) NOT NULL, nickname CHAR(30) UNIQUE)''')
        self.manipulator.commit()