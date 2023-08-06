from pydantic import BaseModel

from moontour_common.models.coordinates import Coordinates
from moontour_common.models.guess import Guess
from moontour_common.models.rooms.participants.player import Player
from moontour_common.models.rooms.phase import Phase
from moontour_common.models.rooms.room import Room


class StreaksPhase(Phase):
    guess: Guess | None = None

    def insert_guess(self, user_id: str, coordinates: Coordinates):
        self.guess = Guess(coordinates=coordinates)


class ParticipantState(BaseModel):
    streak: int = 0


class StreakRoom(Room[StreaksPhase, Player, ParticipantState]):
    pass
