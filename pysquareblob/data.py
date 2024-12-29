"""This file contains all dataclasses """

from dataclasses import dataclass


__all__ = ['Account', 'Object']

@dataclass(frozen=True)
class Account:
    """Represents the account status of an user
    Parameters
    ----------------
    file_count: int
        The total number of objects in your account.

    storage_occupied: int
        The total size of all objects in your account, in bytes.

    price: int
        The total price of storage for all objects in your account, in BRL.

    objects_price: int
        The total price of all objects in your account, in BRL.

    total:
        The total price of all objects in your account, in BRL.
    """

    objects: int
    size: int
    storagePrice: int
    objectsPrice: int
    totalEstimate: int


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
    def url(self) -> str:
        
        return f"https://public-blob.squarecloud.dev/{self._id}"

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