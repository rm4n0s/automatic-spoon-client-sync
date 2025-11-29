import httpx
from pytsterrors import TSTError

from .inputs import EngineUserInput
from .schemas import EngineSchema


class EngineCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_engines(self) -> list[EngineSchema]:
        resp = httpx.get(self._host + "/api/v1/engines")
        if resp.status_code >= 400:
            raise TSTError(
                "failed-list-engines",
                "failed to list engines",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return [EngineSchema(**item) for item in json_data]

    def get_engine(self, id: int) -> EngineSchema:
        resp = httpx.get(self._host + "/api/v1/engines/" + str(id))
        if resp.status_code >= 400:
            raise TSTError(
                "failed-get-engine",
                f"failed to get engine with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return EngineSchema.model_validate(json_data)

    def delete_engine(self, id: int):
        resp = httpx.delete(self._host + "/api/v1/engines/" + str(id))
        if resp.status_code >= 400:
            raise TSTError(
                "failed-delete-engine",
                f"failed to delete engine with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )

    def create_engine(self, input: EngineUserInput) -> EngineSchema:
        resp = httpx.post(self._host + "/api/v1/engines", json=input.model_dump())
        if resp.status_code >= 400:
            raise TSTError(
                "failed-create-engine",
                "failed to create engine",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return EngineSchema.model_validate(json_data)
