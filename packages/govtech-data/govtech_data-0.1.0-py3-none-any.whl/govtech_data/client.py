from functools import lru_cache
from typing import Type, Union

import requests
from fuzzywuzzy import process
from pydantic import BaseModel
from loguru import logger

from govtech_data.models.api import PackageShow, ResourceShow
from govtech_data.models.resources.package_list import PackageListModel
from govtech_data.models.resources.package_show import PackageShowModel
from govtech_data.models.resources.resource_show import ResourceShowModel

ENDPOINTS = {
    "ckan_resource_show": "https://data.gov.sg/api/action/resource_show",
    "ckan_datastore_search": "https://data.gov.sg/api/action/datastore_search",
    "ckan_package_show": "https://data.gov.sg/api/action/package_show",
    "ckan_package_list": "https://data.gov.sg/api/action/package_list",
}

COMMON_HEADERS = {"accept": "application/json"}

DEFAULT_TIMEOUT_IN_SECONDS = 30


class GovTechClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GovTechClient, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

    @classmethod
    def resource_show(cls, id_or_key: str) -> Union[BaseModel, ResourceShowModel]:
        return cls.get_model_from_json_response(
            ENDPOINTS.get("ckan_package_show"),
            ResourceShow(**{"id": id_or_key}).dict(),
            ResourceShowModel,
        )

    def datastore_search(self):
        pass

    @classmethod
    def package_show(cls, id_or_key: str) -> Union[BaseModel, PackageShowModel]:
        return cls.get_model_from_json_response(
            ENDPOINTS.get("ckan_package_show"),
            PackageShow(**{"id": id_or_key}).dict(),
            PackageShowModel,
        )

    @classmethod
    @lru_cache(maxsize=1)
    def package_list(cls) -> Union[BaseModel, PackageListModel]:
        return cls.get_model_from_json_response(
            ENDPOINTS.get("ckan_package_list"), {}, PackageListModel
        )

    @classmethod
    def search_package(cls, name: str, limit: int = 5):
        return process.extract(name, cls.package_list().result, limit=limit)

    @classmethod
    def get_model_from_json_response(
        cls, url: str, params: dict, model: Type[BaseModel]
    ):
        if url is None:
            raise Exception("url cannot be None!")
        if model is None:
            raise Exception("model cannot be None!")
        logger.info(f"endpoint name: {url}")
        resp = requests.get(
            url,
            params=params,
            headers=COMMON_HEADERS,
            timeout=DEFAULT_TIMEOUT_IN_SECONDS,
        )
        if not resp.ok:
            resp.raise_for_status()
        return model(**resp.json())
