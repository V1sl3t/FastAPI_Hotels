from typing import TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import Row, RowMapping

from src.db import Base


SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: Type[Base]
    schema: Type[SchemaType]

    @classmethod
    def map_to_domain_entity(cls, data: Base | dict | Row | RowMapping) -> BaseModel:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel) -> Base:
        return cls.db_model(**data.model_dump())
