# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************

from device_status import DeviceStatus


class BorrowingException(Exception):
    """Ngoại lệ cơ sở của toàn bộ nghiệp vụ mượn trả."""

    def __init__(self, message, inner_exception=None):
        super().__init__(message)
        self.inner_exception = inner_exception  # ngoại lệ gốc (nếu có)


class DeviceUnavailableException(BorrowingException):
    """Thiết bị không ở trạng thái Available."""

    def __init__(self, device_id, current_status):
        super().__init__(
            f"Thiết bị {device_id} không sẵn sàng (trạng thái: {current_status.value})")
        self.device_id = device_id
        self.current_status = current_status


class BorrowLimitExceededException(BorrowingException):
    """Người mượn đã đạt số thiết bị tối đa."""

    def __init__(self, borrower_id, maximum_devices):
        super().__init__(
            f"Người mượn {borrower_id} đã đạt giới hạn {maximum_devices} thiết bị/phiếu")
        self.borrower_id = borrower_id
        self.maximum_devices = maximum_devices


class InvalidBorrowPeriodException(BorrowingException):
    """Số ngày mượn (hoặc tiết mượn) không hợp lệ."""

    def __init__(self, device_id, requested, maximum, message=None):
        super().__init__(message or
                         f"Thiết bị {device_id}: yêu cầu {requested}, tối đa {maximum}")
        self.device_id = device_id
        self.requested = requested
        self.maximum = maximum


class DuplicateDeviceException(BorrowingException):
    """Thiết bị đã tồn tại trong phiếu (hoặc trong phòng)."""

    def __init__(self, device_id):
        super().__init__(f"Thiết bị {device_id} đã tồn tại, không thể thêm lần nữa")
        self.device_id = device_id


class DeviceNotInSlipException(BorrowingException):
    """Trả thiết bị không thuộc phiếu mượn."""

    def __init__(self, device_id, slip_id):
        super().__init__(f"Thiết bị {device_id} không thuộc phiếu {slip_id}")
        self.device_id = device_id
        self.slip_id = slip_id


class DeviceAlreadyReturnedException(BorrowingException):
    """Thiết bị trong phiếu đã được trả trước đó."""

    def __init__(self, device_id):
        super().__init__(f"Thiết bị {device_id} đã được trả trước đó")
        self.device_id = device_id


class InvalidReturnDateException(BorrowingException):
    """Ngày trả trước ngày mượn (ngoại lệ bổ sung: để phân biệt lỗi ngày trả)."""

    def __init__(self, device_id, borrowed_date, returned_date):
        super().__init__(
            f"Thiết bị {device_id}: ngày trả {returned_date:%d/%m/%Y} "
            f"trước ngày mượn {borrowed_date:%d/%m/%Y}")
        self.device_id = device_id