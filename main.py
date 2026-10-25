# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************
from datetime import datetime, timedelta

from borrower import Lecturer, TeachingAssistant
from borrowing_slip import BorrowingSlip
from classroom import ClassRoom
from device import AirConRemote, Microphone, ProjectorRemote
from exceptions import BorrowingException

NGAY_MUON = datetime(2026, 10, 20)


def tao_thiet_bi():
    """Tạo bộ thiết bị mới cho mỗi tình huống (để các test không ảnh hưởng nhau)."""
    return (ProjectorRemote("PJ01", "Điều khiển máy chiếu", 2022, 500000),
            AirConRemote("AC01", "Điều khiển điều hòa", 2018, 300000),
            Microphone("MIC01", "Micro không dây", 2024, 1500000))


def luong_thanh_cong():
    print("===== 11.1. LUỒNG THÀNH CÔNG =====")
    gv = Lecturer("GV01", "Nguyễn Văn A")
    pj, ac, mic = tao_thiet_bi()

    # Phòng học chứa thiết bị (kết tập) + kiểm tra đa hình chi phí bảo trì
    phong = ClassRoom("P101", "Phòng D3-101", 60)
    for d in (pj, ac, mic):
        phong.add_device(d)
    print(f"Chi phí bảo trì dự kiến/năm của phòng: "
          f"{phong.calculate_annual_maintenance_cost():,.0f} VND")
    print("Thiết bị cần bảo trì (>5 năm hoặc đang bảo trì):",
          [d.device_id for d in phong.get_devices_requiring_maintenance()])

    phieu = BorrowingSlip("PM001", gv, "D3-101", NGAY_MUON)
    phieu.add_device(pj, 3, from_period=1, to_period=3)
    phieu.add_device(mic, 1, from_period=1, to_period=2)
    print("Sau khi thêm:", pj.status.value, "/", mic.status.value)

    # Trả đúng hạn
    phi = phieu.return_device("PJ01", NGAY_MUON + timedelta(days=3))
    print(f"Trả PJ01 đúng hạn, phí muộn: {phi:,.0f}")
    # Trả muộn 2 ngày (hạn là 1 ngày -> trả sau 3 ngày)
    phi = phieu.return_device("MIC01", NGAY_MUON + timedelta(days=3))
    print(f"Trả MIC01 muộn 2 ngày, phí muộn: {phi:,.0f}")

    print("Tổng phí muộn của phiếu:", f"{phieu.calculate_total_late_fee():,.0f}")
    print("Các dòng trả muộn:")
    for i in phieu.get_late_items():
        print("  -", i)
    print("Các dòng chưa trả:", [str(i) for i in phieu.get_unreturned_items()] or "không có")


def chay_tinh_huong(ten, ham):
    """Lớp ứng dụng: bắt ngoại lệ, thông báo và quyết định luồng xử lý."""
    print(f"\n--- {ten} ---")
    try:
        ham()
        print("KHÔNG có lỗi (không đúng mong đợi)")
    except BorrowingException as e:
        print(f"Bắt ngoại lệ {type(e).__name__}: {e}")
    except ValueError as e:
        print(f"Bắt ValueError: {e}")
    finally:
        print("(kết thúc tình huống)")   # luôn chạy dù có lỗi hay không


def luong_ngoai_le():
    print("\n===== 11.2. LUỒNG PHÁT SINH NGOẠI LỆ =====")

    # 1. Mượn điều khiển điều hòa đang bảo trì
    def t1():
        gv = Lecturer("GV01", "Nguyễn Văn A")
        _, ac, _ = tao_thiet_bi()
        ac.send_to_maintenance()
        BorrowingSlip("PM002", gv, "D3-101", NGAY_MUON).add_device(ac, 2)
    chay_tinh_huong("1. Mượn thiết bị đang UnderMaintenance", t1)

    # 2. Trợ giảng mượn thiết bị thứ ba (giới hạn 2)
    def t2():
        ta = TeachingAssistant("TG01", "Trần Thị B")
        pj, ac, mic = tao_thiet_bi()
        phieu = BorrowingSlip("PM003", ta, "D3-102", NGAY_MUON)
        phieu.add_device(pj, 1)
        phieu.add_device(ac, 1)
        try:
            phieu.add_device(mic, 1)
        finally:
            print("   Số dòng trong phiếu:", len(phieu.items),
                  "| trạng thái micro:", mic.status.value)  # phải giữ nguyên
    chay_tinh_huong("2. Trợ giảng mượn thiết bị thứ 3", t2)

    # 3. Thêm cùng một micro hai lần
    def t3():
        gv = Lecturer("GV01", "Nguyễn Văn A")
        _, _, mic = tao_thiet_bi()
        phieu = BorrowingSlip("PM004", gv, "D3-101", NGAY_MUON)
        phieu.add_device(mic, 1)
        phieu.add_device(mic, 1)
    chay_tinh_huong("3. Thêm cùng một micro hai lần", t3)

    # 4. Mượn micro 3 ngày (giới hạn 1 ngày)
    def t4():
        gv = Lecturer("GV01", "Nguyễn Văn A")
        _, _, mic = tao_thiet_bi()
        phieu = BorrowingSlip("PM005", gv, "D3-101", NGAY_MUON)
        try:
            phieu.add_device(mic, 3)
        finally:
            print("   Trạng thái micro sau lỗi:", mic.status.value)  # vẫn Available
    chay_tinh_huong("4. Mượn micro 3 ngày (tối đa 1 ngày)", t4)

    # 5. Trả điều khiển máy chiếu không thuộc phiếu
    def t5():
        gv = Lecturer("GV01", "Nguyễn Văn A")
        pj, _, mic = tao_thiet_bi()
        phieu = BorrowingSlip("PM006", gv, "D3-101", NGAY_MUON)
        phieu.add_device(mic, 1)
        phieu.return_device(pj.device_id, NGAY_MUON + timedelta(days=1))
    chay_tinh_huong("5. Trả thiết bị không thuộc phiếu", t5)

    # 6. Trả cùng một thiết bị hai lần
    def t6():
        gv = Lecturer("GV01", "Nguyễn Văn A")
        pj, _, _ = tao_thiet_bi()
        phieu = BorrowingSlip("PM007", gv, "D3-101", NGAY_MUON)
        phieu.add_device(pj, 2)
        phieu.return_device("PJ01", NGAY_MUON + timedelta(days=1))
        phieu.return_device("PJ01", NGAY_MUON + timedelta(days=1))
    chay_tinh_huong("6. Trả cùng một thiết bị hai lần", t6)

    # 7. Ngày trả trước ngày mượn
    def t7():
        gv = Lecturer("GV01", "Nguyễn Văn A")
        pj, _, _ = tao_thiet_bi()
        phieu = BorrowingSlip("PM008", gv, "D3-101", NGAY_MUON)
        phieu.add_device(pj, 2)
        try:
            phieu.return_device("PJ01", NGAY_MUON - timedelta(days=1))
        finally:
            print("   Trạng thái thiết bị sau lỗi:", pj.status.value,
                  "| đã trả:", phieu.items[0].is_returned)  # vẫn Borrowed, chưa trả
    chay_tinh_huong("7. Ngày trả trước ngày mượn", t7)


if __name__ == "__main__":
    luong_thanh_cong()
    luong_ngoai_le()