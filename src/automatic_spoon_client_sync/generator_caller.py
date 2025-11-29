import httpx

from .inputs import GeneratorUserInput
from .schemas import GeneratorSchema


class GeneratorCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_generators(self) -> list[GeneratorSchema]:
        resp = httpx.get(self._host + "/api/v1/generators")
        _ = resp.raise_for_status()
        json_data = resp.json()
        return [GeneratorSchema(**item) for item in json_data]

    def get_generator(self, id: int) -> GeneratorSchema:
        resp = httpx.get(self._host + "/api/v1/generators/" + str(id))
        _ = resp.raise_for_status()
        json_data = resp.json()
        return GeneratorSchema.model_validate(json_data)

    def start_generator(self, id: int) -> GeneratorSchema:
        resp = httpx.patch(self._host + "/api/v1/generators/" + str(id) + "/start")
        _ = resp.raise_for_status()
        json_data = resp.json()
        return GeneratorSchema.model_validate(json_data)

    def close_generator(self, id: int) -> GeneratorSchema:
        resp = httpx.patch(self._host + "/api/v1/generators/" + str(id) + "/close")
        _ = resp.raise_for_status()
        json_data = resp.json()
        return GeneratorSchema.model_validate(json_data)

    def delete_generator(self, id: int):
        resp = httpx.delete(self._host + "/api/v1/generators/" + str(id))
        _ = resp.raise_for_status()

    def create_generator(self, input: GeneratorUserInput) -> GeneratorSchema:
        resp = httpx.post(self._host + "/api/v1/generators", json=input.model_dump())
        _ = resp.raise_for_status()
        json_data = resp.json()
        return GeneratorSchema.model_validate(json_data)
