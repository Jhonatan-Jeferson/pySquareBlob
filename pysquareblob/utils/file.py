"""This module contains the file implementation for validate the inputed file"""

from io import BytesIO, BufferedIOBase, BufferedReader
import os
import sys


class File:
    """Represents a file in the Square Blob Storage service"""
    
    def __init__(self, file: bytes | str | BufferedIOBase) -> None:
        self.__validate_size(file)
        if isinstance(file, BufferedIOBase):
            if not file.seekable() and file.readable():
                raise ValueError(
                    f'File buffer {file!r} must be seekable and readable'
                )
            self.bytes: BufferedIOBase = file
        elif isinstance(file, bytes):
            self.bytes: BytesIO = BytesIO(file)
        else:
            self.__validate_type(file)
            self.bytes = open(file, 'rb')
            
            
    def __validate_size(self, file: str | BytesIO | BufferedIOBase) -> None:
        """Check if the file size is within the allowed range
        
        Params
        ------------
        file: str | BytesIO | BufferedIOBase
        
        Raises
        ------------
        """
        
        if isinstance(file, (BytesIO, BufferedIOBase)):
            size: int = sys.getsizeof(file)
        else:
            size: int = os.path.getsize(file)
        if 104_857_600 < size:
            raise ValueError('File size must be between 1KB and 100MB')
        elif size < 1024:
            raise ValueError('File size must be at least 1KB')
            
    def __validate_type(self, path: str) -> None:
        """Validate that the file is a valid file type
        
        Params
        ------------
        path: str
            The file path to validate if is a valid file type
            
        Raises
        ------------
        """
        
        extension: str = path.split('.')[-1]
        allowed: tuple[str] = (
            'mp4', 'mpeg', 'webm', 'flv', 'm4v',
            'jpeg', 'jpg', 'png', 'apng', 'tiff', 'gif',
            'webp', 'bmp', 'svg', 'ico', 'cur',
            'heic', 'heif', 'mp3', 'mp4', 'wav',
            'ogg', 'opus', 'mpeg', 'aac', 'txt',
            'html', 'css', 'csv', 'x-sql', 'xml',
            'sql', 'x-sql', 'sqlite3', 'pdf', 'json',
            'js', 'p12'
        )
        if extension not in allowed:
            
            raise ValueError(f'Invalid file type: {extension}')