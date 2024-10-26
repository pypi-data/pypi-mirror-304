import requests
from gypsumai_client.project_manager import ProjectManager
from gypsumai_client.dataset_manager import DatasetManager
from gypsumai_client.document_manager import DocumentManager


class GypsumClient:
    def __init__(self, api_key: str, base_url: str = "https://api.gypsum.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"x-gypsum-api-key": self.api_key}

        # Initialize the managers and make them accessible via the client
        self.ProjectManager = ProjectManager(client=self)
        self.DatasetManager = DatasetManager(client=self)
        self.DocumentManager = DocumentManager(
            client=self, dataset_manager=self.DatasetManager
        )

    def _request(self, method: str, endpoint: str, stream: bool = False, **kwargs):
        """
        Internal method to handle HTTP requests.

        Args:
            method (str): The HTTP method (GET, POST, etc.)
            endpoint (str): The API endpoint to call.
            stream (bool): If True, the response will be streamed (e.g., for file downloads).
            **kwargs: Additional keyword arguments to pass to the `requests` method.

        Returns:
            The parsed JSON response for most requests, or the raw response object for streamed requests.
        """
        url = f"{self.base_url}/{endpoint}"

        # Make the request
        response = requests.request(
            method, url, headers=self.headers, stream=stream, **kwargs
        )

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # If stream is True, return the raw response object for file handling
        if stream:
            return response

        # Otherwise, attempt to return the JSON response
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise ValueError(f"Expected JSON response but got non-JSON data from {url}")
