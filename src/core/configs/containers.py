from functools import lru_cache

import punq

from src.domain.post.services import IPostService
from src.domain.post.use_cases import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostListUseCase,
    GetPostUseCase,
    UpdatePostUseCase,
)
from src.domain.review.services import IReviewService
from src.domain.review.use_cases import (
    CreateOrUpdateReviewUseCase,
    DeleteReviewUseCase,
)
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserService,
)
from src.domain.user_auth.use_cases import AuthorizeUserUseCase, LoginUserUseCase
from src.infrastructure.database import Database
from src.infrastructure.repositories.post import IPostRepository, MongoPostRepository
from src.infrastructure.repositories.review import (
    IReviewRepository,
    MongoReviewRepository,
)
from src.infrastructure.repositories.user_auth import (
    IUserRepository,
    MongoUserRepository,
)
from src.services.post import PostService
from src.services.review import ReviewService
from src.services.user_auth import (
    CacheCodeService,
    LoginService,
    SMSSendService,
    UserService,
)


def get_container() -> punq.Container:
    return init_container()


@lru_cache(1)
def init_container() -> punq.Container:
    container = punq.Container()

    container.register(Database, scope=punq.Scope.singleton)

    # post
    container.register(IPostRepository, MongoPostRepository)
    container.register(IPostService, PostService)

    container.register(CreatePostUseCase)
    container.register(UpdatePostUseCase)
    container.register(DeletePostUseCase)
    container.register(GetPostUseCase)
    container.register(GetPostListUseCase)

    # user
    container.register(IUserRepository, MongoUserRepository)

    container.register(ICodeService, CacheCodeService)
    container.register(ISendService, SMSSendService)
    container.register(ILoginService, LoginService)
    container.register(IUserService, UserService)

    container.register(AuthorizeUserUseCase)
    container.register(LoginUserUseCase)

    # review
    container.register(IReviewRepository, MongoReviewRepository)
    container.register(IReviewService, ReviewService)

    container.register(CreateOrUpdateReviewUseCase)
    container.register(DeleteReviewUseCase)

    return container
