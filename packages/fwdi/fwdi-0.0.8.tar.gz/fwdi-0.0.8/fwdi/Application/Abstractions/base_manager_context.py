from .base_service import BaseService
from ...Application.DTO.Repository.model_user import *
from abc import ABCMeta, abstractmethod


class BaseManagerContext(BaseService, metaclass=ABCMeta):
     
     @abstractmethod
     def get_metadata_user(self) -> User:
          pass

     @abstractmethod
     def get_metadata_permission(self) -> Permissions:
          pass

     @abstractmethod
     def get_metadata_scopes(self) -> Scope:
          pass