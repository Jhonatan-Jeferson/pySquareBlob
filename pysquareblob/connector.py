from aiohttp import ClientSession


class Connector:

    """This class represents connector"""

    URLS = {
        "ACCOUNT": "https://blob.squarecloud.app/v1/account/stats",
        "OBJECTS": "https://blob.squarecloud.app/v1/objects"
    }


    def __init__(self, headers: dict[str, str]) -> None:

        self.__headers = headers
        self.__connection = ClientSession

    async def make_request(self, target: str, method: str, **kwargs) -> dict:

        """Open a context manager of connector and make the request"""

        async with self.__connection(headers=self.__headers) as http:
            url = self.URLS.get(target.upper(), False)
            async with http.request(method.upper(), url, **kwargs) as req:
                json_response: dict = await req.json()
                return json_response