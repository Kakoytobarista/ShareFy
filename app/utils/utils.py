from typing import List
from typing import Any, Protocol


from data_managers.base import AbstractDataManager


class ManagerCombine(Protocol):
    """Class encapsulate few managers"""
    def __getattr__(self, name: str) -> Any:
        ...


def combine_classes(*classes: List[AbstractDataManager]):
    combine_obj = ManagerCombine
    for cls in classes:
        methods = [method for method in dir(cls) if callable(getattr(cls, method)) and not method.startswith("__")]
        for method in methods:
            setattr(ManagerCombine, method, getattr(cls, method))

    return combine_obj
