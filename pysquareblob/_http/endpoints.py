class Endpoint:
    """This class represents an Blob API endpoint.
    
    Parameters
    ------------------
    name: str
        The name of the endpoint. Must be one of the keys in the ENDPOINTS dictionary.
    
    Attributes
    ------------------
    name: str
    method: str
    path: str
    """
    
    ENDPOINTS: dict[str, dict[str, str]] = {
        'ACCOUNT_INFO': {'method': 'GET', 'path': 'account/stats'},
        'LIST_OBJECTS': {'method': 'GET', 'path': 'objects'},
        'UPLOAD_OBJECTS': {'method': 'POST', 'path': 'objects'},
        'DELETE_OBJECTS': {'method': 'DELETE', 'path': 'objects'}
    }
    VERSION: str = 'v1'
    
    def __init__(self, name: str) -> None:
        if not (endpoint := self.ENDPOINTS.get(name)):
            raise ValueError(f"Invalid endpoint: {name}")
        self.name: str = name
        self.method: str = endpoint['method']
        self.path: str = endpoint['path']
        
    def __repr__(self) -> str:
        """Representation of Endpoint object"""
        
        return f"https://blob.squarecloud.app/{self.VERSION}/{self.path}"
    
    def __eq__(self, other: 'Endpoint') -> bool:
        """
        Compare two Endpoint instances for equality.

        Parameters
        ------------------
        other: Endpoint
            The endpoint to compare
        
        Returns
        ------------------
        bool: True if both instances have the same name, otherwise False.
        """
        
        return isinstance(other, Endpoint) and self.name == other.name
        
    @classmethod
    def account_info(cls) -> 'Endpoint':
        """Returns the endpoint to get the account info
        
        Returns
        ---------
        Endpoint: The endpoint to get the account info"""
        
        return cls("ACCOUNT_INFO")
    
    @classmethod
    def objects(cls) -> 'Endpoint':
        """Returns the endpoint to get the objects stored in blob
        
        Returns
        ---------
        Endpoint: The endpoint to get the objects stored in blob"""
        
        return cls("LIST_OBJECTS")
    
    @classmethod
    def upload(cls) -> 'Endpoint':
        """Returns the endpoint to upload an object to blob
        
        Returns
        ---------
        Endpoint: The endpoint to upload an object to blob"""
        
        return cls("UPLOAD_OBJECTS")
    
    @classmethod
    def delete(cls) -> 'Endpoint':
        """Returns the endpoint to delete an object from blob
        
        Returns
        ---------
        Endpoint: The endpoint to delete an object from blob"""
        
        return cls("DELETE_OBJECTS")
    
    
