from ..Application.Abstractions.base_manager_context import BaseManagerContext
from .manager_db_context import ManagerDbContext
from ..Application.Abstractions.base_service_collection import BaseServiceCollection

class DependencyInjection():
    def AddPersistence(services:BaseServiceCollection)->None:
        services.AddTransient(BaseManagerContext, ManagerDbContext)