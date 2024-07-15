from .connector import Connector
from .account import Account
from .objects import Object
from .utils.logs import logs
from asyncio import sleep, get_event_loop, create_task

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

    def __init__(self, api_key: str, *, clean_cache_timer: float=300):

        self.__connection = Connector({"Authorization": api_key})
        self.cached = {
            "account": None,
            "objects": None
        }
        self._cache_clear = get_event_loop().call_later(clean_cache_timer, create_task, self.__clean_cache())

    @logs(message="Limpando cache")
    async def __clean_cache(self):

        self.cached = {
            "account": None,
            "objects": None
        }

    @logs(message="requesting objects list at: https://blob.squarecloud.app/v1/objects")
    async def _object_list(self) -> list[Object]:

        """Request the objects list
        DO NOT USE THIS METHOD, INSTEAD USE \"objects\" property to get objects list doing requests only when necessary"""

        json = await self.__connection.make_request('objects', 'get')
        resp: dict = json.get("response")
        objects = []
        for _object in resp.get("objects", []):
            objects.append(Object(**_object))
        self.cached["objects"] = objects
        return objects
        # async with self._connection(headers=self.__headers) as http:
        #     url = "https://blob.squarecloud.app/v1/objects"
        #     async with http.get(url) as req:
        #         json: dict = await req.json()
        #         resp: dict = json.get("response", None)
        #         objects: list[Object] = []
        #         for _object in resp.get("objects", []):
        #             objects.append(Object(**_object))
        #         self.cached["objects"] = objects
        #         return objects
            
    @logs(message="requesting account info at: https://blob.squarecloud.app/v1/account/stats")
    async def _get_account_infos(self) -> Account:

        """Requests the account info of an user
        DO NOT USE THIS METHOD, instead use \"account_info\" property to get accounts info doing requests only when necessary"""

        json = await self.__connection.make_request('account', 'get')
        resp: dict = json.get("response", None)
        acc = Account(**resp)
        self.cached["account"] = acc
        return acc
        # async with self._connection(headers=self.__headers) as http:
        #     url = "https://blob.squarecloud.app/v1/account/stats"
        #     async with http.get(url) as req:
        #         json: dict = await req.json()
        #         resp = json.get("response", None)
        #         acc = Account(**resp)
        #         self.cached["account"] = acc
        #         return acc
        
    @property
    @logs(message="getting account info, first trying to get cached info")
    async def account_info(self) -> Account:

        """Account infos"""

        res = self.cached.get("account")
        if not isinstance(res, Account): res = await self._get_account_infos()
        return res
    
    @property
    @logs(message="getting object info, first trying to get cached objects")
    async def objects(self) -> list[Object]:

        res = self.cached.get("objects")
        if not isinstance(res, list): res = await self._object_list()
        return res

    @logs(message="trying to upload a object, request post at: https://blob.squarecloud.app/v1/objects")
    async def upload_object(
        self, path: str, name: str, 
        *, prefix: str|None=None, expire: int|None=None, 
        auto_download: bool=True, 
        security_hash: bool=False
    ) -> dict[str, str|int]:

        """Upload a object/file to blob storage
        Params
        ---------------------------------------
        path: str
            the path to the target object
        
        name: str
            the name the object will have on blob

        KEYWORD-ONLY ARGS
        prefix: str
            if the object must have a prefix, pass this arg
        
        expire: int
            if the object must expire/deleted after some time, pass it in days
        
        auto_download: bool
            if someone access the link to the object it will be automatically downloaded

        security_hash: bool
            if the object must have a security hash
        """

        with open(path, "rb") as target_file:
            payload = {"file": target_file}
            query = {"name": name}
            query.update({"auto_download": "true"}) if auto_download else query.update({"auto_download": "false"})
            query.update({"security_hash": "true"}) if security_hash else query.update({"security_hash": "false"})
            if prefix is not None: query.update({"prefix": prefix})
            if expire is not None and (expire > 0 and expire <= 365): query.update({"expire": expire})

            json = await self.__connection.make_request('objects', 'post', data=payload, params=query)
            resp = json.get("response", None)
            return resp
        # async with self._connection(headers=self.__headers) \
        # as http:
        #     url = "https://blob.squarecloud.app/v1/objects"
        #     payload = {"file": {}}
        #     query = {"name": name}
        #     query.update({"auto_download": "true"}) if auto_download else query.update({"auto_download": "false"})
        #     query.update({"security_hash": "true"}) if security_hash else query.update({"security_hash": "false"})
        #     if prefix is not None: query.update({"prefix": prefix})
        #     if expire is not None and (expire > 0 and expire <= 365): query.update({"expire": expire})
        #     with open(path, "rb") as file:
        #         payload = {"file": file}
        #         async with http.post(url, data=payload, params=query) as req: 
        #             json: dict = await req.json()
        #             res = json.get("response", None)
        #             return res

    @logs(message="request delete at: https://blob.squarecloud.app/v1/objects")
    async def delete_object(self, object_list: list[Object]) -> dict[str, str]: 

        """Delete an object from Square Cloud Blob
        Params
        ------------------------------------------
        object_list: list[Object]
            a list of objects that must be deleted from blob, this arg must be a list of Objects like the property objects of this class
        """

        

        payload = {"objects": []}
        for _object in object_list:
            payload["objects"].append(_object.id)

        json = await self.__connection.make_request('objects', 'delete', json=payload)
        resp = json.get("status")
        return resp

        # async with self._connection(headers=self.__headers) as http:
        #     url = "https://blob.squarecloud.app/v1/objects"
        #     async with http.delete(url, json=payload) as req:
        #         json: dict = await req.json()
        #         resp = json.get("status")
        #         return resp
