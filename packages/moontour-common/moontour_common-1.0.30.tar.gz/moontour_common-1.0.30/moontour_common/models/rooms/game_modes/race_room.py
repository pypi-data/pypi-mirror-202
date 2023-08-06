from typing import Generic, TypeVar

from pydantic import BaseModel

from moontour_common.models.guess import Guess
from moontour_common.models.rooms.participants.participant import Participant
from moontour_common.models.rooms.phase import Phase
from moontour_common.models.rooms.room import Room, modify_room


class ParticipantState(BaseModel):
    current_phase: int = 0
    stunned: bool = False


ParticipantType = TypeVar('ParticipantType', bound=Participant)


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
        return any([state.current_phase == self.phase_count for state in self.participants_state.values()])
