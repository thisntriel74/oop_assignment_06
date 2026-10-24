# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from device_status import DeviceStatus
from exceptions import DeviceUnavailableException


class Device(ABC):
    """Lớp trừu tượng: thiết bị chung của trường."""

    def __init__(self, device_id, name, year_in_use, purchase_price):
        # Kiểm tra dữ liệu đầu vào
        if device_id is None or str(device_id).strip() == "":
            raise ValueError("Mã thiết bị không được rỗng")
        if purchase_price <= 0:
            raise ValueError("Giá mua phải lớn hơn 0")
        if year_in_use > datetime.now().year:
            raise ValueError("Năm đưa vào sử dụng không được lớn hơn năm hiện tại")

        self._device_id = device_id          # chỉ gán 1 lần ở đây
        self.name = name
        self.year_in_use = year_in_use
        self.purchase_price = Decimal(purchase_price)
        self._status = DeviceStatus.AVAILABLE

    # Mã thiết bị: chỉ có getter, không có setter => chỉ đặt khi khởi tạo
    @property
    def device_id(self):
        return self._device_id

    @property
    def status(self):
        return self._status

    def get_age(self):
        """Số năm đã sử dụng."""
        return datetime.now().year - self.year_in_use

    # ---- Các thao tác đổi trạng thái (gom vào 1 chỗ để dễ kiểm soát) ----
    def mark_as_borrowed(self):
        if self._status != DeviceStatus.AVAILABLE:
            raise DeviceUnavailableException(self._device_id, self._status)
        self._status = DeviceStatus.BORROWED

    def mark_as_available(self):
        self._status = DeviceStatus.AVAILABLE

    def send_to_maintenance(self):
        self._status = DeviceStatus.UNDER_MAINTENANCE

    @abstractmethod
    def calculate_annual_maintenance_cost(self):
        """Chi phí bảo trì dự kiến 1 năm - mỗi loại thiết bị tự tính."""

    def __str__(self):
        return (f"[{self._device_id}] {self.name} | Năm: {self.year_in_use} | "
                f"Giá: {self.purchase_price:,.0f} | Trạng thái: {self._status.value}")


class TeachingDevice(Device):
    """Thiết bị phục vụ giảng dạy: có giới hạn mượn và phí trả muộn."""

    MAX_BORROW_DAYS = 7          # số ngày mượn tối đa (lớp con ghi đè)
    MAX_PERIODS = 10             # số tiết tối đa được mượn
    LATE_FEE_PER_DAY = Decimal("10000")
    MAINTENANCE_RATE = Decimal("0.02")

    @property
    def max_borrow_days(self):
        return self.MAX_BORROW_DAYS

    @property
    def max_periods(self):
        return self.MAX_PERIODS

    @property
    def late_fee_per_day(self):
        return self.LATE_FEE_PER_DAY

    def calculate_annual_maintenance_cost(self):
        return self.purchase_price * self.MAINTENANCE_RATE


class AirConRemote(TeachingDevice):
    """Điều khiển điều hòa."""
    MAX_BORROW_DAYS = 5
    MAX_PERIODS = 10
    LATE_FEE_PER_DAY = Decimal("10000")
    MAINTENANCE_RATE = Decimal("0.02")


class Microphone(TeachingDevice):
    """Micro không dây (pin, đầu thu dễ hỏng nên phí bảo trì cao hơn)."""
    MAX_BORROW_DAYS = 1
    MAX_PERIODS = 5
    LATE_FEE_PER_DAY = Decimal("30000")
    MAINTENANCE_RATE = Decimal("0.08")


class ProjectorRemote(TeachingDevice):
    """Điều khiển máy chiếu."""
    MAX_BORROW_DAYS = 3
    MAX_PERIODS = 10
    LATE_FEE_PER_DAY = Decimal("20000")
    MAINTENANCE_RATE = Decimal("0.03")