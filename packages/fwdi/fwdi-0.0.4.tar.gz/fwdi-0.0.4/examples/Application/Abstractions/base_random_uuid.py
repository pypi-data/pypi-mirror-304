from abc import ABCMeta, abstractmethod
from uuid import UUID

from fwdi.Application.Abstractions.base_service import BaseService

class BaseRandomGUID(BaseService, metaclass=ABCMeta):
    @abstractmethod
    def get_id(self)->UUID:
        ...

    @abstractmethod
    def get_next(self)->UUID:
        ...