from abc import ABCMeta, abstractmethod

from .base_manager_context import BaseManagerContext
from .base_service import BaseService


class BaseUserRepository(BaseService, metaclass=ABCMeta):
    
    @abstractmethod
    def get_all(self, manager_db_context: BaseManagerContext) -> list[dict]:
        ...
    
    @abstractmethod
    def get_user_scopes(self, email, manager_db_context: BaseManagerContext) -> list[str]:
        ...