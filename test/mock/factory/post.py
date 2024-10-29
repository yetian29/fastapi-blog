from polyfactory.factories import DataclassFactory

from src.domain.post.command import CreatePostCommand
from src.domain.post.entities import Post


class PostFactory(DataclassFactory[Post]):
    __model__ = Post


class CreatePostCommandFactory(DataclassFactory[CreatePostCommand]):
    __model__ = CreatePostCommand
