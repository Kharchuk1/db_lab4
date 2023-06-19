import os

USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
DB = os.environ["DB"]

connection = {
    "dbname": DB,
    "user": USER,
    "password": PASSWORD,
    "port": PORT,
    "host": HOST
}