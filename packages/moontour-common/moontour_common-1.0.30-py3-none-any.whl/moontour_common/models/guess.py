from datetime import datetime

import geopy.distance
from pydantic import BaseModel, Field

from moontour_common.models.coordinates import Coordinates

MAX_POINTS = 5000


class Guess(BaseModel):
    time: datetime = Field(default_factory=datetime.now)
    coordinates: Coordinates

    def compute_distance(self, target: Coordinates) -> float:
        return geopy.distance.geodesic(
            (target.latitude, target.longitude),
            (self.coordinates.latitude, self.coordinates.longitude)
        ).km

    def compute_points(self, target: Coordinates) -> int:
        distance = self.compute_distance(target)
        return max(MAX_POINTS - int(distance), 0)
