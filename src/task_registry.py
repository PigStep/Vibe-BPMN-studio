import asyncio
import logging

logger = logging.getLogger(__name__)


class TaskRegistry:
    _tasks: dict[str, asyncio.Task] = {}

    @classmethod
    def register(cls, session_id: str, task: asyncio.Task):
        old_task = cls._tasks.get(session_id, None)

        if old_task and not old_task.done():
            # TODO: send notification. User need to know previous answer was killed
            # TODO: add true cancelation mechanism
            # TODO: add cleaning mechanism
            logger.info(
                "Session id: %s. Face with multiple task run. Canceling old one",
                session_id,
            )
            old_task.cancel()
        cls._tasks[session_id] = task
