from ..Application.DTO.Repository.model_user import *
from ..Application.Abstractions.db_context import db

class DefaultInitializeDB():
    def init_db():
        db.connect()
        db.create_tables([Scope, Permissions, User, Permissions.scopes_detail.get_through_model()], safe = True)
        DefaultInitializeDB.__default_data()
        db.close()

    def __default_data():
        if len(Scope.select()) == 0:
            scopes_info = Scope(name='guest', description='Info scopes')
            scopes_info.save()
            
            scopes_user = Scope(name='user', description='User scopes')
            scopes_user.save()

            scopes_admin = Scope(name='admin', description='Admin scopes')
            scopes_admin.save()

        if len(Permissions.select()) == 0:
            permission_admin = Permissions(name='Admin')
            permission_admin.save()

            permission_admin.scopes_detail.add([scopes_info, scopes_user, scopes_admin])
            permission_admin.save()
            
            permission_user = Permissions(name='User')
            permission_user.save()
            
            permission_user.scopes_detail.add([scopes_info, scopes_user])
            permission_user.save()
            
            permission_guest = Permissions(name='Info')
            permission_guest.save()
            permission_guest.scopes_detail.add([scopes_info])
            permission_guest.save()
        
        from ..Infrastructure.JwtService.jwt_service import JwtService
        if len(User.select()) == 0:
            user = User(username='admin', full_name='Administrator', email='admin@admin.ru', hashed_password=JwtService.get_password_hash('admin'), disabled=False, scopes=permission_admin)
            user.full_name = "Admin adminich"
            user.save()

            user = User(username='user', full_name='user', email='user@user.ru', hashed_password=JwtService.get_password_hash('user'), disabled=False, scopes=permission_user)
            user.full_name = "User userovich"
            user.save()
            
            user = User(username='guest', full_name='guest', email='guest@guest.ru', hashed_password=JwtService.get_password_hash('guest'), disabled=False, scopes=permission_guest)
            user.full_name = "Guest guestovich"
            user.save()