from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Dict, Optional


class BaseDto(ABC):
    def dump(self) -> Dict:
        return asdict(self)

    @staticmethod
    @abstractmethod
    def load(data: Optional[Dict]) -> "BaseDto":
        pass
