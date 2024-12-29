"""This file contains the main interface to interact with Blob"""

from io import BytesIO, BufferedIOBase
import os

from .utils import *
from ._http import *
from .data import *


class Client:
    """Class that helps you interact with square cloud blob services

    Parameters
    ------------------
    api_key: str
        Your Square Cloud Api key

    clean_cache_timer: float
        This keyword-only argument sets the timer to clear object list cache of the class

    Property
    ------------------
    account_info: Account
        This property gets the account infos
    
    objects: list[Object]
        This property gets the objects list stored in Square Cloud Blob
        
    """
    
    __logger = Logger(debug=True)
    
    def __init__(
        self, api_key: str, *, clean_cache_timer: float=60,
        debug: bool=True, download_path: str='blobDownloads/'
    ):
        self.__http: HttpConnector = HttpConnector(api_key)
        self._cache: Cache = Cache(clean_cache_timer)
        self.__logger.debug = debug
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        self.download_path = download_path
    
    async def fetch_object_list(self) -> list[Object]:
        """Makes a request to the API to fetch and returns a list of objects.
        """
        
        endpoint = Endpoint.objects()
        self.__logger.info(f'Fetching objects in Square Cloud Blob from {endpoint}.')
        request: Response = await self.__http.make_request(endpoint)
        objects = request.response.get('objects', [])
        self.__logger.info(f'Found {len(objects)} objects in Square Cloud Blob')
        for item in objects:
            self._cache.objects.append(Object(**item))
        return self._cache.objects
    
    async def fetch_account_info(self) -> Account:
        """Makes a request to the API to fetch the account information
        
        The account info updates every two hours, so don't make too many requests"""
        
        endpoint = Endpoint.account_info()
        self.__logger.info(f'Fetching account info in Square Cloud Blob from {endpoint}.')
        request: Response = await self.__http.make_request(Endpoint.account_info())
        self._cache.account_info = Account(**request.response)
        return self._cache.account_info
    
    async def upload_object(
        self, name: str, file: str | BufferedIOBase | BytesIO,
        *, prefix: str = None, expire: int | None = None,
        auto_download: bool = True, security_hash: bool = False
    ) -> Response:
        """Uploads a file to the blob service
        
        Params
        ------------
        name: str
            The name of the file to upload(without extension). Must adhere to the a to z, A to Z, 0 to 9, and _ pattern.
        file: str | BufferedIOBase | BytesIO
            The file to upload. Must be a path to the file, or BytesIO or a BufferedIOBase.
        
        KEYWORD ONLY
        prefix: str
            The prefix of the object
        expire: int
            The expiration time of the object. The expiration period expressed in days, ranging from 1 to 365. if None, it will never expire.
        auto_download: bool
            If True, dowloads the file when access the URL.
        security_hash: bool
            Set to true if a security hash is required."""
        
        endpoint = Endpoint.upload()
        target_object: File = File(file)
        query = {
            "name": name,
            "auto_download": str(auto_download).lower(),
            "security_hash": str(security_hash).lower()
        }
        if prefix: 
            query.update({'prefix': prefix})
        if expire and (0 < expire <= 365): 
            query.update({'expire': expire})
        self.__logger.info(f'Uploading the file to Square Cloud Blob service on endpoint {endpoint}')
        request: Response = await self.__http.make_request(endpoint, file=target_object, params=query)
        return request
                
    async def delete_object(self, objects: Object | list[Object]) -> Response:
        """Delete an object from Square Cloud Blob
        
        Params
        ------------------
        objects: Object | list[Object]
            a single object or a list of objects that must be deleted from blob, this arg must be a single Object or a list of Objects like the property objects of this class
        
        Returns
        ---------------
        Response: The response of the deletion request"""

        endpoint = Endpoint.delete()
        if isinstance(objects, Object):
            objects = [objects]
        payload: dict[str, list[str]] = {"objects": [blob_object.id for blob_object in objects]}
        self.__logger.info(f'Deleting the object from Square Cloud Blob service on endpoint {endpoint}')
        request: Response = await self.__http.make_request(endpoint, json=payload)
        self._cache.objects = list(filter(lambda obj: obj.id not in objects, self._cache.objects))
        return request
    
    async def download_object(self, obj: Object) -> None:
        """This method downloads an object from Square Cloud Blob and saves it on the directory specified on this
        class instance. If not specified, the object will be downloaded and stored in `root/blobDownloads` 
        
        Params
        -----------------
        obj: Object
            The object to be downloaded. Use one object from the property `objects`.
        """
        
        session = self.__http.session
        self.__logger.info(f'Downloading object from {obj.url}')
        async with session() as http:
            async with http.get(obj.url) as response:
                if response.status == 200:
                    self.__logger.info(f'Object download status code: {response.status}')
                    content: bytes = await response.content.read()
                    path: str = self.download_path+obj.id.split('/')[-1]
                    with open(path, 'wb') as file:
                        file.write(content)
                    self.__logger.info(f'Downloaded object and saved in {path}')
                else:
                    self.__logger.warning(f'Failed to download object from {obj.url}. Status code: {response.status}')
        
    @property
    async def account_info(self) -> Account:
        """Gets the account info
        
        First checks if has account info in cache, if not makes an request"""
        if not self._cache.account_info:
            return await self.fetch_account_info()
        return self._cache.account_info
    
    @property
    async def objects(self) -> list[Object]:
        """Get all objects stored in blob.
        
        First checks if has objects in cache, if not makes an request"""
        
        if len(self._cache.objects) == 0:
            return await self.fetch_object_list()
        return self._cache.objects
        