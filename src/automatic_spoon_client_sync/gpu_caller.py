import httpx
from pytsterrors import TSTError

from .schemas import GPUSchema


class GPUCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_gpus(self) -> list[GPUSchema]:
        resp = httpx.get(self._host + "/api/v1/gpus")
        if resp.status_code >= 400:
            raise TSTError(
                "failed-list-gpus",
                "failed to list gpus",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return [GPUSchema(**item) for item in json_data]
