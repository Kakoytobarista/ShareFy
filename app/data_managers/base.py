from abc import ABC, ABCMeta, abstractmethod
from typing import Any, List, Type, TypeVar, Union

from models.v1.user import Base
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')

class AbstractDataManager(ABC, metaclass=ABCMeta):
    @abstractmethod
    def create(self, model: Type[T]) -> None:
        pass

    @abstractmethod
    def get(self, model: Type[T], **kwargs) -> List[Union[T, None]]:
        pass

    @abstractmethod
    def update(self, model: Type[T], updated_data: dict) -> None:
        pass

    @abstractmethod
    def delete(self, model: Type[T]) -> None:
        pass


class SQLAlchemyDataManager(AbstractDataManager):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model: Base):
        self.session.add(model)
        await self.session.commit()

    async def get(self, model: Base, **kwargs) -> Any:
        query = select(model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(self, model: Base, **kwargs) -> Any:
        query = select(model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, model: Base, updated_data: dict) -> None:
        for key, value in updated_data.items():
            setattr(model, key, value)
        await self.session.commit()

    async def delete(self, model: Base):
        await self.session.delete(instance=model)
        await self.session.commit()
