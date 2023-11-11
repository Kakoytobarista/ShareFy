from abc import abstractmethod, ABC, ABCMeta
from typing import List, Union, Any, Type

from app.types import T
from app.utils.utils import combine_classes, ManagerCombine


class AbstractBaseService(ABC, metaclass=ABCMeta):
    @abstractmethod
    def create_item(self, data) -> None:
        pass

    @abstractmethod
    def get_items(self, model, **kwargs) -> List[Union[T, None]]:
        pass

    @abstractmethod
    def get_item(self, model, **kwargs) -> Union[T, None]:
        pass

    @abstractmethod
    def update_item(self, model, filters, update_data) -> None:
        pass

    @abstractmethod
    def delete_item(self, model) -> None:
        pass


class BaseService(AbstractBaseService):
    def __init__(self, managers: Any):
        self.manager: ManagerCombine = combine_classes(*managers)

    def create_item(self, data):
        return self.manager.create(model=data)

    def get_items(self, model, **kwargs):
        return self.manager.get(model, **kwargs).all()

    def get_item(self, model, **kwargs):
        return self.manager.get(model, **kwargs)

    def update_item(self, model, filters, update_data):
        return self.manager.update(model, filters, update_data)

    def delete_item(self, model):
        return self.manager.delete(model)
