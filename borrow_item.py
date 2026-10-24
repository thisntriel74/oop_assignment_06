# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************

from datetime import timedelta
from decimal import Decimal

from exceptions import DeviceAlreadyReturnedException, InvalidReturnDateException


class BorrowItem:
    """Một dòng trong phiếu mượn: 1 thiết bị + thời hạn mượn."""

    def __init__(self, device, borrowed_date, due_date, from_period=1, to_period=1):
        if device is None:
            raise ValueError("Thiết bị không được null")
        if due_date < borrowed_date:
            raise ValueError("Hạn trả phải sau hoặc bằng ngày mượn")
        if from_period < 1 or to_period < from_period:
            raise ValueError("Tiết mượn không hợp lệ (cần 1 <= từ tiết <= đến tiết)")

        self._device = device
        self._borrowed_date = borrowed_date
        self._due_date = due_date
        self._from_period = from_period
        self._to_period = to_period
        self._returned_date = None          # ban đầu chưa trả

    @property
    def device(self):
        return self._device

    @property
    def borrowed_date(self):
        return self._borrowed_date

    @property
    def due_date(self):
        return self._due_date

    @property
    def returned_date(self):
        return self._returned_date

    @property
    def is_returned(self):
        return self._returned_date is not None

    @property
    def from_period(self):
        return self._from_period

    @from_period.setter
    def from_period(self, value):
        if value < 1 or value > self._to_period:
            raise ValueError("Từ tiết phải >= 1 và <= đến tiết")
        self._from_period = value

    @property
    def to_period(self):
        return self._to_period

    @to_period.setter
    def to_period(self, value):
        if value < self._from_period:
            raise ValueError("Đến tiết phải >= từ tiết")
        self._to_period = value

    def return_device(self, returned_date):
        """Ghi nhận ngày trả. Kiểm tra hết rồi mới thay đổi dữ liệu."""
        if self.is_returned:
            raise DeviceAlreadyReturnedException(self._device.device_id)
        if returned_date < self._borrowed_date:
            raise InvalidReturnDateException(
                self._device.device_id, self._borrowed_date, returned_date)
        self._returned_date = returned_date

    def calculate_late_fee(self):
        """Phí trả muộn = số ngày muộn x phí mỗi ngày của thiết bị."""
        if not self.is_returned:
            return Decimal(0)
        late_days = (self._returned_date - self._due_date).days
        return Decimal(max(late_days, 0)) * self._device.late_fee_per_day

    def is_late(self):
        return self.is_returned and self._returned_date > self._due_date

    def __str__(self):
        tra = f"{self._returned_date:%d/%m/%Y}" if self.is_returned else "chưa trả"
        return (f"{self._device.name} ({self._device.device_id}) | "
                f"Mượn: {self._borrowed_date:%d/%m/%Y} | Hạn: {self._due_date:%d/%m/%Y} | "
                f"Tiết {self._from_period}-{self._to_period} | Trả: {tra}")