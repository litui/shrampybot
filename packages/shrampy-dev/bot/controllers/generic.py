from os import environ


class GenericController:
    def __init__(self, headers, body, path, method, router, query, body_raw):
        self._env = environ
        self._headers = headers
        self._body = body
        self._body_raw = body_raw
        self._path = path
        self._method = method
        self._query = query
        self._router = router

    async def _call_appropriate_function(self):
        """Inherited coroutine that maps the method and path
        to a function call on self."""
        path = self._path[0] if not len(self._path) > 1 \
            else "{}_{}".format(self._path[0], self._path[1])

        func = getattr(self, "_{}__{}".format(self._method, path))
        return await func()

    async def entry_point(self):
        """Generic entry point"""
        return await self._call_appropriate_function()