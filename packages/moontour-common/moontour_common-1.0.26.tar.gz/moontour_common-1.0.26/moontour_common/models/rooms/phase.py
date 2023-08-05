from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from moontour_common.models.coordinates import Coordinates
from moontour_common.models.guess import Guess
from moontour_common.models.location import Location


class PhaseStatus(StrEnum):
    waiting = 'waiting'
    running = 'running'
    finished = 'finished'


class Phase(BaseModel):
    target: Location
    status: PhaseStatus = PhaseStatus.waiting
    create_time: datetime = Field(default_factory=datetime.now)
    guesses: dict[str, Guess] = {}  # User ID to guess

    def insert_guess(self, user_id: str, guess: Guess):
        self.guesses[user_id] = guess
