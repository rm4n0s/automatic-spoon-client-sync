import httpx
from pytsterrors import TSTError

from .schemas import ImageSchema


class ImageCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_images(self) -> list[ImageSchema]:
        resp = httpx.get(self._host + "/api/v1/images")
        if resp.status_code >= 400:
            raise TSTError(
                "failed-list-images",
                "failed to list images",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return [ImageSchema(**item) for item in json_data]

    def get_image(self, id: int) -> ImageSchema:
        resp = httpx.get(self._host + "/api/v1/images/" + str(id))
        if resp.status_code >= 400:
            raise TSTError(
                "failed-get-image",
                f"failed to get image with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return ImageSchema.model_validate(json_data)

    def download_image(self, id: int, file_path: str) -> None:
        with httpx.Client() as client:
            with client.stream(
                "GET", self._host + "/api/v1/images/" + str(id) + "/show"
            ) as response:
                if response.status_code >= 400:
                    raise TSTError(
                        "failed-download-image",
                        f"failed to download image with id {id}",
                        metadata={
                            "content": response.text,
                            "http_status": response.status_code,
                        },
                    )
                with open(file_path, "wb") as f:
                    for chunk in response.iter_bytes(
                        chunk_size=8192
                    ):  # Adjust chunk_size as needed
                        f.write(chunk)
