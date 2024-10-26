from ....Application.Abstractions.db_context import *

class Scope(DbContext):
    id = PrimaryKeyField()
    name = CharField()
    description = CharField()