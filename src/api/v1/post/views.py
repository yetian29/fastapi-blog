

from fastapi import APIRouter, Depends

from src.api.v1.post.schemas import PostInSchema, PostOutSchema
from src.api.v1.schemas import ApiResponse
import punq

from src.core.configs.containers import get_container
from src.domain.post.commands import CreatePostCommand
from src.domain.post.use_cases import CreatePostUseCase

router = APIRouter()

@router.post("/", response_model=ApiResponse[PostOutSchema])
async def create_post_views(
    post_in: PostInSchema,
    container: punq.Container = Depends(get_container)
) -> ApiResponse[PostOutSchema]:
    use_case: CreatePostUseCase = container.resolve(CreatePostUseCase)
    command = CreatePostCommand(
        post=post_in.to_entity()
    )
    post = await use_case.execute(command)
    return ApiResponse(
        data=PostOutSchema.from_entity(post)
    )

    