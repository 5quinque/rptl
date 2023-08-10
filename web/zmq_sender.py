# import asyncio
# import json
import logging

import zmq
import zmq.asyncio


logger = logging.getLogger(__name__)

class ZmqSender:
    def __init__(self, zmq_connect_address="tcp://127.0.0.1:5555"):
        self._zmq_connect_address = zmq_connect_address
        self._context = zmq.asyncio.Context()
        self.socket = self._context.socket(zmq.REQ)

        logger.debug(f"Connecting to {self._zmq_connect_address}")
        self.socket.connect(self._zmq_connect_address)
        logger.debug("Connected")

    async def send_json(self, data):
        logger.debug(f"Sending data: {data}")
        await self.socket.send_json(data)
        logger.debug("Waiting for response")
        resp = await self.socket.recv_string()
        logger.debug(f"Received response: {resp}")

        return resp
