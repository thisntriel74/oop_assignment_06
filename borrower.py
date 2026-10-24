# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************

from abc import ABC, abstractmethod


class IBorrower(ABC):
    """Interface người mượn (Python dùng lớp trừu tượng để mô phỏng interface)."""

    @property
    @abstractmethod
    def borrower_id(self):
        pass

    @property
    @abstractmethod
    def full_name(self):
        pass

    @abstractmethod
    def get_maximum_devices(self):
        pass


class Lecturer(IBorrower):
    """Giảng viên: tối đa 3 thiết bị/phiếu."""

    def __init__(self, borrower_id, full_name):
        self._borrower_id = borrower_id
        self._full_name = full_name

    @property
    def borrower_id(self):
        return self._borrower_id

    @property
    def full_name(self):
        return self._full_name

    def get_maximum_devices(self):
        return 3


class TeachingAssistant(IBorrower):
    """Trợ giảng: tối đa 2 thiết bị/phiếu."""

    def __init__(self, borrower_id, full_name):
        self._borrower_id = borrower_id
        self._full_name = full_name

    @property
    def borrower_id(self):
        return self._borrower_id

    @property
    def full_name(self):
        return self._full_name

    def get_maximum_devices(self):
        return 2