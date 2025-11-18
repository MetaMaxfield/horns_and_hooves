from typing import Generic, Protocol, TypeVar

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")


class EntityMapper(Protocol, Generic[TModel, TEntity]):
    def to_entity(self, model: TModel) -> TEntity: ...
