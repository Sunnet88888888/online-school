from dataclasses import dataclass, field
from io import BytesIO
from uuid import UUID


@dataclass
class UploadedFile:
    filename: str
    content_type: str | None
    stream: BytesIO
    
    
@dataclass
class ValidatedImage:
    data: bytes
    format: str
    width: int
    height: int