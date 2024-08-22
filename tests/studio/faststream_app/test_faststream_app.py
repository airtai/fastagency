import asyncio
import json
import random

import pytest
from faststream.nats import TestNatsBroker

from fastagency.studio.faststream_app import broker, register_handler, stream


@pytest.mark.nats
@pytest.mark.asyncio
async def test_register_handler() -> None:
    client_id = random.randint(1, 1000)
    async with TestNatsBroker(broker, with_real=True) as br:
        # br._connection = br.stream = AsyncMock()
        await br.publish(
            {"client_id": client_id},
            f"register.{client_id}",
        )
        await register_handler.wait_call(timeout=3)

        register_handler.mock.assert_called_once_with({"client_id": client_id})  # type: ignore[union-attr]

        # Later I will send a message to "ping.*" and will await for "pong.*" message


@pytest.mark.nats
@pytest.mark.asyncio
async def test_ping_handler() -> None:
    client_id = random.randint(1, 1000)

    msg_queue: asyncio.Queue = asyncio.Queue(maxsize=1)  # type: ignore [type-arg]

    @broker.subscriber(f"pong.{client_id}", stream=stream)
    async def pong_handler(msg: str) -> None:
        await msg_queue.put(msg)

    async with TestNatsBroker(broker, with_real=True) as br:
        await br.publish(
            {"client_id": client_id},
            f"register.{client_id}",
        )
        await register_handler.wait_call(timeout=3)

        register_handler.mock.assert_called_once_with({"client_id": client_id})  # type: ignore[union-attr]

        await br.publish({"msg": "ping"}, f"ping.{client_id}")
        # await ping_handler.wait_call(timeout=3)

        # ping_handler.mock.assert_called_once_with({"msg": "ping"})  # type: ignore[union-attr]

        result_set, _ = await asyncio.wait(
            (asyncio.create_task(msg_queue.get()),), timeout=3
        )
        assert len(result_set) == 1
        result = json.loads(result_set.pop().result())
        assert result["msg"] == "pong"
        assert "process_id" in result


@pytest.mark.nats
@pytest.mark.asyncio
async def test_ping_handler_with_wrong_message() -> None:
    client_id = random.randint(1, 1000)

    msg_queue: asyncio.Queue = asyncio.Queue(maxsize=1)  # type: ignore [type-arg]

    @broker.subscriber(f"pong.{client_id}", stream=stream)
    async def pong_handler(msg: str) -> None:
        await msg_queue.put(msg)

    async with TestNatsBroker(broker, with_real=True) as br:
        await br.publish(
            {"client_id": client_id},
            f"register.{client_id}",
        )
        await register_handler.wait_call(timeout=3)

        register_handler.mock.assert_called_once_with({"client_id": client_id})  # type: ignore[union-attr]

        msg_to_send = {"msg": "This is a random message"}
        await br.publish(msg_to_send, f"ping.{client_id}")  # type: ignore[arg-type]
        # await ping_handler.wait_call(timeout=3)

        # ping_handler.mock.assert_called_once_with({"msg": "ping"})  # type: ignore[union-attr]

        result_set, _ = await asyncio.wait(
            (asyncio.create_task(msg_queue.get()),), timeout=3
        )
        assert len(result_set) == 1
        result = json.loads(result_set.pop().result())
        expected_msg = (
            f"Unkown message: {msg_to_send}, please send 'ping' in body['msg']"
        )
        assert result["msg"] == expected_msg
        assert "process_id" in result
