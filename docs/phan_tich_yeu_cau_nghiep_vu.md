# Phân tích yêu cầu nghiệp vụ

## 1. Bài toán

Hệ thống quản lý ba loại thiết bị (Điều khiển điều hòa, micro, điều khiển máy chiếu) phục vụ trường đại học. Giảng viên/trợ giảng lập phiếu mượn, mỗi phiếu có thể chứa nhiều thiết bị. Khi xảy ra các tình huống bất thường hay lỗi, hệ thống sử dụng ngoại lệ để thông báo lỗi, phải giữ cho dữ liệu nhất quán

## 2. Đối tượng và thuộc tính

- Thiết bị (Device): có mã (không rỗng, chỉ đặt khi khởi tạo), tên, năm đưa vào sử dụng (không lớn hơn năm hiện tại), giá mua (> 0), trạng thái. Mỗi loại thiết bị tự tính chi phí bảo trì/năm (đa hình).
- Phòng học (ClassRoom): kết tập nhiều thiết bị. Có mã (không thêm trùng mã, không thêm null), tên, sức chứa, danh sách thiết bị, tính tổng chi phí bảo trì bằng đa hình; lọc thiết bị cần bảo trì (đang bảo trì hoặc dùng trên 5 năm).
- Người mượn (IBorrower): Lecturer mượn tối đa 3 thiết bị/phiếu, TeachingAssistant tối đa 2.
- Phiếu mượn (BorrowingSlip) hợp thành các BorrowItem; BorrowItem chỉ tham chiếu thiết bị nên xóa phiếu không xóa thiết bị hay người mượn.
- Trả thiết bị: kiểm tra thiết bị có trong phiếu, chưa trả, ngày trả không trước ngày mượn; tính phí trả muộn = số ngày muộn × phí/ngày của thiết bị.

## 3. Thứ tự kiểm tra khi thêm thiết bị vào phiếu

(1) thiết bị không null → (2) số ngày mượn hợp lệ (> 0 và không vượt giới hạn thiết bị), tiết mượn hợp lệ → (3) chưa có trong phiếu → (4) người mượn chưa đạt giới hạn → (5) thiết bị đang Available. Chỉ khi tất cả hợp lệ mới tạo BorrowItem, đổi trạng thái thiết bị thành Borrowed rồi thêm vào danh sách. Nhờ vậy nếu lỗi thì dữ liệu sẽ nhất quán (không vị thay đổi)

## 4. Một số điểm chưa rõ và quyết định

- Yêu cầu có hai enum trạng thái -> gộp thành một DeviceStatus (Available, Borrowed, UnderMaintenance, Retired)
- Vừa nói “số tiết” vừa nói “số ngày” tối đa → mỗi thiết bị có MaxBorrowDays (giới hạn số ngày) và MaxPeriods (giới hạn số tiết); BorrowItem lưu thêm từ tiết – đến tiết.
- Python không có interface → dùng lớp trừu tượng ABC cho IBorrower; thuộc tính chỉ đọc dùng @property không có setter.
- Bổ sung ngoại lệ InvalidReturnDateException để phân biệt lỗi “ngày trả trước ngày mượn” với các lỗi khác.
