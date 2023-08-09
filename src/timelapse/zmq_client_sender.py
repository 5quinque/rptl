import asyncio
import json
import logging

import zmq
import zmq.asyncio


logger = logging.getLogger(__name__)

class ZmqSender:
    def __init__(self, address, port):
        self._address = address
        self._port = port
        self._context = zmq.asyncio.Context()
        self.socket = self._context.socket(zmq.REQ)

        logger.debug(f"Connecting to {self._address}:{self._port}")
        self.socket.connect(f"tcp://{self._address}:{self._port}")
        logger.debug("Connected")

    async def send_json(self, data):
        logger.debug(f"Sending data: {data}")
        await self.socket.send_json(data)
        logger.debug("Waiting for response")
        resp = await self.socket.recv_string()
        logger.debug(f"Received response: {resp}")


if __name__ == "__main__":
    logging.basicConfig(
        # level=opts["--log-level"],
        level="DEBUG",
        format="[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s",
        force=True,
    )
    sender = ZmqSender("127.0.0.1", 5555)
    asyncio.run(sender.send_json({"action": "capture_current_image"}))