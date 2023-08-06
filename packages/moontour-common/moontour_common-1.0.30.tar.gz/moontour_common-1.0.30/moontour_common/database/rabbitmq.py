import os

import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue, ExchangeType

from moontour_common.models.game_messages.game_message import GameMessage

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
ROOMS_EXCHANGE_NAME = 'rooms'
GAME_EXCHANGE_NAME = 'game'
GAME_QUEUE_NAME = 'game'

_channel: AbstractChannel | None = None


async def get_rabbitmq_client() -> AbstractChannel:
    global _channel
    if _channel is None:
        connection = await aio_pika.connect_robust(host=RABBITMQ_HOST)
        _channel = await connection.channel()
    return _channel


async def get_rooms_exchange() -> AbstractExchange:
    client = await get_rabbitmq_client()
    return await client.declare_exchange(name=ROOMS_EXCHANGE_NAME, type=ExchangeType.TOPIC)


async def declare_player_queue(room_id: str, user_id: str) -> AbstractQueue:
    client = await get_rabbitmq_client()
    queue_name = f'{room_id}.{user_id}'
    queue = await client.declare_queue(name=queue_name, auto_delete=True)
    exchange = await get_rooms_exchange()
    await queue.bind(exchange, routing_key=f'{room_id}.*')
    return queue


async def get_game_exchange() -> AbstractExchange:
    client = await get_rabbitmq_client()
    return await client.declare_exchange(name='x-delayed-message', type=ExchangeType.X_DELAYED_MESSAGE,
                                         arguments={'x-delayed-type': 'direct'})


async def declare_game_queue() -> AbstractQueue:
    client = await get_rabbitmq_client()
    queue = await client.declare_queue(name=GAME_QUEUE_NAME)
    exchange = await get_game_exchange()
    await queue.bind(exchange, routing_key=GAME_QUEUE_NAME)
    return queue


async def send_game_message(game_message: GameMessage, delay: float = 0):
    exchange = await get_game_exchange()
    await exchange.publish(
        Message(body=game_message.json().encode(), headers={'x-delay': 1000 * delay}),
        routing_key=GAME_QUEUE_NAME
    )
