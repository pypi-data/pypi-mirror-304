from fastapi import Depends, Security
from Application.Abstractions.base_composit import BaseComposit

from fwdi.Application.Abstractions.base_controller import BaseController
from fwdi.Application.Abstractions.meta_service import MetaService
from fwdi.Application.DTO.Auth.model_user import User
from fwdi.Infrastructure.JwtService.jwt_service import JwtService

class UserController(BaseController, metaclass=MetaService):
    def __init__(self, composite:BaseComposit, base_path:str='/'):
        super().__init__(base_path)
        self.__composite:BaseComposit = composite
    
    async def get(self, current_user: User = Security(JwtService.get_current_active_user, scopes=["user"]),):
        result_composit_test = self.__composite.run_once()
        return {
            "Controller": self.__class__.__name__,
            "Method 'GET'": "Hello from KSU Flat Web Dependency Injection platform",
            "Composite result":result_composit_test,
            "Current user": {
                "Login": current_user.username,
                "Email": current_user.email,
                }
            }
    