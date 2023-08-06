from moontour_common.models.coordinates import Coordinates


class Location(Coordinates):
    map: str
    country: str
    famous: bool
