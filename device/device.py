from abc import ABC, abstractmethod
from datetime import datetime
from device.device_status import DeviceStatus

class Device(ABC):
    def __init__(self, device_id: str, device_name: str,
                 year_of_manufacture: int, purchase_price: float):
        if not device_id or not device_id.strip():
            raise ValueError
        if purchase_price <= 0:
            raise ValueError
        if year_of_manufacture > datetime.now().year:
            raise ValueError

        self._device_id = device_id        
        self.device_name = device_name
        self.year_of_manufacture = year_of_manufacture
        self.purchase_price = purchase_price
        self.status = DeviceStatus.AVAILABLE

    @property
    def device_id(self) -> str:
        return self._device_id

    @abstractmethod
    def calculate_annual_maintenance_cost(self) -> float:
        ...

    def mark_as_borrowed(self):
        self.status = DeviceStatus.BORROWED

    def mark_as_available(self):
        self.status = DeviceStatus.AVAILABLE

    def __str__(self):
        return (f"Mã: {self.device_id}, Tên: {self.device_name}, "
                f"Năm: {self.year_of_manufacture}, Giá: {self.purchase_price}, "
                f"Trạng thái: {self.status.value}")