from pydantic import BaseModel

class UploadFileResponse(BaseModel):
    url: str
    bucket: str
    storage_id: str
    object_name: str
    uid: str

class UploadRawDataResponse(BaseModel):
    raw_data_id: str

class UploadAnnotationDataResponse(BaseModel):
    annotation_data_id: str

class CreateDataSetResponse(BaseModel):
    dataset_id: str

class SummaryAndDownloadDataSetResponse(BaseModel):
    url: str
    bucket: str
    object_name: str