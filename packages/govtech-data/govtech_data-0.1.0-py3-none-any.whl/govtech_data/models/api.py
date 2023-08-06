from pydantic import BaseModel


class PackageShow(BaseModel):
    id: str


class ResourceShow(BaseModel):
    id: str
