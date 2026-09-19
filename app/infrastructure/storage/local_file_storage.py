from pathlib import Path
from uuid import uuid4


class LocalFileStorage:

    def __init__(self) -> None:
        self.upload_dir = Path(__file__).resolve().parents[3] / "uploaded_media"
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save(
        self,
        data: bytes,
        extension: str,
    ) -> str:
        filename = f"{uuid4()}{extension}"
        file_path = self.upload_dir / filename

        file_path.write_bytes(data)

        return filename