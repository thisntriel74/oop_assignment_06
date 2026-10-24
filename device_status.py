# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************

from enum import Enum


class DeviceStatus(Enum):
    """Trạng thái của thiết bị"""
    AVAILABLE = "Available"                  # Sẵn sàng cho mượn (có sẵn)
    BORROWED = "Borrowed"                    # Đang được mượn
    UNDER_MAINTENANCE = "UnderMaintenance"   # Đang bảo trì
    RETIRED = "Retired"                      # Đã thanh lý