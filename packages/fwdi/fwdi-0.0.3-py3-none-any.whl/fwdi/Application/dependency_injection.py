from ..Application.Abstractions.base_user_repository import BaseUserRepository
from ..Application.Abstractions.base_service_collection import BaseServiceCollection
from .Usecase.user_repository import UserRepository

class DependencyInjection():
    def AddApplication(services:BaseServiceCollection)->None:
        services.AddTransient(BaseUserRepository, UserRepository)