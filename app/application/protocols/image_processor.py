from typing import Protocol


class ImageProcessor(Protocol):
    
    def validate(self, data_bytes: bytes) -> None :
        pass
    