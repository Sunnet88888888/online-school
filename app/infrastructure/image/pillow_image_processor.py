from PIL import Image
from io import BytesIO
from PIL import UnidentifiedImageError
from PIL.Image import DecompressionBombError
from app.application.protocols.image_processor import ImageProcessor
from app.application.exceptions import InvalidFileError

class PillowImageProcessor(ImageProcessor):

    def validate(self, stream: BytesIO) -> None:
        try:
            image = Image.open(stream)
            image.verify()
        except (
            UnidentifiedImageError,
            OSError,
            DecompressionBombError,
        ) as exc:
            raise InvalidFileError("Invalid or unsafe image") from exc
            