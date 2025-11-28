import httpx

from .inputs import EngineUserInput
from .schemas import EngineSchema


class EngineCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_engines(self) -> list[EngineSchema]:
        resp = httpx.get(self._host + "/api/v1/engines")
        _ = resp.raise_for_status()
        json_data = resp.json()
        return [EngineSchema(**item) for item in json_data]

    def get_engine(self, id: int) -> EngineSchema:
        resp = httpx.get(self._host + "/api/v1/engines/" + str(id))
        _ = resp.raise_for_status()
        json_data = resp.json()
        return EngineSchema.model_validate(json_data)

    def delete_engine(self, id: int):
        resp = httpx.delete(self._host + "/api/v1/engines/" + str(id))
        _ = resp.raise_for_status()

    def create_engine(self, input: EngineUserInput) -> EngineSchema:
        resp = httpx.post(self._host + "/api/v1/engines", json=input.model_dump())
        _ = resp.raise_for_status()
        json_data = resp.json()
        return EngineSchema.model_validate(json_data)
