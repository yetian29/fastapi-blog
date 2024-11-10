from datetime import datetime
from uuid import uuid4

from src.domain.user_profile.entities import UserProfile
from src.domain.user_profile.service import IUserProfileService
from test.mock.factory.user_profile import UserProfileFactory


class DummyUserProfileService(IUserProfileService):
    async def get_by_oid(self, oid: str) -> UserProfile:
        return UserProfileFactory.build(oid=oid)

    async def create(self, user_profile: UserProfile) -> UserProfile:
        user_profile.oid = str(uuid4())
        user_profile.created_at = datetime.now()
        user_profile.updated_at = datetime.now()
        return user_profile

    async def update(self, user_profile: UserProfile) -> UserProfile:
        return user_profile
