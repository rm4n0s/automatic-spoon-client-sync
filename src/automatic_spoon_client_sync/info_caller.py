import httpx
from pytsterrors import TSTError

from .schemas import InfoSchema


class InfoCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_info(self) -> InfoSchema:
        resp = httpx.get(self._host + "/api/v1/info")
        if resp.status_code >= 400:
            raise TSTError(
                "failed-get-info",
                "failed to get info",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return InfoSchema.model_validate(json_data)
