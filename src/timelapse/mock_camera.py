import logging
import time


logger = logging.getLogger(__name__)


class Camera:
    def __init__(self):
        logger.debug("Loading mock camera.")
        time.sleep(0.1)

        self.start()

    def set_hdr(self, enable=True):
        pass

    def start(self):
        logger.debug("Starting camera.")

    def capture_still(self, filename):
        logger.info(f"Capturing still to {filename}")
        time.sleep(0.1)
        logger.info(f"Captured still to {filename}")

    def stop(self):
        logger.debug("Stopping camera.")
