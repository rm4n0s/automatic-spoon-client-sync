import httpx
from pytsterrors import TSTError

from .inputs import JobUserInput
from .schemas import JobSchema


class JobCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def get_list_jobs(self) -> list[JobSchema]:
        resp = httpx.get(self._host + "/api/v1/jobs")
        if resp.status_code >= 400:
            raise TSTError(
                "failed-get-list-jobs",
                "failed to get list of jobs",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return [JobSchema(**item) for item in json_data]

    def get_job(self, id: int) -> JobSchema:
        resp = httpx.get(self._host + "/api/v1/jobs/" + str(id))
        if resp.status_code >= 400:
            raise TSTError(
                "failed-get-job",
                f"failed to get job with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return JobSchema.model_validate(json_data)

    def delete_job(self, id: int):
        resp = httpx.delete(self._host + "/api/v1/jobs/" + str(id))
        if resp.status_code >= 400:
            raise TSTError(
                "failed-delete-job",
                f"failed to delete job with id {id}",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )

    def create_job(self, input: JobUserInput) -> JobSchema:
        resp = httpx.post(self._host + "/api/v1/jobs", json=input.model_dump())
        if resp.status_code >= 400:
            raise TSTError(
                "failed-create-job",
                "failed to create job",
                metadata={"content": resp.text, "http_status": resp.status_code},
            )
        json_data = resp.json()
        return JobSchema.model_validate(json_data)
