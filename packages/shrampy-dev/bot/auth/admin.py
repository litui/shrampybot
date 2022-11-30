import logging
from logging import DEBUG, WARN, ERROR, INFO
from auth.generic import GenericAuthenticator


class AdminAuthenticator(GenericAuthenticator):
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("AdminAuthenticator")
        self.l = logger.log
        self.l(INFO, "Initializing AdminAuthenticator")

        self.verify = self.entry_point
        super().__init__(*args, **kwargs)

    async def check_credentials(self):
        self.l(INFO, "Checking credentials...")
        header_token = self._headers.get("gsg-admin-token")
        authoritative_token = self._env.get("GSG_ADMIN_TOKEN")

        if not header_token:
            self.l(WARN, "Failed to find token in headers.")
            return False

        if not authoritative_token:
            self.l(WARN, "Failed to find authoritative token in config.")
            return False

        if header_token != authoritative_token:
            self.l(WARN, "Header token did not match authoritative token.")
            return False

        self.l(INFO, "Passed admin authentication check.")
        return True