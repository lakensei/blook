from abc import ABC, abstractmethod
from typing import Dict, Any

from pydantic import BaseModel

from ..base import BaseConfig

#
# class VectorConfig(BaseModel):
#     host: str
#     port: str


class VectorsConfig(BaseConfig):

    @classmethod
    def from_settings(cls, settings: Dict[str, Any]) -> Dict:
        return dict(
            impl_type=settings["IMPL_TYPE"],
            **settings["VECTOR_INFOS"]
        )


class BaseRegister(ABC):

    # def __init__(self, host, port, embedding_name):
    #     self.embedding_name = embedding_name
    #     self.host = host
    #     self.port = port

    @abstractmethod
    def connect(self, collection_name: str):
        pass

    @abstractmethod
    def add_embedding(self, embedding, collection_name: str):
        pass

    @abstractmethod
    def search_embeddings(self, query_embedding, collection_name: str, k: int = 5):
        pass


PLUGIN_NAME: str = "vector"
