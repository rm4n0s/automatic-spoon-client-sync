import json

import httpx
from pytsterrors import TSTError

from .exceptions import CreationError, ErrorField
from .inputs import AIModelUserInput
from .schemas import AIModelSchema


class AIModelCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_aimodels(self) -> list[AIModelSchema]:
        resp = httpx.get(self._host + "/api/v1/aimodels")
        if resp.status_code >= 400:
            raise TSTError(
                "failed-list-aimodels",
                "failed to list aimodels",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return [AIModelSchema(**item) for item in json_data]

    def get_aimodel(self, id: int) -> AIModelSchema:
        resp = httpx.get(self._host + "/api/v1/aimodels/" + str(id))
        if resp.status_code >= 400:
            raise TSTError(
                "failed-get-aimodel",
                f"failed to get aimodel with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return AIModelSchema.model_validate(json_data)

    def delete_aimodel(self, id: int):
        resp = httpx.delete(self._host + "/api/v1/aimodels/" + str(id))
        if resp.status_code >= 400:
            raise TSTError(
                "failed-delete-aimodel",
                f"failed to delete aimodel with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )

    def create_aimodel(self, input: AIModelUserInput) -> AIModelSchema:
        resp = httpx.post(self._host + "/api/v1/aimodels", json=input.model_dump())
        if resp.status_code >= 400:
            if resp.status_code == 400:
                error_dict = json.loads(resp.text)
                error_msg = error_dict["error"]
                errors_list = error_dict["error_per_field"]
                error_fields = [
                    ErrorField(error["field"], error["error"]) for error in errors_list
                ]
                raise CreationError("failed-create-aimodel", error_msg, error_fields)

            raise TSTError(
                "failed-unexpectedly-create-aimodel",
                "failed unexpectedly to create aimodel",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return AIModelSchema.model_validate(json_data)
