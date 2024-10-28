import requests
import hashlib

from os.path import join, dirname, abspath, basename, exists
from os import makedirs
from .types import *

class AnkerAutoTrainSDK:
    def __init__(self, url="https://dataloop.anker-in.com"):
        self.url = url

    def _calculate_md5(self, file_path: str) -> str:
        """计算文件的MD5哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except IOError as e:
            raise Exception(f"Error reading file {file_path}: {e}")
        return hash_md5.hexdigest()
    
    def _query_origin_data(self, query_data: dict) -> dict:
        try:
            url = f"{self.url}/query_origin_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=query_data)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while querying origin data: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while querying origin data: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying origin data: {e}")
        
    def _summarize_and_download(self, dataset_name: str, dataset_version: str) -> SummaryAndDownloadDataSetResponse:
        try:
            url = f"{self.url}/data/annotation/summarize_and_download"
            headers = { 'accept': 'application/json', 'Content-Type': 'application/json' }
            dataset_list = [{"datasetName": dataset_name, "datasetVersion": dataset_version}]
            dataset_info = {"dataset": dataset_list}
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return SummaryAndDownloadDataSetResponse(
                url=response.get("url", ""),
                bucket=response.get("bucketName", ""),
                object_name=response.get("objectName", "")
            )
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while summarizing and downloading dataset: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while summarizing and downloading dataset: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while summarizing and downloading dataset: {e}")

    def upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
        try:
            url = f"{self.url}/get_upload_url"
            file_name = basename(file_path)
            response = requests.post(url, params={"directory": directory, "file_name": file_name})
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while getting upload URL: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while getting upload URL: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting upload URL: {e}")
    
        
        try:    
            upload_url = response.get("url")  # 从响应中获取上传URL
            if not upload_url:
                raise Exception("No upload URL found in the response.")
            file_md5 = self._calculate_md5(file_path)  # 计算文件的MD5
            # 然后put到这个路径
            with open(file_path, "rb") as f:
                res = requests.put(upload_url, data=f)
                res.raise_for_status()  # 检查HTTP错误
                return UploadFileResponse(
                    url=upload_url,
                    bucket=response.get("bucket", ""),
                    storage_id=response.get("storage_id", ""),
                    object_name=response.get("object_name", ""),
                    uid=file_md5
                )
        except requests.exceptions.RequestException as e:
            if res is None:
                raise Exception(f"HTTP error occurred while uploading file: {e}")
            detail = res.json().get("detail")
            raise Exception(f"HTTP error occurred while uploading file: {detail}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading file: {e}")
    
    def upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
        try:
            url = f"{self.url}/upload_raw_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=raw_data)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return UploadRawDataResponse(
                raw_data_id=response.get("raw_data_id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while uploading raw data: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while uploading raw data: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading raw data: {e}")

    def upload_annotated_data(self, annotated_data: dict) -> UploadAnnotationDataResponse: 
        try:
            url = f"{self.url}/data/annotation"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=annotated_data)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return UploadAnnotationDataResponse( 
                annotation_data_id=response.get("id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while uploading annotated data: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while uploading annotated data: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading annotated data: {e}")


    def download_file_by_storage(self, storage_id: str, bucket: str, object_name: str, directory: str) -> str:
        try:
            url = f"{self.url}/get_download_url"
            response = requests.post(url, params={"storage_id": storage_id, "bucket": bucket, "object_name": object_name})
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while getting download URL: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while getting download URL: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")
        
        try:
            download_url = response.get("url")  # 从响应中获取下载URL
            if not download_url:
                raise Exception("No download URL found in the response.")
            response = requests.get(download_url)
            response.raise_for_status()  # 检查HTTP错误
            # 保存到本地
            save_path = join(directory, object_name)
            # 判断目录是否存在
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while downloading file: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while downloading file: {detail}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading file: {e}")
        
    def download_file_by_uid(self, uid: str, directory: str) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = self._query_origin_data(query_origin_data)

            if not origin_data:  # 检查origin_data是否为空
                raise Exception("No origin data found for the given UID.")
            records = origin_data.get("records")

            if not records or len(records) == 0:  # 检查records是否为空
                raise Exception("No origin data found for the given UID.")

            record = records[0]  # 获取第一个记录
            get_uid = record.get("uid")
            if not get_uid or get_uid != uid:
                raise Exception("UID mismatch.")
            storage = record.get("storage")
            storage_id = storage.get("storageId")
            bucket = storage.get("bucket")
            object_name = storage.get("objectName")
            if not storage_id or not bucket or not object_name:
                raise Exception("Missing storage_id, bucket or object_name in origin data.")
            return self.download_file_by_storage(storage_id, bucket, object_name, directory)  # 调用原始下载方法
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

    def create_dataset(self, dataset_info: dict) -> CreateDataSetResponse:
        try:
            url = f"{self.url}/data/annotation/version"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 棃查HTTP错误
            response = response.json()
            return CreateDataSetResponse(
                dataset_id=response.get("dataset_version_id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while creating dataset: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while creating dataset: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while creating dataset: {e}")
        
    def link_dataset(self, annotation_id_list: list, dataset_id: str) -> dict:
        try:
            # 去除annotation_id_list中的重复元素
            unique_annotation_id_list = list(set(annotation_id_list))
            
            url = f"{self.url}/data/annotation/link"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            dataset_info = {
                "annotationIds": unique_annotation_id_list,
                "annotationVersionId": dataset_id
            }
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while linking dataset: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while linking dataset: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while linking dataset: {e}")
        
    def download_dataset(self, dataset_name: str, dataset_version: str, directory: str) -> str:
        try:
            download_response = self._summarize_and_download(dataset_name, dataset_version)

            download_url = download_response.url  # 从响应中获取下载URL
            download_object_name = download_response.object_name
            if not download_url:
                raise Exception("No download URL found in the download_dataset.")
            response = requests.get(download_url)
            response.raise_for_status()  # 检查HTTP错误
            # 保存到本地
            save_path = join(directory, download_object_name)
            # 判断目录是否存在
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while downloading dataset: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while downloading dataset: {detail}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading dataset: {e}")