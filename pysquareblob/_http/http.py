import aiohttp
from typing import Any, Literal

from .endpoints import Endpoint
from ..utils import Logger

 
class Response:
    """This is the response of api
    
    Parameters
    ------------
    json: dict[str, Any]
        The response json
    endpoint: Endpoint
        The endpoint used to make the request
    status_code: int
        The response status code
        
    Attributes
    ------------------
    _data: dict[str, Any]
        All the response json
    endpoint: Endpoint
        The endpoint used to make the request
    status: str
        If was succeded or if was a error.
    status_code: int
        The response status code
    """
    __logger = Logger(True)
    
    def __init__(self, json: dict[str, Any], endpoint: Endpoint, status_code: int) -> None:
        self._data = json
        self.endpoint = endpoint
        self.response: list[dict[str, Any]]|dict[str,int]|dict[str] = self._data.get('response', None)
        self.status: Literal['success', 'error'] = self._data.get('status')
        self.status_code = status_code
        self.__check_for_errors()
        
    def __repr__(self) -> str:
        """Representation of the response"""
        return f'{self.__class__}(endpoint={self.endpoint}, status_code={self.status_code})'
    
    def __check_for_errors(self):
        """Checks if the response has an error"""
        if self.status == 'error':
            error = self._data.get("code")
            self.__logger.warning(f'Error occurred during request: {error}')
            if error == 'ACCESS_DENIED':
                self.__logger.warning(f'Check if your API key is valid')
            elif error == 'INVALID_OBJECT_NAME':
                self.__logger.warning(f'Check if the object name or prefix is valid')
            elif error == 'TOO_MANY_OBJECTS':
                self.__logger.warning(f'Too many objects to exclude')
            elif error == 'FAILED_DELETE':
                self.__logger.warning(f'Failed to delete the object')
        
    


class HttpConnector:
    """This is the connection representation
    
    Parameters
    ------------
    api_key: str
        Square Cloud API key"""
    
    def __init__(self, api_key: str) -> None:
        self.session = aiohttp.ClientSession
        self.__api_key = api_key
        
    async def make_request(self, endpoint: Endpoint, **kwargs) -> Response:
        """Makes a request to the given endpoint
        
        Parameters
        ----------------
        endpoint: Endpoint
            The endpoint to make a request to
        kwargs: dict
            The additional keyword arguments to make a request
            
        Returns
        ----------------
        Response: The response of the request      
        """
        
        headers = {
            'Authorization': self.__api_key
        }
        if endpoint == Endpoint.upload():
            data = aiohttp.FormData()
            data.add_field('file', kwargs.pop('file').bytes)
            kwargs['data'] = data
        async with self.session() as http:
            async with http.request(endpoint.method, str(endpoint), headers=headers, **kwargs) as response:
                return Response(await response.json(), endpoint, response.status)