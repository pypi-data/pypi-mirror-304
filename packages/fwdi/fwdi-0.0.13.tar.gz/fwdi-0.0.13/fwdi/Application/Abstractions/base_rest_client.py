from abc import ABCMeta, abstractmethod
from pydantic import BaseModel

from .base_service import BaseService


class BaseRestClient(BaseService, metaclass=ABCMeta):
    
    @abstractmethod
    def login(self, url:str='/token')->bool:
        ...
    
    @abstractmethod
    def get(self, path:str, _data:BaseModel=None, _params=None)->any:
        ...

    @abstractmethod
    def post(self, path:str, _data:BaseModel=None, _params=None)->any:
        ...