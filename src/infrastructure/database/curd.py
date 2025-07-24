from typing import TypeVar, Generic, Optional, Any

ModelID = TypeVar("ModelID")
ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType")


class BaseDatabase(Generic[ModelType, ModelID]):

    async def get(self, model_id: ModelID) -> Optional[ModelType]:
        raise NotImplementedError()

    async def select(self, model_id: ModelID) -> Optional[ModelType]:
        raise NotImplementedError()

    async def create(self, create_dict: dict[str, Any]) -> ModelType:
        raise NotImplementedError()

    async def update(self, model: ModelType, update_dict: dict[str, Any]) -> ModelType:
        raise NotImplementedError()

    async def delete(self, model: ModelType) -> None:
        raise NotImplementedError()

    async def delete_logical(self, model: ModelType, delete_dict: dict[str, str | int]):
        raise NotImplementedError()
