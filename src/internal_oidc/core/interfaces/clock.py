from abc import ABC, abstractmethod


class Clock(ABC):
    @abstractmethod
    def now_epoch(self) -> int:
        raise NotImplementedError
