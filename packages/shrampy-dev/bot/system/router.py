import json
import logging
from controllers.event import EventController
from controllers.admin import AdminController
from controllers.user import UserController
from logging import DEBUG, INFO, WARN, ERROR
from urllib.parse import parse_qs

class Router():
    ERROR_MAP = {
        5: "Unhandled exception occurred while routing: {}",
        10: "No arguments to route.",
        11: "No route provided.",
        12: "Invalid route: {}.",
        13: "No applicable methods or invalid command.",
        14: "Authentication failed.",
        15: "Key not found in input json: {}",
        16: "Corrupt json found on input"
    }

    def __init__(self):
        logger = logging.getLogger("Router")
        self.l = logger.log
        self.l(INFO, "Initializing Router object")

        self._path_map = {
            "admin": AdminController,
            "event": EventController,
            "user": UserController,
        }

    async def route(self, args):
        self.l(INFO, "Processing route")
        self._args = args
        self.l(DEBUG, "Argument dump: {}".format(args))
        self._headers = args.get("__ow_headers", {})
        self._body_raw = args["__ow_body"]
        try:
            self._body = json.loads(self._body_raw)
        except json.JSONDecodeError:
            self._body = self._body_raw

        self._path = args.get("__ow_path", "").split('/')
        self._path.pop(0)
        self._method = args["__ow_method"]
        self._query = parse_qs(
            qs=args["__ow_query"],
            keep_blank_values=True
        )

        self.l(INFO, "Headers: {}".format(self._headers))
        self.l(INFO, "Body: {}".format(self._body))
        self.l(INFO, "Request Path: {}".format(self._path))
        self.l(INFO, "Request Method: {}".format(self._method))
        self.l(INFO, "Request Query: {}".format(self._query))

        try:
            route = self._path_map[self._path[0]]
        except IndexError as e:
            return {"body": self.call_error(11)}
        except KeyError as e:
            return {"body": self.call_error(12, self._path[0])}

        controller = route(
            headers=self._headers,
            body=self._body,
            body_raw=self._body_raw,
            path=self._path,
            method=self._method,
            query=self._query,
            router=self
        )

        try:
            return {"body": await controller.entry_point()}
        except Exception as e:
            return {"body": self.call_error(5, e)}

    def call_error(self, error_code, *format_args):
        self.l(ERROR, self.ERROR_MAP[error_code].format(*format_args))
        return {
            "error_code": error_code,
            "error_msg": self.ERROR_MAP[error_code].format(*format_args)
        }
