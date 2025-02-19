import asyncio
import importlib.resources
import logging
from datetime import datetime
from pathlib import Path

import zmq
import zmq.asyncio

from timelapse import sort_colour_profile, timestamp_images

logger = logging.getLogger(__name__)


class Daemon:
    def __init__(
        self,
        timelapse_interval=300,
        start_hour=None,
        start_minute=None,
        end_hour=None,
        end_minute=None,
        no_camera=False
    ):
        self.timelapse_interval = timelapse_interval
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.end_hour = end_hour
        self.end_minute = end_minute
        self.zmq_bind_address = "tcp://127.0.0.1:5555"

        self.timelapse_running = False
        if no_camera:
            from timelapse.mock_camera import Camera
        else:
            from timelapse.camera import Camera
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
                await socket.send(filename.encode("utf-8"))
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
        logger.debug(f"Capturing filename {filename}")
        self.camera.capture_still(filename)

        return filename

    async def run_timelapse(self):
        # log the datetime timestamp when we last took a stil
        last_still_timestamp = None

        while self.timelapse_running:
            logger.debug(f"Running: {self.timelapse_running}")
            try:
                if (
                    last_still_timestamp is not None
                    and (datetime.now() - last_still_timestamp).seconds
                    < self.timelapse_interval
                ):
                    # calculate how long to sleep for based on the timelapse_interval
                    time_to_sleep = (
                        self.timelapse_interval
                        - (datetime.now() - last_still_timestamp).seconds
                    )
                    logger.debug(f"[timelapse] Sleeping for {time_to_sleep} seconds.")
                    await asyncio.sleep(time_to_sleep)

                last_still_timestamp = datetime.now()

                now = datetime.now()
                if self.start_hour:
                    start_time = now.replace(hour=self.start_hour, minute=self.start_minute)
                    if now < start_time:
                        logger.debug("Outside of start time.")
                        continue

                if self.end_hour:
                    end_time = now.replace(hour=self.end_hour, minute=self.end_minute)
                    if now > end_time:
                        logger.debug("Outside of end time.")
                        continue

                self.capture_current_image()
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt, exiting.")
                self.timelapse_running = False

        # self.camera.stop()

    async def run_timestamp_images(self):
        process_interval = 60 * 60

        last_still_timestamp = None

        while self.timelapse_running:
            if (
                last_still_timestamp is not None
                and (datetime.now() - last_still_timestamp).seconds < process_interval
            ):
                # calculate how long to sleep for based on the process_interval
                time_to_sleep = (
                    process_interval - (datetime.now() - last_still_timestamp).seconds
                )
                logger.debug(f"[timestamp] Sleeping for {time_to_sleep} seconds.")
                await asyncio.sleep(time_to_sleep)

            last_still_timestamp = datetime.now()

            try:
                timestamp_images.run()
            except Exception as e:
                logger.exception(e)

    async def run_sort_colour_profile(self):
        cp_files = sort_colour_profile.Files()

        while self.timelapse_running:
            if not cp_files.is_timestamped_images_to_process():
                logger.debug("[sort colour profile] Sleeping for 6 hours.")
                await asyncio.sleep(60 * 60 * 6)  # 6 hours

            try:
                sort_colour_profile.run()
            except Exception as e:
                logger.exception(e)

    async def run_daily_video(self):
        day_ran = None
        while self.timelapse_running:
            now = datetime.now()
            start_time = now.replace(hour=1, minute=0)
            end_time = now.replace(hour=2, minute=0)

            # We don't want to run again on the same day
            # And only run between 1am-2am
            if day_ran == now.day or now < start_time or now > end_time:
                logger.debug("[daily video] Sleeping for 30 minutes.")
                await asyncio.sleep(30 * 60)  # 30 minutes
                continue

            # if sort_colour_profile:
            #   script_name = "generate_sort_daily_videos.sh"
            day_ran = now.day

            script_path = str(
                    importlib.resources.files("timelapse").joinpath("generate_timelapse.sh")
            )
            logger.debug(f"[daily video] running script {script_path}")
            await self.run_shellscript(script_path)

    async def run_shellscript(self, shellscript):
        proc = await asyncio.create_subprocess_shell(
            shellscript,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        logger.debug(f"[{shellscript!r} exited with {proc.returncode}]")
        if stdout:
            logger.debug(f"[stdout]\n{stdout.decode()}")
        if stderr:
            logger.debug(f"[stderr]\n{stderr.decode()}")
