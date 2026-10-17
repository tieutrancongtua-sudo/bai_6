import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from datetime import datetime
from interface.lecturer import Lecturer
from interface.teaching_assistant import TeachingAssistant
from device.device_types import AirConditionerController, Microphone
from device.device_status import DeviceStatus
from borrowing_slip import BorrowingSlip
from exceptions import (
    DeviceUnavailableException,
    BorrowLimitExceededException,
    DuplicateDeviceException,
    InvalidBorrowPeriodException,
    DeviceNotInSlipException,
    DeviceAlreadyReturnedException,
)

gv = Lecturer("GV001", "Nguyễn Văn A")
tg = TeachingAssistant("TG001", "Trần Thị B")


print("1 Mượn điều hòa UnderMaintenance")
ac = AirConditionerController("TB002", "Điều khiển điều hòa", 2018, 800_000)
ac.status = DeviceStatus.UNDER_MAINTENANCE
slip = BorrowingSlip("PM001", gv, "A101", datetime(2024, 1, 10))
try:
    slip.add_device(ac, 5)
except DeviceUnavailableException as e:
    print("  Lỗi:", e)


print("2 Trợ giảng mượn thiết bị thứ 3")
m1 = Microphone("TB101", "Micro 1", 2023, 500_000)
m2 = Microphone("TB102", "Micro 2", 2023, 500_000)
m3 = Microphone("TB103", "Micro 3", 2023, 500_000)
slip = BorrowingSlip("PM002", tg, "A102", datetime(2024, 1, 10))
try:
    slip.add_device(m1, 1)
    slip.add_device(m2, 1)
    slip.add_device(m3, 1)
except BorrowLimitExceededException as e:
    print("  Lỗi:", e)


print("3 Thêm cùng 1 micro 2 lần")
mic = Microphone("TB201", "Micro trùng", 2023, 500_000)
slip = BorrowingSlip("PM003", gv, "A103", datetime(2024, 1, 10))
try:
    slip.add_device(mic, 1)
    slip.add_device(mic, 1)
except DuplicateDeviceException as e:
    print("  Lỗi:", e)


print("4 Mượn micro 3 ngày (giới hạn 1 ngày)")
mic = Microphone("TB301", "Micro 1 ngày", 2023, 500_000)
slip = BorrowingSlip("PM004", gv, "A104", datetime(2024, 1, 10))
try:
    slip.add_device(mic, 3)
except InvalidBorrowPeriodException as e:
    print("  Lỗi:", e)

print("5 Trả máy chiếu không thuộc phiếu")
slip = BorrowingSlip("PM005", gv, "A105", datetime(2024, 1, 10))
try:
    slip.return_device("TB999", datetime(2024, 1, 12))
except DeviceNotInSlipException as e:
    print("  Lỗi:", e)

print("6 Trả cùng 1 thiết bị 2 lần")
mic = Microphone("TB601", "Micro 6", 2023, 500_000)
slip = BorrowingSlip("PM006", gv, "A106", datetime(2024, 1, 10))
slip.add_device(mic, 1)
slip.return_device("TB601", datetime(2024, 1, 11))
try:
    slip.return_device("TB601", datetime(2024, 1, 12))
except DeviceAlreadyReturnedException as e:
    print("  Lỗi:", e)

