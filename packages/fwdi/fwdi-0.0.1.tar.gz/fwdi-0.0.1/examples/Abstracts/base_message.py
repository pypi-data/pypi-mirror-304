from abc import ABCMeta, abstractmethod

from fwdi.Abstractions.base_service import BaseService
from enum_type_message import EnumTypeMessage

class BaseMessage(BaseService, metaclass=ABCMeta):

    @abstractmethod
    def set_msg(msg_type:EnumTypeMessage, msg:str):
        pass

    @abstractmethod
    def show_message(self, msg_type:EnumTypeMessage, message:str):
        pass
