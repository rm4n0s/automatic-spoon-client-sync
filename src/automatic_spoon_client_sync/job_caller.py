import httpx

from .inputs import JobUserInput
from .schemas import JobSchema


class JobCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_jobs(self) -> list[JobSchema]:
        resp = httpx.get(self._host + "/api/v1/jobs")
        _ = resp.raise_for_status()
        json_data = resp.json()
        return [JobSchema(**item) for item in json_data]

    # def get_job(self, id: int) -> JobSchema:
    #     resp = httpx.get(self._host + "/api/v1/jobs/" + str(id))
    #     _ = resp.raise_for_status()
    #     json_data = resp.json()
    #     return JobSchema.model_validate(json_data)

    def delete_job(self, id: int):
        resp = httpx.delete(self._host + "/api/v1/jobs/" + str(id))
        _ = resp.raise_for_status()

    def create_job(self, input: JobUserInput) -> JobSchema:
        resp = httpx.post(self._host + "/api/v1/jobs", json=input.model_dump())
        _ = resp.raise_for_status()
        json_data = resp.json()
        return JobSchema.model_validate(json_data)
