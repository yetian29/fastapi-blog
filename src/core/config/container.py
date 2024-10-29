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
from src.infrastructure.db import Database
from src.infrastructure.repositories.post import IPostRepository, MongoPostRepository
from src.service.post import PostService


def init_container() -> punq.Container:
    container = punq.Container()

    container.register(Database, scope=punq.Scope.singleton)

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
