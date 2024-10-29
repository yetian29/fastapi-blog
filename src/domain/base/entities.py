from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BaseEntity:
    oid: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
