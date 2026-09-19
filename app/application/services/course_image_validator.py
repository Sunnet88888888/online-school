from pathlib import Path

from app.application.exceptions import InvalidFileExtensionError, InvalidFileMimeTypeError


class ImageValidationService:
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
    ALLOWED_MIME_TYPES = {
        "image/jpeg",
        "image/png",
    }

    async def validate(
        self,
        filename: str | None,
        content_type: str | None,
    ) -> None:
        extension = Path(filename or "").suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise InvalidFileExtensionError(
                f"Unsupported image extension: {extension}"
            )

        if content_type not in self.ALLOWED_MIME_TYPES:
            raise InvalidFileMimeTypeError(
                f"Unsupported MIME type: {content_type}"
            )