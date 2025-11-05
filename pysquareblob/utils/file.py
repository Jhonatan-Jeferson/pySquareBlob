"""This module contains the file implementation for validate the inputed file"""

from io import BytesIO, BufferedIOBase, BufferedReader
import os
import sys


class File:
    """Represents a file in the Square Blob Storage service"""
    
    def __init__(self, file: bytes | str | BufferedIOBase | BytesIO, mime: str|None=None) -> None:
        if isinstance(file, BufferedIOBase) or isinstance(file, BytesIO):
            if not file.seekable() and not file.readable():
                raise ValueError(
                    f'File buffer {file!r} must be seekable and readable'
                )
            self.bytes: bytes = file.read()
        elif isinstance(file, bytes):
            self.bytes = file
        else:
            file_opened = open(file, 'rb')
            self.bytes: bytes = file_opened.read()
            file_opened.close()
            file_mime = self.__validate_type(file)
            if not mime: 
                mime = file_mime
        self.__validate_size(self.bytes)
        self._mimetype: str|None = mime or self.mimetype
        
    @property
    def mimetype(self) -> str:
        """Get the mimetype of the file
        
        Returns
        ------------
        str
            The mimetype of the file
        """
        if self._mimetype: 
            return self._mimetype
        elif isinstance(self.bytes, bytes):
            content = BytesIO(self.bytes)
            mimetypes_bytes: dict[bytes, str] = {
                b'\x89PNG\r\n\x1a\n': 'image/png',
                b'\xff\xd8\xff': 'image/jpeg',
                b'GIF87a': 'image/gif',
                b'GIF89a': 'image/gif',
                b'%PDF-': 'application/pdf',
                b'BM': 'image/bmp',
                b'II*\x00': 'image/tiff',
                b'MM\x00*': 'image/tiff',
                b'\x00\x00\x01\x00': 'image/x-icon',
                b'\x1A\x45\xDF\xA3': 'video/webm', 
                b'ID3': 'audio/mpeg',
                b'OggS': 'audio/ogg',
                b'SQLite format 3\x00': 'application/x-sqlite3'
            }
            for byt, mime in mimetypes_bytes.items():
                content.seek(0)
                file_start = content.read(len(byt))
                if file_start == byt:
                    return mime
        raise ValueError('Could not determine the mimetype of the file')
 
    def __validate_size(self, file: bytes) -> None:
        """Check if the file size is within the allowed range
        
        Params
        ------------
        file: str | BytesIO | BufferedIOBase
        
        Raises
        ------------
        """
        size: int = len(file)
        if 104_857_600 < size:
            raise ValueError('File size must be between 1KB and 100MB')
        elif size < 1024:
            raise ValueError('File size must be at least 1KB')
            
    def __validate_type(self, path: str) -> str:
        """Validate that the file is a valid file type
        
        Params
        ------------
        path: str
            The file path to validate if is a valid file type
            
        Raises
        ------------
        """
        
        extension: str = path.split('.')[-1]
        mimetypes: dict[str, str] = {
                'mp4': 'video/mp4', 'mpeg': 'video/mpeg',
                'webm': 'video/webm', 'flv': 'video/x-flv',
                'm4v': 'video/x-m4v', 'jpeg': 'image/jpeg',
                'jpg': 'image/jpeg', 'png': 'image/png',
                'apng': 'image/apng', 'tiff': 'image/tiff',
                'gif': 'image/gif', 'webp': 'image/webp',
                'bmp': 'image/bmp','svg': 'image/svg+xml',
                'ico': 'image/vnd.microsoft.icon', 'cur': 'image/x-icon',
                'heic': 'image/heic', 'heif': 'image/heif',
                'mp3': 'audio/mpeg', 'wav': 'audio/wav',
                'ogg': 'audio/ogg', 'opus': 'audio/opus',
                'aac': 'audio/aac', 'txt': 'text/plain',
                'html': 'text/html', 'css': 'text/css',
                'csv': 'text/csv', 'x-sql': 'application/x-sql',
                'xml': 'application/xml', 'sql': 'application/x-sql',
                'sqlite3': 'application/x-sqlite3', 'pdf': 'application/pdf',
                'json': 'application/json', 'js': 'application/javascript',
                'p12': 'application/x-pkcs12'
        }
        if not (mime := mimetypes.get(extension)):
            raise ValueError(f'Invalid file type: {extension}')
        return mime