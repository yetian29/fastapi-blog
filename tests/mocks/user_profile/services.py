

from src.domain.user_profile.entities import UserProfile
from src.domain.user_profile.services import IUserProfileService
from tests.mocks.user_profile.factories import UserProfileFactory


class DummyUserProfileService(IUserProfileService):
    async def create(self, user: UserProfile) -> UserProfile:
        return user
    
    async def update(self, user: UserProfile) -> UserProfile:
        return user
    
    async def get_by_id(self, oid: str) -> UserProfile:
        return UserProfileFactory.build(oid=oid)
    