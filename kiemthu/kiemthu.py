import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from interface.lecturer import Lecturer
from device.device_types import ProjectorController, AirConditionerController, Microphone
from borrowing_slip import BorrowingSlip
from exceptions import BorrowingException
from datetime import datetime

from datetime import datetime, timedelta

from interface.lecturer import Lecturer
from device.device_types import (
    ProjectorController,
    AirConditionerController,
    Microphone,
)
from borrowing_slip import BorrowingSlip
from exceptions import BorrowingException



def is_late(item) -> bool:
    """Item đã trả nhưng trả sau hạn."""
    if not item.is_returned:
        return False
    due_date = item.borrowed_date + timedelta(days=item.to_period)
    return item.returned_date > due_date


def show_report(slips: list[BorrowingSlip]):
    print("\n===== PHIẾU TRẢ MUỘN =====")
    co_tre = False
    for slip in slips:
        late_items = [i for i in slip.items if is_late(i)]
        if not late_items:
            continue
        co_tre = True
        print(f"\nPhiếu: {slip.slip_id} - {slip.borrower.full_name} - {slip.teaching_room}")
        for item in late_items:
            due = item.borrowed_date + timedelta(days=item.to_period)
            late_days = (item.returned_date - due).days
            print(f"  - {item.device.device_name}: trả muộn {late_days} ngày "
                  f"(hạn {due.date()}, trả {item.returned_date.date()})")
    if not co_tre:
        print("  (Không có)")

    print("\n===== PHIẾU CHƯA TRẢ =====")
    co_chua_tra = False
    for slip in slips:
        unreturned = [i for i in slip.items if not i.is_returned]
        if not unreturned:
            continue
        co_chua_tra = True
        print(f"\nPhiếu: {slip.slip_id} - {slip.borrower.full_name} - {slip.teaching_room}")
        for item in unreturned:
            print(f"  - {item.device.device_name}: chưa trả "
                  f"(mượn ngày {item.borrowed_date.date()})")
    if not co_chua_tra:
        print("  (Không có)")



def main():

    lecturer = Lecturer("GV001", "Nguyễn Văn A")
    print(f"1. Đã tạo giảng viên: {lecturer.full_name} ({lecturer.borrower_id})")

    projector = ProjectorController("TB001", "Điều khiển máy chiếu", 2026, 1_000_000)
    ac = AirConditionerController("TB002", "Điều khiển điều hòa", 2026, 800_000)
    mic = Microphone("TB003", "Micro không dây", 2026, 500_000)
    print(f"2. Đã tạo 3 thiết bị:")
    print(f"   - {projector}")
    print(f"   - {ac}")
    print(f"   - {mic}")

    slip = BorrowingSlip(
        slip_id="PM001",
        borrower=lecturer,
        teaching_room="Phòng A101",
        borrowed_date=datetime(2026, 1, 10),
    )
    print(f"3. Đã tạo phiếu mượn: {slip.slip_id} - {slip.teaching_room} "
          f"- ngày {slip.borrowed_date.date()}")

    try:
        slip.add_device(projector, borrow_days=5)   
        slip.add_device(mic, borrow_days=5)         
        print("4. Đã thêm điều khiển máy chiếu và micro vào phiếu.")
    except BorrowingException as e:
        print(f" Lỗi khi thêm thiết bị: {e}")

    try:
        fee = slip.return_device("TB001", datetime(2026, 1, 15))
        print(f"5. Đã trả điều khiển máy chiếu đúng hạn.")
    except BorrowingException as e:
        print(f" Lỗi khi trả máy chiếu: {e}")

    try:
        fee = slip.return_device("TB003", datetime(2026, 1, 17))
        print(f"6. Đã trả micro muộn 2 ngày.  ")
    except BorrowingException as e:
        print(f" Lỗi khi trả micro: {e}")

    print("\n7. Báo cáo:")
    show_report([slip])


if __name__ == "__main__":
    main()