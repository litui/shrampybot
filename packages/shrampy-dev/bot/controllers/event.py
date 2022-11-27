import asyncio
import logging
from logging import DEBUG, WARN, ERROR, INFO
from lib.s3 import S3
from controllers.generic import GenericController

class EventController(GenericController):
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("EventController")
        self.l = logger.log
        self.l(INFO, "Initializing EventController.")
        super().__init__(*args, **kwargs)

    async def entry_point(self):
        if self._method == "patch":
            pass
        return super().entry_point()