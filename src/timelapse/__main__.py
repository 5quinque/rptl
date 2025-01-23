"""Raspberry Pi Time Lapse.

Usage:
  rptl [options]

Options:
  -h --help             Show this screen.
  --version             Show version.
  --interval=<seconds>  Interval [default: 300].
  --start-time=<HHMM>   Time to start..
  --end-time=<HHMM>     Time to stop
  --log-level=<LEVEL>   Log level [default: INFO]

"""

import asyncio
import logging
import re

from docopt import docopt

from timelapse.daemon import Daemon

logger = logging.getLogger(__name__)


async def _main(interval, start_hour, start_minute, end_hour, end_minute):
    daemon = Daemon(interval, start_hour, start_minute, end_hour, end_minute)
    daemon.start()

    tasks = [
        asyncio.create_task(daemon.run_timelapse()),
        asyncio.create_task(daemon.run_timestamp_images()),
        asyncio.create_task(daemon.run_sort_colour_profile()),
        asyncio.create_task(daemon.zmq_server()),
    ]

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


def main():
    arguments = docopt(__doc__, version="RPTL V0.1")
    logging.basicConfig(
        level=arguments["--log-level"],
        format="[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s",
        force=True,
    )
    start_hour = None
    start_minute = None
    end_hour = None
    end_minute = None
    if arguments["--start-time"]:
        if re.match(r"\d{4}$", arguments["--start-time"]):
            start_hour = int(arguments["--start-time"][:2])
            start_minute = int(arguments["--start-time"][2:])
        else:
            logger.info("Invalid start time")
            print(__doc__)
            return
    if arguments["--end-time"]:
        if re.match(r"\d{4}$", arguments["--end-time"]):
            end_hour = int(arguments["--end-time"][:2])
            end_minute = int(arguments["--end-time"][2:])
        else:
            logger.info("Invalid end time")
            print(__doc__)
            return
    interval = int(arguments["--interval"])
    asyncio.run(_main(interval, start_hour, start_minute, end_hour, end_minute))


if __name__ == "__main__":
    main()
