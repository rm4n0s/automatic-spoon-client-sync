import httpx
from pytsterrors import TSTError

from .inputs import GeneratorUserInput
from .schemas import GeneratorSchema


class GeneratorCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_generators(self) -> list[GeneratorSchema]:
        resp = httpx.get(self._host + "/api/v1/generators")
        if resp.status_code >= 400:
            raise TSTError(
                "failed-list-generators",
                "failed to get list of generators",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return [GeneratorSchema(**item) for item in json_data]

    def get_generator(self, id: int) -> GeneratorSchema:
        resp = httpx.get(self._host + "/api/v1/generators/" + str(id))
        if resp.status_code >= 400:
            raise TSTError(
                "failed-get-generator",
                f"failed to get generator with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return GeneratorSchema.model_validate(json_data)

    def start_generator(self, id: int) -> GeneratorSchema:
        resp = httpx.patch(self._host + "/api/v1/generators/" + str(id) + "/start")
        if resp.status_code >= 400:
            raise TSTError(
                "failed-start-generator",
                f"failed to start generator with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return GeneratorSchema.model_validate(json_data)

    def close_generator(self, id: int) -> GeneratorSchema:
        resp = httpx.patch(self._host + "/api/v1/generators/" + str(id) + "/close")
        if resp.status_code >= 400:
            raise TSTError(
                "failed-close-generator",
                f"failed to close generator with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return GeneratorSchema.model_validate(json_data)

    def delete_generator(self, id: int):
        resp = httpx.delete(self._host + "/api/v1/generators/" + str(id))
        if resp.status_code >= 400:
            raise TSTError(
                "failed-delete-generator",
                f"failed to delete generator with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )

    def create_generator(self, input: GeneratorUserInput) -> GeneratorSchema:
        resp = httpx.post(self._host + "/api/v1/generators", json=input.model_dump())
        if resp.status_code >= 400:
            raise TSTError(
                "failed-create-generator",
                "failed to create generator",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return GeneratorSchema.model_validate(json_data)
