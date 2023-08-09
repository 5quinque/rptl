import asyncio
import logging

from timelapse.daemon import Daemon


logger = logging.getLogger(__name__)


async def _main():
    daemon = Daemon()
    daemon.start()

    # create two tasks from daemon.run_timelapse() and daemon.zmq_server()
    tasks = [
        asyncio.create_task(daemon.run_timelapse()),
        asyncio.create_task(daemon.zmq_server()),
    ]

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # asy

def main():
    logging.basicConfig(
        # level=opts["--log-level"],
        level="DEBUG",
        format="[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s",
        force=True,
    )
    asyncio.run(_main())

if __name__ == "__main__":
    main()