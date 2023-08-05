from typing import Generic

from moontour_common.models.rooms.participants.participant import Participant, ParticipantState
from moontour_common.models.user import User


class Team(Participant[ParticipantState], Generic[ParticipantState]):
    users: list[User] = []
    size: int = 2

    def insert_user(self, user: User):
        self.users.append(user)

    def remove_user(self, user_id: str):
        self.users = [user for user in self.users if user.id != user_id]

    def is_full(self) -> bool:
        return len(self.users) >= self.size

    def get_user_ids(self) -> set[str]:
        return {user.id for user in self.users}
