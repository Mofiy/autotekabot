import datetime
from dataclasses import dataclass

__version_ = 0.0001

@dataclass
class User:
    id: int
    name: str
    phone: str
    time = datetime.datetime.now()
    score: int
