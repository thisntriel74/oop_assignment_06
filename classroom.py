# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************

from decimal import Decimal

from device_status import DeviceStatus
from exceptions import DuplicateDeviceException


class ClassRoom:
    """Phòng học: kết tập (aggregation) các thiết bị.
    Xóa phòng không làm mất thiết bị."""

    def __init__(self, room_id, room_name, capacity):
        self.room_id = room_id
        self.room_name = room_name
        self.capacity = capacity
        self._devices = []

    @property
    def devices(self):
        return list(self._devices)   # trả về bản sao để bên ngoài không sửa trực tiếp

    def add_device(self, device):
        if device is None:
            raise ValueError("Thiết bị không được null")
        if self.find_device(device.device_id) is not None:
            raise DuplicateDeviceException(device.device_id)
        self._devices.append(device)

    def remove_device(self, device_id):
        device = self.find_device(device_id)
        if device is None:
            return False
        self._devices.remove(device)
        return True

    def find_device(self, device_id):
        for d in self._devices:
            if d.device_id == device_id:
                return d
        return None

    def calculate_annual_maintenance_cost(self):
        # Đa hình: gọi chung 1 phương thức, mỗi lớp con tự tính, KHÔNG dùng if/isinstance
        return sum((d.calculate_annual_maintenance_cost() for d in self._devices),
                   Decimal(0))

    def get_devices_requiring_maintenance(self):
        return [d for d in self._devices
                if d.status == DeviceStatus.UNDER_MAINTENANCE or d.get_age() > 5]