from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Optional


class BaseDto(ABC):
    def dump(self) -> dict:
        return asdict(self)

    @staticmethod
    @abstractmethod
    def load(data: Optional[dict]) -> "BaseDto":
        pass
