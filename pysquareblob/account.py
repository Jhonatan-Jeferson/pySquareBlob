from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
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