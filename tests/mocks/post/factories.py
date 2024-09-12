from polyfactory.factories import DataclassFactory

from src.domain.post.commands import CreatePostCommand, DeletePostCommand, GetPostCommand, UpdatePostCommand
from src.domain.post.entities import Post


class PostFactory(DataclassFactory[Post]):
    __model__ = Post
    

class CreatePostCommandFactory(DataclassFactory[CreatePostCommand]):
    __model__ = CreatePostCommand

class UpdatePostCommandFactory(DataclassFactory[UpdatePostCommand]):
    __model__ = UpdatePostCommand

class DeletePostCommandFactory(DataclassFactory[DeletePostCommand]):
    __model__ = DeletePostCommand

class GetPostCommandFactory(DataclassFactory[GetPostCommand]):
    __model__ = GetPostCommand