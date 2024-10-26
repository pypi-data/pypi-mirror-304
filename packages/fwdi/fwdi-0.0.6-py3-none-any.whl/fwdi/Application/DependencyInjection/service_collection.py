#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from typing import Type

from ...Application.Abstractions.base_di_container import BaseDIConteiner
from ...Application.Abstractions.base_service_collection import BaseServiceCollection
from ...Application.Abstractions.service_descriptor import ServiceDescriptor
from ...Domain.Enums.service_life import ServiceLifetime
from .dependency_container import DependencyContainer, TService

class ServiceCollection(BaseServiceCollection):
    def __init__(self) -> None:        
        self._serviceDescriptor:set[ServiceDescriptor] = set()
        #self._serviceDescriptor = set()

    @property
    def ServiceDescriptor(self)->set:
        return self._serviceDescriptor

    def AddSingleton(self, implementation:TService):
        self._serviceDescriptor.add(ServiceDescriptor.create(type(implementation), ServiceLifetime.Singleton))
	
    def AddSingleton(self, type_service:Type[TService], implementation:TService):
        self._serviceDescriptor.add(ServiceDescriptor.create(type_service, implementation, ServiceLifetime.Singleton))

    def AddTransient(self, implementation: TService):
        self._serviceDescriptor.add(ServiceDescriptor.create(implementation, ServiceLifetime.Transient))

    def AddTransient(self, type_service:Type[TService], implementation:TService):
        self._serviceDescriptor.add(ServiceDescriptor.create(type_service, implementation, ServiceLifetime.Transient))

    def GenerateContainer(self)->BaseDIConteiner:
        return DependencyContainer(self._serviceDescriptor)