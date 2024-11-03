from functools import lru_cache

import punq

from src.domain.post.services import IPostService
from src.domain.post.use_case import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostListUseCase,
    GetPostUseCase,
    UpdatePostUseCase,
)
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserAuthService,
)
from src.domain.user_auth.use_case import AuthorizeUseAuthUseCase, LoginUserAuthUseCase
from src.infrastructure.db import Database
from src.infrastructure.repositories.post import IPostRepository, MongoPostRepository
from src.infrastructure.repositories.user_auth import (
    IUserAuthRepository,
    MongoUserAuthRepository,
)
from src.service.post import PostService
from src.service.user_auth import (
    CodeService,
    LoginService,
    SendService,
    UserAuthService,
)


def init_container() -> punq.Container:
    container = punq.Container()

    container.register(Database, scope=punq.Scope.singleton)

    # Register User Auth
    container.register(IUserAuthRepository, MongoUserAuthRepository)
    container.register(ICodeService, CodeService)
    container.register(ISendService, SendService)
    container.register(ILoginService, LoginService)
    container.register(IUserAuthService, UserAuthService)
    container.register(AuthorizeUseAuthUseCase)
    container.register(LoginUserAuthUseCase)

    # Register Post
    container.register(IPostRepository, MongoPostRepository)

    container.register(IPostService, PostService)

    container.register(CreatePostUseCase)
    container.register(UpdatePostUseCase)
    container.register(DeletePostUseCase)
    container.register(GetPostUseCase)
    container.register(GetPostListUseCase)

    return container


@lru_cache(1)
def get_container() -> punq.Container:
    return init_container()
