import json

from moontour_common.models.rooms.game_modes.health_room import HealthRoom
from moontour_common.models.rooms.game_modes.race_room import RaceRoom
from moontour_common.models.rooms.game_modes.streak_room import StreakRoom
from moontour_common.models.rooms.participants.player import Player
from moontour_common.models.rooms.participants.team import Team
from moontour_common.models.rooms.room import Room

ROOM_MODELS: dict[str, type[Room]] = {
    cls.__name__: cls for cls in
    {HealthRoom[Player], HealthRoom[Team], RaceRoom[Player], RaceRoom[Team], StreakRoom}
}


def get_room_model(type_: str) -> type[Room]:
    return ROOM_MODELS[type_]


def parse_room(room_raw: str) -> Room:
    room_dict = json.loads(room_raw)
    room_model = get_room_model(room_dict['type'])
    return room_model.parse_obj(room_dict)


async def get_room(id_: str) -> Room:
    room_raw = await Room.commands.get(id_)
    return parse_room(room_raw)
