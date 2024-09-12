
from abc import ABC, abstractmethod
from dataclasses import asdict

class BaseDto(ABC):
    def dump(self):
        return asdict(self)

    @staticmethod
    @abstractmethod
    def load(data: dict | None) -> "BaseDto":
        pass
