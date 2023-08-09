from datetime import datetime
from pathlib import Path
import asyncio
import logging

import zmq
import zmq.asyncio

from timelapse.camera import Camera


logger = logging.getLogger(__name__)

class Daemon:
    def __init__(self, zmq_bind_address="tcp://127.0.0.1:5555"):
        self.zmq_bind_address = zmq_bind_address

        self.timelapse_running = False
        self.camera = Camera()

    async def zmq_server(self):
        context = zmq.asyncio.Context()
        socket = context.socket(zmq.REP)
        socket.bind(self.zmq_bind_address)

        while True:
            logger.debug("Waiting for message...")
            message = await socket.recv_json()
            logger.debug(f"Received message: {message}")
            action = message.get("action", None)
            if action == "start_camera":
                pass
                # self.start()
                # await socket.send(b"started")
            elif action == "stop_timelapse":
                self.stop()
                await socket.send(b"stopped")
            elif action == "timelapse_status":
                await socket.send(b"started" if self.timelapse_running else b"stopped")
            elif action == "capture_current_image":
                filename = self.capture_current_image("requested_images")
                await socket.send(f"captured {filename}".encode("utf-8"))
            else:
                await socket.send(b"unknown command")

    def start(self):
        self.timelapse_running = True
        # self.camera.start()

    def stop(self):
        self.timelapse_running = False
        # self.camera.stop()
    
    def capture_current_image(self, image_directory="images"):
        dir_name = datetime.now().strftime("%Y%m%d")

        # create the directory if it doesn't exist
        Path(f"{image_directory}/{dir_name}").mkdir(parents=True, exist_ok=True)

        filename = f"{image_directory}/{dir_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        self.camera.capture_still(filename)

        return filename

    async def run_timelapse(self):
        timelapse_interval = 300
        # 6 hours
        # timelapse_duration = 6 * 60 * 60

        # log the datetime timestamp when we last took a stil
        last_still_timestamp = None

        while self.timelapse_running:
            logger.debug(f"Running: {self.timelapse_running}")
            try:
                if last_still_timestamp != None and (datetime.now() - last_still_timestamp).seconds < timelapse_interval:
                    # calculate how long to sleep for based on the timelapse_interval
                    time_to_sleep = timelapse_interval - (datetime.now() - last_still_timestamp).seconds
                    logger.debug(f"Sleeping for {time_to_sleep} seconds.")
                    await asyncio.sleep(time_to_sleep)

                last_still_timestamp = datetime.now()

                self.capture_current_image()
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt, exiting.")
                self.timelapse_running = False

        # self.camera.stop()