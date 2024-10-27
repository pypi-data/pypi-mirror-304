#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from abc import ABCMeta, abstractmethod
from typing import Type, TypeVar, Protocol

from .base_di_container import BaseDIConteiner

TService = TypeVar('TService')

class BaseServiceCollection(metaclass=ABCMeta):
    @property
    @abstractmethod
    def ServiceDescriptor(self)->set:
        ...

    @abstractmethod
    def AddSingleton(self, implementation:TService):
        pass

    @abstractmethod
    def AddSingleton(self, type_service:Type[TService], implementation:TService):
        pass

    @abstractmethod
    def AddTransient(self, implementation: TService):
        pass

    @abstractmethod
    def AddTransient(self, type_service:Type[TService], implementation:TService):
        pass

    @abstractmethod
    def GenerateContainer(self)->BaseDIConteiner:
        pass
