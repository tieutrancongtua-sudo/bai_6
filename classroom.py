from device.device import Device
from device.device_status import DeviceStatus
from datetime import datetime

class ClassRoom:
    def __init__(self, room_id: str, room_name: str, capacity: int):
        self.room_id = room_id
        self.room_name = room_name
        self.capacity = capacity
        self.devices: list[Device] = []

    def add_device(self, device: Device):
        if device is None:
            raise ValueError
        if any(d.device_id == device.device_id for d in self.devices):
            raise ValueError
        self.devices.append(device)

    def remove_device(self, device_id: str) -> bool:
        device = self.find_device(device_id)
        if device is None:
            return False
        self.devices.remove(device)
        return True

    def find_device(self, device_id: str) -> Device | None:
        return next((d for d in self.devices if d.device_id == device_id), None)

    def calculate_annual_maintenance_cost(self) -> float:
        return sum(d.calculate_annual_maintenance_cost() for d in self.devices)

    def get_devices_requiring_maintenance(self) -> list[Device]:
        current_year = datetime.now().year
        return [
            d for d in self.devices
            if d.status == DeviceStatus.UNDER_MAINTENANCE
            or (current_year - d.year_of_manufacture) > 5
        ]