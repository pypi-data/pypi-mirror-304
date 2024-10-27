#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from ..Application.Abstractions.base_service_collection import BaseServiceCollection

#------INTERFACES-----------------------------------------------------------

from ..Application.Abstractions.base_logging_service import BaseLoggingService
from ..Application.Abstractions.base_storage_service import BaseStorageService

#------/INTERFACES----------------------------------------------------------

#-----INSTANCE--------------------------------------------------------------

from .LoggingService.logging_service import LoggingService
from ..Persistence.Storages.storage_repository import StorageService

#-----/INSTANCE-------------------------------------------------------------

class DependencyInjection():
    def AddInfrastructure(services:BaseServiceCollection)->None:
        services.AddSingleton(BaseStorageService, StorageService)
        services.AddSingleton(BaseLoggingService, LoggingService)