from __future__ import annotations
from typing import TYPE_CHECKING
from .models import DeleteResponse, ProjectCreate, Project, ProjectList

if TYPE_CHECKING:
    from .client import GypsumClient


class ProjectManager:
    def __init__(self, client: GypsumClient):
        self.client = client

    def list_projects(self) -> ProjectList:
        """
        Retrieve all projects available for the tenant.
        """
        response = self.client._request("GET", "projects/")
        return ProjectList(projects=[Project(**project) for project in response])

    def create_project(self, id: str, name: str) -> Project:
        """
        Create a new project with a specified name and ID.
        """
        payload = ProjectCreate(name=name, id=id)
        response = self.client._request("POST", "projects/", json=payload.model_dump())
        return Project(**response)

    def get_project(self, project_id: str) -> Project:
        """
        Retrieve details of a specific project by its project ID.
        """
        response = self.client._request("GET", f"projects/{project_id}/")
        return Project(**response)

    def delete_project(self, project_id: str) -> DeleteResponse:
        """
        Delete a project by its project ID.
        """
        response = self.client._request("DELETE", f"projects/{project_id}/")
        return DeleteResponse(**response)
