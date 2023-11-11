from abc import ABC
from typing import List

from app.data_managers.base import AbstractDataManager


class ManagerCombine:
    """Class encapsulate few managers"""
    pass


def combine_classes(*classes: List[AbstractDataManager]):
    combine_obj = ManagerCombine
    for cls in classes:
        methods = [method for method in dir(cls) if callable(getattr(cls, method)) and not method.startswith("__")]
        for method in methods:
            setattr(ManagerCombine, method, getattr(cls, method))

    return combine_obj
