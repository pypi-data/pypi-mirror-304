from abc import ABCMeta, abstractmethod

from fwdi.Application.Abstractions.base_service import BaseService
from Application.Abstractions.base_message import BaseMessage

class BaseComposit(BaseService, metaclass=ABCMeta):   
    @abstractmethod
    def run_once(self)->BaseMessage:
        pass