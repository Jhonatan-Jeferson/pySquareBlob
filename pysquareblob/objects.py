from pysquareblob.utils.logs import logs


class Object:

    """Represents the Object stored on blob user's account
    Properties
    -------------------------
    id: str
        The id of the object.
    size: int
        The size of the object in bytes.
    created_at: str
        The date and time the object was created.
    expires_at: str
        The date and time the object will expire.
    """


    def __init__(self, **kwargs) -> None:
        
        self._id: str = kwargs.get("id", "")
        self._size: int = kwargs.get("size", 0)
        self._created_at: str = kwargs.get("created_at", "")
        self._expires_at: str = kwargs.get("expires_at", "")

    def __repr__(self) -> str:
        
        return f"Object(id={self.id} , size={self.size/1000}KB)"

    @property
    def id(self) -> str:

        return self._id
    
    @property
    def size(self) -> int:

        return self._size
    
    @property
    def created_at(self) -> str:

        return self._created_at
    
    @property
    def expires_at(self) -> str:

        return self._expires_at