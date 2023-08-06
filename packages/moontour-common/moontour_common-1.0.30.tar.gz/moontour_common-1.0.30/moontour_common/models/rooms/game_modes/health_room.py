from typing import Generic, TypeVar

from pydantic import BaseModel

from moontour_common.models.rooms.participants.participant import Participant
from moontour_common.models.rooms.phase import Phase
from moontour_common.models.rooms.room import Room

START_HEALTH = 5000


class HealthPhase(Phase):
    damage_multiplier: float = 1


class ParticipantState(BaseModel):
    health: int = START_HEALTH


ParticipantType = TypeVar('ParticipantType', bound=Participant)


class HealthRoom(Room[HealthPhase, ParticipantType, ParticipantState], Generic[ParticipantType]):
    guess_duration: float = 15  # Time between first guess to phase ending

    def should_close(self) -> bool:
        dead_count = len([state for state in self.participants_state.values() if state.health == 0])
        return dead_count == len(self.participants) - 1

    def _finalize_phase(self, phase: HealthPhase):
        guesses = phase.guesses
        best_guess = max([guess.compute_points(phase.target) for guess in guesses.values()]) if guesses else 0
        for participant, state in self.participants_data.values():
            participant_guesses = {
                guesses[user_id].compute_points(phase.target)
                for user_id in participant.get_user_ids() if user_id in guesses
            }
            best_participant_guess = max(participant_guesses) if participant_guesses else 0
            damage = best_guess - best_participant_guess
            state.health = max(state.health - damage, 0)
