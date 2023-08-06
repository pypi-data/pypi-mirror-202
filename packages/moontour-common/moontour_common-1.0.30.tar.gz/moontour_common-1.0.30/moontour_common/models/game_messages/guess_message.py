from moontour_common.models.coordinates import Coordinates
from moontour_common.models.game_messages.game_message import GameMessage


class GuessMessage(GameMessage):
    coordinates: Coordinates
    user_id: str
