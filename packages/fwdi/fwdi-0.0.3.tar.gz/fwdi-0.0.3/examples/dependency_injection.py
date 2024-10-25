from examples.guest_controller import GuestController
from admin_controller import AdminController
from user_controller import UserController
from fwdi.WebApp.web_application import WebApplication


class WebService():
    def AddControllers(app:WebApplication)->None:
        app.map_controller(GuestController())
        app.map_controller(AdminController())
        app.map_controller(UserController())