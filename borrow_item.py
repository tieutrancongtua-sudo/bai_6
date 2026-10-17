from datetime import datetime
from device.device import Device
from exceptions import DeviceAlreadyReturnedException

class BorrowItem:
    def __init__(self, device: Device, borrowed_date: datetime,
             from_period: int, to_period: int):
        if device is None:
            raise ValueError
        if to_period < from_period:
            raise ValueError

        self.device = device
        self.borrowed_date = borrowed_date
        self.from_period = from_period
        self.to_period = to_period
        self._returned_date: datetime | None = None

    @property
    def returned_date(self) -> datetime | None:
        return self._returned_date

    @property
    def is_returned(self) -> bool:
        return self._returned_date is not None

    def return_device(self, returned_date: datetime):
        if self.is_returned:
            raise DeviceAlreadyReturnedException(self.device.device_id)
        if returned_date < self.borrowed_date:
            raise ValueError
        self._returned_date = returned_date