import asyncio
import json
import sys
import logging
from logging import log, INFO, ERROR, DEBUG, WARN
from system.router import Router

logging.basicConfig(stream=sys.stdout, level=INFO)


def main(args):
    """Entrypoint for serverless function"""
    log(INFO, "Entered main function.")

    router = Router()
    
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(router.route(args))
