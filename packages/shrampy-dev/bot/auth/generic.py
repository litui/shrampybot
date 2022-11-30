from controllers.generic import GenericController


class GenericAuthenticator(GenericController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def entry_point(self):
        pass

    async def check_credentials(self):
        return False