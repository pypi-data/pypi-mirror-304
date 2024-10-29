from peewee import *

db = SqliteDatabase('db.sqlite3')

class DbContext(Model):
    class Meta:
        database = db