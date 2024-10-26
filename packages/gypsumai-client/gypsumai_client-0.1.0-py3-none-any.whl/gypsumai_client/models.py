from enum import IntEnum
from pydantic import BaseModel, Field, RootModel
from typing import Any, List, Optional, Union
from datetime import datetime
from typing import Dict


class ProjectCreate(BaseModel):
    """
    Model for creating a new project.
    """

    name: str = Field(..., title="Project Name", description="The name of the project.")
    id: str = Field(
        ..., title="Project ID", description="The unique identifier for the project."
    )


class Project(BaseModel):
    id: str = Field(
        ..., title="Project ID", description="The unique identifier for the project."
    )
    name: str = Field(..., title="Project Name", description="The name of the project.")
    tenant_id: str = Field(
        ...,
        title="Tenant ID",
        description="The tenant identifier associated with the project.",
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the project was created.",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the project was last updated.",
    )


class ProjectList(BaseModel):
    """
    Model for representing a list of projects.
    """

    projects: List[Project] = Field(
        ..., title="Projects", description="A list of projects."
    )


class DatasetCreate(BaseModel):
    """
    Model for creating a new dataset.
    """

    id: str = Field(
        ..., title="Dataset ID", description="The unique identifier for the dataset."
    )
    name: str = Field(..., title="Dataset Name", description="The name of the dataset.")
    project_id: str = Field(
        ..., title="Project ID", description="The unique identifier for the project."
    )


class Dataset(BaseModel):
    """
    Model for representing a dataset.
    """

    id: str = Field(
        ..., title="Dataset ID", description="The unique identifier for the dataset."
    )
    name: str = Field(..., title="Dataset Name", description="The name of the dataset.")
    project_id: str = Field(
        ..., title="Project ID", description="The unique identifier for the project."
    )
    tenant_id: Optional[str] = Field(
        None,
        title="Tenant ID",
        description="The tenant identifier associated with the dataset.",
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the dataset was created.",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the dataset was last updated.",
    )


class DatasetList(BaseModel):
    """
    Model for representing a list of datasets.
    """

    datasets: List[Dataset] = Field(
        ..., title="Datasets", description="A list of datasets."
    )


class DeleteResponse(BaseModel):
    """
    Model for representing a delete response.
    """

    status: str = Field(..., title="Status", description="The status of the operation.")
    message: str = Field(
        ..., title="Message", description="A message describing the operation."
    )


class JobStatusResponse(BaseModel):
    status: Union[str, int]
    err_code: Union[int, None]
    err_msg: Union[str, None]


class FileUploadResponse(BaseModel):
    """
    Model representing the response for a single file upload.
    """

    status: str = Field(
        ..., title="Status", description="The status of the file upload."
    )
    document_id: str = Field(
        ...,
        alias="document-id",
        title="Document ID",
        description="The unique identifier of the document.",
    )
    submission_id: str = Field(
        ...,
        alias="submission-id",
        title="Submission ID",
        description="The unique identifier of the submission.",
    )


class AddFileResponse(RootModel[Dict[str, FileUploadResponse]]):
    """
    Root model representing the response for adding files/URLs to a dataset.
    The root model is a dictionary that maps file names to their respective upload results.
    """

    pass


class ImagePropertiesModel(BaseModel):
    heading: Optional[str] = Field(None, title="Image Heading")
    caption: Optional[str] = Field(None, title="Image Caption")
    location: Optional[str] = Field(None, title="Image Location")


class TablePropertiesModel(BaseModel):
    heading: Optional[str] = Field(None, title="Table Heading")
    caption: Optional[str] = Field(None, title="Table Caption")
    header_row: Optional[bool] = Field(False, title="Has Header Row")


class ElementModel(BaseModel):
    type: str = Field(..., title="Element Type", description="Type of the element")
    html_tag: Optional[str] = Field(
        None, title="HTML Tag", description="HTML tag of the element"
    )
    text: Optional[str] = Field(
        None, title="Element Text", description="Text of the element"
    )
    section: List[str] = Field(
        [], title="Section", description="Hierarchy of headings for this element"
    )
    page_number: Optional[int] = Field(None, title="Page Number")
    table_properties: Optional[TablePropertiesModel] = Field(
        None, title="Table Properties"
    )
    image_properties: Optional[ImagePropertiesModel] = Field(
        None, title="Image Properties"
    )
    properties: Dict[str, Any] = Field({}, title="Additional Properties")


class SchemaFieldModel(BaseModel):
    name: str = Field(..., title="Field Name")
    type: str = Field(..., title="Field Type")
    description: Optional[str] = Field(None, title="Field Description")


class GsDocumentModel(BaseModel):
    id: str = Field(
        ..., title="Document ID", description="Unique identifier for the document"
    )
    name: str = Field(..., title="Document Name", description="Name of the document")
    type: Optional[str] = Field(
        None,
        title="Document Type",
        description="Type of the document based on its extension",
    )
    tags: Dict[str, List[str]] = Field({}, title="Document Tags")
    elements: List[ElementModel] = Field(
        [],
        title="Document Elements",
        description="Extracted elements from the document",
    )
    fields: List[SchemaFieldModel] = Field(
        [],
        title="Document Fields",
        description="Extracted schema fields based on user-defined schema",
    )
    properties: Dict[str, Any] = Field(
        {}, title="Document Properties", description="Additional document properties"
    )
    converted_type: Optional[str] = Field(
        None,
        title="Converted Document Type",
        description="Converted type of the document if applicable",
    )


class JobStatusCode(IntEnum):
    """
    Enum to represent different job statuses.
    """

    INITIATED = 0
    COMPLETED = 1
    FAILED = 2
