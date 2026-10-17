from abc import ABC, abstractmethod

class IBorrower(ABC):
    @property
    @abstractmethod
    def borrower_id(self) -> str: ...

    @property
    @abstractmethod
    def full_name(self) -> str: ...

    @abstractmethod
    def get_maximum_devices(self) -> int: ...