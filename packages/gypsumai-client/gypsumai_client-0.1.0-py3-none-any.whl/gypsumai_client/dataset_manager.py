from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from .models import (
    AddFileResponse,
    Dataset,
    DatasetCreate,
    DatasetList,
    DeleteResponse,
)

if TYPE_CHECKING:
    from .client import GypsumClient


class DatasetManager:
    def __init__(self, client: GypsumClient):
        self.client = client

    def list_datasets(self, project_id: str) -> DatasetList:
        """
        Retrieve all datasets available for a specific project.
        """
        response = self.client._request("GET", f"projects/{project_id}/datasets/")
        return DatasetList(datasets=[Dataset(**dataset) for dataset in response])

    def create_dataset(self, id: str, project_id: str, name: str) -> Dataset:
        """
        Create a new dataset within a specific project.
        """
        payload = DatasetCreate(id=id, name=name, project_id=project_id)
        response = self.client._request(
            "POST", f"projects/{project_id}/datasets/", json=payload.model_dump()
        )
        return Dataset(**response)

    def get_dataset(self, dataset_id: str, project_id: str) -> Dataset:
        """
        Retrieve details of a specific dataset by its ID and associated project ID.
        """
        response = self.client._request(
            "GET", f"projects/{project_id}/datasets/{dataset_id}/"
        )
        return Dataset(**response)

    def delete_dataset(self, dataset_id: str, project_id: str) -> DeleteResponse:
        """
        Delete a dataset by its ID and associated project ID.
        """
        response = self.client._request(
            "DELETE", f"projects/{project_id}/datasets/{dataset_id}/"
        )
        return DeleteResponse(**response)

    def add_files(
        self, project_id: str, dataset_id: str,
        files: List[str],  # List of file paths
        extract_tables: bool = False
    ) -> AddFileResponse:
        """
        Add files to a dataset and initiate an extraction job.

        Parameters:
            project_id (str): The project ID.
            dataset_id (str): The dataset ID.
            files (List[str]): A list of file paths to upload.
            extract_tables (bool): Whether to extract tables from the file

        Returns:
            AddFileResponse: The response mapping file names to their respective statuses.
        """
        # Construct the endpoint URL
        url = f"projects/{project_id}/datasets/{dataset_id}/add/"

        # Prepare multipart/form-data for files
        multipart_data = []
        for file_path in files:
            file_name = file_path.split("/")[-1]  # Extract file name from path
            try:
                # Open the file in binary mode and add to multipart_data
                multipart_data.append(
                    (
                        "files",
                        (
                            file_name,
                            open(file_path, "rb"),
                            "application/octet-stream",
                        ),
                    )
                )
            except FileNotFoundError as e:
                print(f"File not found: {file_path}")
                raise e

        payload = {"extract_tables": extract_tables}

        # Use the client's _request method to make the POST request
        response = self.client._request(
            "POST", url, files=multipart_data, data=payload
        )

        # Validate and return the response using the appropriate model
        return AddFileResponse.model_validate(response)

    def add_urls(
        self, project_id: str, dataset_id: str,
        urls: List[str],  # List of URLs
        extract_tables: bool = False
    ) -> AddFileResponse:
        """
        Add URLs to a dataset and initiate an extraction job.

        Parameters:
            project_id (str): The project ID.
            dataset_id (str): The dataset ID.
            urls (List[str]): A list of URLs to extract data from.
            extract_tables (bool): Whether to extract tables from the document
            

        Returns:
            AddFileResponse: The response mapping URLs to their respective statuses.
        """
        # Construct the endpoint URL
        url = f"projects/{project_id}/datasets/{dataset_id}/add/"

        # Prepare payload for URLs (convert list to comma-separated string)
        payload = {"urls": ",".join(urls), "extract_tables": extract_tables}

        # Use the client's _request method to make the POST request
        response = self.client._request("POST", url, data=payload)

        # Validate and return the response using the appropriate model
        return AddFileResponse.model_validate(response)
