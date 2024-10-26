from __future__ import annotations
import os
import time
from typing import TYPE_CHECKING, Optional, Any, Dict
from .models import GsDocumentModel, JobStatusCode, JobStatusResponse

if TYPE_CHECKING:
    from .client import GypsumClient
    from .dataset_manager import DatasetManager


class DocumentManager:
    def __init__(self, client: GypsumClient, dataset_manager: DatasetManager):
        self.client = client
        self.dataset_manager = dataset_manager

    def get_extraction_status(
        self, project_id: str, dataset_id: str, document_id: str
    ) -> JobStatusResponse:
        """
        Retrieve the extraction status of a document processing job.

        Args:
            project_id (str): Unique ID for the project containing the dataset.
            dataset_id (str): Unique ID for the dataset.
            document_id (str): Unique ID for the document.

        Returns:
            JobStatusResponse: Contains job status, error code, and error message.
        """
        url = f"projects/{project_id}/datasets/{dataset_id}/documents/{document_id}/status/"
        params = {"type": "extraction"}  # Specifically for extraction job status

        response = self.client._request("GET", url, params=params)

        return JobStatusResponse(**response)

    def get_extracted_elements(
        self, project_id: str, dataset_id: str, document_id: str
    ) -> GsDocumentModel:
        """
        Retrieve the extracted elements of a document.

        Args:
            project_id (str): Unique ID for the project containing the dataset.
            dataset_id (str): Unique ID for the dataset.
            document_id (str): Unique ID for the document.

        Returns:
            GsDocumentModel: Parsed document model containing elements and metadata.
        """
        url = f"projects/{project_id}/datasets/{dataset_id}/documents/{document_id}/extraction/"

        response = self.client._request("GET", url)

        # Convert the response to GsDocumentModel using Pydantic's validation and parsing
        gs_document = GsDocumentModel(**response)

        return gs_document

    def download_document(
        self, project_id: str, dataset_id: str, document_id: str, output_dir: str = "./"
    ) -> str:
        """
        Download the raw document.

        Args:
            project_id (str): Unique ID for the project.
            dataset_id (str): Unique ID for the dataset.
            document_id (str): Unique ID for the document.
            output_dir (str): Directory where the file will be saved. Defaults to current directory.

        Returns:
            str: Path to the downloaded file.
        """

        url = f"projects/{project_id}/datasets/{dataset_id}/documents/{document_id}/download/"

        # Make an API request to download the document (using stream=True)
        try:
            response = self.client._request("GET", url, stream=True)

            # Get the filename from Content-Disposition or generate one
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
            else:
                filename = f"{document_id}.file"

            # Full file path to save the document
            file_path = os.path.join(output_dir, filename)

            # Write the downloaded content to a file
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

            return file_path

        except Exception as e:
            raise RuntimeError(f"Error downloading document {document_id}: {str(e)}")

    def delete_document(
        self, project_id: str, dataset_id: str, document_id: str
    ) -> dict:
        """
        Delete a document

        Args:
            project_id (str): Unique ID for the project.
            dataset_id (str): Unique ID for the dataset.
            document_id (str): Unique ID for the document.

        Returns:
            dict: Confirmation message indicating success or failure.
        """
        url = f"projects/{project_id}/datasets/{dataset_id}/documents/{document_id}/"

        try:
            response = self.client._request("DELETE", url)
            return response
        except Exception as e:
            raise RuntimeError(f"Error deleting document {document_id}: {str(e)}")

    def poll_for_extraction_completion(
        self,
        project_id: str,
        dataset_id: str,
        document_id: str,
        polling_interval: int = 5,
        timeout: int = 120,  # Default timeout of 2 minutes
    ) -> None:
        """
        Polls for the extraction status of a document until it is completed, fails, or times out.

        Args:
            project_id (str): Unique ID for the project.
            dataset_id (str): Unique ID for the dataset.
            document_id (str): Unique ID for the document.
            polling_interval (int): Time in seconds between each polling attempt. Default is 5 seconds.
            timeout (int): Maximum time in seconds to keep polling before giving up. Default is 120 seconds.

        Raises:
            RuntimeError: If the extraction fails or the polling times out.
        """
        start_time = time.time()

        while True:
            # Check the elapsed time to see if the timeout is reached
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                raise RuntimeError(f"Polling timed out after {timeout} seconds for document {document_id}.")

            status_response = self.get_extraction_status(
                project_id, dataset_id, document_id
            )

            if status_response.status == JobStatusCode.COMPLETED:
                break
            elif status_response.status == JobStatusCode.FAILED:
                err_msg = status_response.err_msg or "Unknown error"
                raise RuntimeError(
                    f"Extraction failed for document {document_id}: {err_msg}"
                )

            time.sleep(polling_interval)  # Wait before checking the status again

    def add_and_extract_file(
        self, project_id: str, dataset_id: str, file_path: str,
        extract_tables: bool = False
    ) -> GsDocumentModel:
        """
        Upload a file to the dataset, trigger extraction, and return the extracted document.

        Args:
            project_id (str): Unique ID for the project.
            dataset_id (str): Unique ID for the dataset.
            file_path (str): Path to the file to be uploaded.

        Returns:
            GsDocumentModel: Extracted document data.
        """
        # Add the file to the dataset
        add_file_response = self.dataset_manager.add_files(
            project_id, dataset_id, [file_path], extract_tables
        )
        # Access the internal root dictionary of the response object
        root_response = add_file_response.root

        file_name = file_path.split("/")[-1]  # This gets 'test.pdf'

        # Access the FileUploadResponse for the file and get the document_id
        file_upload_response = root_response[file_name]  # Access the root dictionary
        document_id = file_upload_response.document_id  # Now we get the document_id

        # Poll for extraction status using the common polling logic
        self.poll_for_extraction_completion(project_id, dataset_id, document_id)

        # Retrieve and return the extracted elements
        return self.get_extracted_elements(project_id, dataset_id, document_id)

    def add_and_extract_url(
        self, project_id: str, dataset_id: str, url_to_extract: str,
        extract_tables: bool = False
    ) -> GsDocumentModel:
        """
        Add a URL to the dataset, trigger extraction, and return the extracted document.

        Args:
            project_id (str): Unique ID for the project.
            dataset_id (str): Unique ID for the dataset.
            url_to_extract (str): URL to be extracted.

        Returns:
            GsDocumentModel: Extracted document data.
        """
        # Add the URL to the dataset
        add_url_response = self.dataset_manager.add_urls(
            project_id, dataset_id, [url_to_extract], extract_tables
        )
        # Access the internal root dictionary of the response object
        root_response = add_url_response.root

        document_id = root_response[url_to_extract].document_id

        # Poll for extraction status using the common polling logic
        self.poll_for_extraction_completion(project_id, dataset_id, document_id)

        # Retrieve and return the extracted elements
        return self.get_extracted_elements(project_id, dataset_id, document_id)
    
    def search(
        self, project_id: str, dataset_id: str, document_id: str,
        query: str = None, sections: list[str] = None, response_format: Dict[str, Any] = None
    ) -> GsDocumentModel:
        """
        Search within a document

        Args:
            project_id (str): Unique ID for the project.
            dataset_id (str): Unique ID for the dataset.
            document_id (str): Unique ID for the document
            query: Optional search query
            section: The section to limit the search to
            response_format: Optional structured format to use for the response

        Returns:
            Search response
        """
        if not query and not sections:
            raise ValueError("Please provide query or sections to search")

        # Construct the endpoint URL
        url = f"projects/{project_id}/datasets/{dataset_id}/documents/{document_id}/search"

        payload = {}
        if query:
            payload["query"] = query
        if sections:
            payload["sections"] = sections
        if response_format:
            payload["response_format"] = response_format

        response = self.client._request("POST", url, json=payload)
        if response:
            return response.get("response", None)
        return None    