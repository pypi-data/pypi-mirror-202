from typing import Generic

from moontour_common.models.rooms.participants.participant import Participant, ParticipantState
from moontour_common.models.user import User


class Player(Participant[ParticipantState], Generic[ParticipantState]):
    user: User | None = None

    def insert_user(self, user: User):
        self.user = user

    def remove_user(self, user_id: str):
        if self.user.id == user_id:
            self.user = None

    def is_full(self) -> bool:
        return self.user is not None

    def get_user_ids(self) -> set[str]:
        return {self.user.id} if self.user else set()
