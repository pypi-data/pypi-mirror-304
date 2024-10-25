from .model_scope import *

class Permissions(DbContext):
    id = PrimaryKeyField()
    name = CharField()
    scopes_detail = ManyToManyField(Scope, backref='scopes')