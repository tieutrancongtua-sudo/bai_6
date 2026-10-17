from datetime import datetime
from borrow_item import BorrowItem
from interface.i_borrower import IBorrower
from device.device import Device
from device.device_status import DeviceStatus
from exceptions import *

class BorrowingSlip:
    def __init__(self, slip_id: str, borrower: IBorrower,
                 teaching_room: str, borrowed_date: datetime):
        if not slip_id or not slip_id.strip():
            raise ValueError
        if borrower is None:
            raise ValueError
        if not teaching_room or not teaching_room.strip():
            raise ValueError

        self._slip_id = slip_id
        self._borrower = borrower
        self._teaching_room = teaching_room
        self._borrowed_date = borrowed_date
        self._items: list[BorrowItem] = []

    @property
    def slip_id(self) -> str:
        return self._slip_id

    @property
    def borrower(self) -> IBorrower:
        return self._borrower

    @property
    def teaching_room(self) -> str:
        return self._teaching_room

    @property
    def borrowed_date(self) -> datetime:
        return self._borrowed_date

    @property
    def items(self) -> list[BorrowItem]:
        return list(self._items) 

    
    def add_device(self, device: Device, borrow_days: int):
        self._validate_borrowing(device, borrow_days)

        item = BorrowItem(
            device=device,
            borrowed_date=self._borrowed_date,
            from_period=0,
            to_period=borrow_days
        )

        device.mark_as_borrowed()
        self._items.append(item)

    def _validate_borrowing(self, device: Device, borrow_days: int):
        if device is None:
            raise ValueError
        
        if borrow_days <= 0:
            raise InvalidBorrowPeriodException(device.device_id, borrow_days, 0)
        
        if any(i.device.device_id == device.device_id for i in self._items):
            raise DuplicateDeviceException(device.device_id)
        
        if len(self._items) >= self._borrower.get_maximum_devices():
            raise BorrowLimitExceededException(
                self._borrower.borrower_id,
                self._borrower.get_maximum_devices()
            )
        
        if device.status != DeviceStatus.AVAILABLE:
            raise DeviceUnavailableException(device.device_id, device.status)


    def return_device(self, device_id: str, returned_date: datetime) -> float:
        if not device_id or not device_id.strip():
            raise ValueError

        item = next(
            (i for i in self._items if i.device.device_id == device_id),
            None
        )
        if item is None:
            raise DeviceNotInSlipException(device_id)
        if item.is_returned:
            raise DeviceAlreadyReturnedException(device_id)
        if returned_date < item.borrowed_date:
            raise ValueError

        item.return_device(returned_date)
        item.device.mark_as_available()

        return self._calculate_late_fee(item)

    def _calculate_late_fee(self, item: BorrowItem) -> float:
     
        due_date = item.borrowed_date.replace()  
        if item.returned_date and item.returned_date > due_date:
            late_days = (item.returned_date - due_date).days
            return item.device.purchase_price * 0.1 * late_days
        return 0.0

    def calculate_total_late_fee(self) -> float:
        return sum(self._calculate_late_fee(i) for i in self._items)