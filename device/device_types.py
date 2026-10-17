from device.device import Device   

class AirConditionerController(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        return self.purchase_price * 0.05


class Microphone(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        return self.purchase_price * 0.10


class ProjectorController(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        return self.purchase_price * 0.08