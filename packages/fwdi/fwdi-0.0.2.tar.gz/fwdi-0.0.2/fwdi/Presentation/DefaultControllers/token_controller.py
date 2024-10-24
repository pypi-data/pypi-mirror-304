#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from datetime import timedelta
from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ...Abstractions.base_user_repository import BaseUserRepository
from ...Application.Usecase.user_repository import UserRepository
from ...Abstractions.meta_service import MetaService
from ...Abstractions.base_logging_service import BaseLoggingService
from ...Domain.token import Token
from ...Infrastructure.JwtService.jwt_service import JwtService, ACCESS_TOKEN_EXPIRE_MINUTES

class TokenController(metaclass=MetaService):
    def __init__(self, logging_service:BaseLoggingService):
        super().__init__()
        self._logging:BaseLoggingService = logging_service
    
    def post(self, user_repository:UserRepository = Depends(), form_data:OAuth2PasswordRequestForm = Depends())->Token:
        user = JwtService.authenticate_user(user_repository.get_all(), form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        #--------Using service by created dependency injection service -------

        user_scopes = user_repository.get_user_scopes(user.email)

        #--------/Using service by created dependency injection service ------

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = JwtService.create_access_token(
            data={
                "sub": user.username, 
                "email": user.email,
                "scopes": user_scopes
                },
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")