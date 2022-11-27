import asyncio
import logging
from logging import DEBUG, WARN, ERROR, INFO
from lib.s3 import S3
from controllers.generic import GenericController

class AdminController(GenericController):
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("AdminController")
        self.l = logger.log
        self.l(INFO, "Initializing AdminController.")
        super().__init__(*args, **kwargs)

    async def entry_point(self):
        return {}