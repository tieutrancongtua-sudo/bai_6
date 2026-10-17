from device.device_status import DeviceStatus

class BorrowingException(Exception):
    pass

class DeviceUnavailableException(BorrowingException):
    def __init__(self, device_id: str, current_status: DeviceStatus):
        super().__init__(
            f"Thiết bị {device_id} không ở trạng thái sẵn sàng. "
            f"Trạng thái hiện tại: {current_status.value}"
        )
        self.device_id = device_id
        self.current_status = current_status


class BorrowLimitExceededException(BorrowingException):
    def __init__(self, borrower_id: str, maximum_devices: int):
        super().__init__(
            f"Người mượn {borrower_id} đã đạt giới hạn {maximum_devices} thiết bị."
        )
        self.borrower_id = borrower_id
        self.maximum_devices = maximum_devices


class InvalidBorrowPeriodException(BorrowingException):
    def __init__(self, device_id: str, requested_days: int, maximum_days: int):
        super().__init__(
            f"Số ngày mượn không hợp lệ cho thiết bị {device_id}. "
            f"Yêu cầu: {requested_days}, tối đa: {maximum_days}"
        )
        self.device_id = device_id
        self.requested_days = requested_days
        self.maximum_days = maximum_days


class DuplicateDeviceException(BorrowingException):
    def __init__(self, device_id: str):
        super().__init__(f"Thiết bị {device_id} đã tồn tại trong phiếu.")
        self.device_id = device_id


class DeviceNotInSlipException(BorrowingException):
    def __init__(self, device_id: str):
        super().__init__(f"Thiết bị {device_id} không thuộc phiếu mượn.")
        self.device_id = device_id


class DeviceAlreadyReturnedException(BorrowingException):
    def __init__(self, device_id: str):
        super().__init__(f"Thiết bị {device_id} đã được trả trước đó.")
        self.device_id = device_id