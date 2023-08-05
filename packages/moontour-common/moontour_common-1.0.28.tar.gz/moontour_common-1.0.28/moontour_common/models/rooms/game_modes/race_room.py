from typing import Generic

from pydantic import BaseModel

from moontour_common.models.guess import Guess
from moontour_common.models.rooms.phase import Phase
from moontour_common.models.rooms.room import Room, modify_room
from moontour_common.models.rooms.room_model import ParticipantType


class ParticipantState(BaseModel):
    current_phase: int = 0
    stunned: bool = False


class RaceRoom(Room[Phase, ParticipantType, ParticipantState], Generic[ParticipantType]):
    phase_count: int = 10
    stun_duration: float = 5

    @modify_room
    def initialize_phases(self, phases: list[Phase]):
        self.phases = phases

    def _on_guess(self, user_id: str, guess: Guess):
        participant = self._get_participant(user_id)
        target = self.phases[participant.state.current_phase].target
        if guess.compute_points(target) > 4000:
            participant.state.current_phase += 1
        else:
            participant.state.stunned = True

    def should_close(self) -> bool:
        return any([participant.state.current_phase == self.phase_count for participant in self.participants])
