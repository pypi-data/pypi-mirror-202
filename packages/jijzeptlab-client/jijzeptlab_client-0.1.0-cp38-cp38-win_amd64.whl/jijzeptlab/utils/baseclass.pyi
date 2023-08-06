import abc

from abc import ABC, abstractmethod
from typing import Any

import jijmodeling as jm

from _typeshed import Incomplete
from pydantic import BaseModel

class Option(BaseModel):
    class Config:
        extra: Incomplete
        allow_mutation: bool

class Result(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def to_sample_set(self) -> jm.SampleSet: ...

class ResultWithDualVariables(Result, metaclass=abc.ABCMeta): ...

class StateModel(metaclass=abc.ABCMeta):
    @abstractmethod
    def reset(self, *args, **kwargs) -> Any: ...
    @abstractmethod
    def update(self, *args, **kwargs) -> Any: ...
