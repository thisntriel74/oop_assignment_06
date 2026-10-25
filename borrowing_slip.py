# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************

from datetime import timedelta
from decimal import Decimal

from borrow_item import BorrowItem
from device_status import DeviceStatus
from exceptions import (BorrowLimitExceededException, DeviceNotInSlipException,
                        DeviceUnavailableException, DuplicateDeviceException,
                        InvalidBorrowPeriodException)


class BorrowingSlip:
    """Phiếu mượn: thuộc 1 người mượn, gồm nhiều BorrowItem (composition).
    Xóa phiếu thì xóa các BorrowItem nhưng KHÔNG xóa thiết bị / người mượn."""

    def __init__(self, slip_id, borrower, teaching_room, borrowed_date):
        if slip_id is None or str(slip_id).strip() == "":
            raise ValueError("Mã phiếu không hợp lệ")
        if borrower is None:
            raise ValueError("Người mượn không được null")
        if teaching_room is None or str(teaching_room).strip() == "":
            raise ValueError("Phòng dạy không hợp lệ")

        self._slip_id = slip_id
        self._borrower = borrower
        self._teaching_room = teaching_room
        self._borrowed_date = borrowed_date
        self._items = []

    @property
    def slip_id(self):
        return self._slip_id

    @property
    def borrower(self):
        return self._borrower

    @property
    def teaching_room(self):
        return self._teaching_room

    @property
    def borrowed_date(self):
        return self._borrowed_date

    @property
    def items(self):
        return tuple(self._items)     # chỉ đọc

    # ------------------------------------------------------------------
    def _find_item(self, device_id):
        for item in self._items:
            if item.device.device_id == device_id:
                return item
        return None

    def _validate_borrowing(self, device, borrow_days, from_period, to_period):
        """Kiểm tra TẤT CẢ điều kiện, chưa thay đổi bất cứ dữ liệu nào."""
        # 1. device không null
        if device is None:
            raise ValueError("Thiết bị không được null")
        # 2. số ngày mượn > 0 và không vượt giới hạn của thiết bị
        if borrow_days <= 0 or borrow_days > device.max_borrow_days:
            raise InvalidBorrowPeriodException(
                device.device_id, borrow_days, device.max_borrow_days,
                f"Thiết bị {device.device_id}: yêu cầu mượn {borrow_days} ngày, "
                f"tối đa {device.max_borrow_days} ngày")
        # tiết mượn hợp lệ
        if from_period < 1 or to_period < from_period or to_period > device.max_periods:
            raise InvalidBorrowPeriodException(
                device.device_id, f"tiết {from_period}-{to_period}",
                f"tối đa {device.max_periods} tiết")
        # 3. chưa có trong phiếu
        if self._find_item(device.device_id) is not None:
            raise DuplicateDeviceException(device.device_id)
        # 4. chưa đạt giới hạn người mượn
        if len(self._items) >= self._borrower.get_maximum_devices():
            raise BorrowLimitExceededException(
                self._borrower.borrower_id, self._borrower.get_maximum_devices())
        # 5. thiết bị đang Available
        if device.status != DeviceStatus.AVAILABLE:
            raise DeviceUnavailableException(device.device_id, device.status)

    def add_device(self, device, borrow_days, from_period=1, to_period=1):
        # Bước 1: kiểm tra hết (nếu lỗi -> ngoại lệ, chưa có gì bị thay đổi)
        self._validate_borrowing(device, borrow_days, from_period, to_period)
        # Bước 2: hợp lệ rồi mới thay đổi dữ liệu
        item = BorrowItem(device, self._borrowed_date,
                          self._borrowed_date + timedelta(days=borrow_days),
                          from_period, to_period)
        device.mark_as_borrowed()
        self._items.append(item)

    def return_device(self, device_id, returned_date):
        """Trả thiết bị, trả về phí trả muộn của thiết bị đó."""
        if device_id is None or str(device_id).strip() == "":
            raise ValueError("Mã thiết bị không được rỗng")
        item = self._find_item(device_id)
        if item is None:
            raise DeviceNotInSlipException(device_id, self._slip_id)
        # item.return_device tự kiểm tra: đã trả chưa, ngày trả hợp lệ không
        item.return_device(returned_date)
        item.device.mark_as_available()
        return item.calculate_late_fee()

    def calculate_total_late_fee(self):
        return sum((i.calculate_late_fee() for i in self._items), Decimal(0))

    # ---- Hỗ trợ báo cáo ----
    def get_late_items(self):
        return [i for i in self._items if i.is_late()]

    def get_unreturned_items(self):
        return [i for i in self._items if not i.is_returned]