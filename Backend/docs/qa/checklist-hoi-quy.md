# Checklist kiểm thử hồi quy

Dùng sau mỗi lần sửa lỗi hoặc trước mỗi lần bàn giao. Người kiểm thử (Nguyễn Hoàng Giang) đánh dấu từng mục; người duyệt (Nguyễn Đình Nam Khánh) chỉ ký nghiệm thu khi mọi mục bắt buộc đã đạt.

Cột **Lần 26/11/2026** ghi kết quả của đợt kiểm thử đầu tiên, để lần sau so sánh.

## A. Chuẩn bị (bắt buộc)

| # | Việc | Lần 26/11/2026 |
|---|---|:---:|
| A1 | Lấy mã mới nhất của nhánh `main`, ghi lại mã commit vào báo cáo | ✅ `4ffb52e` |
| A2 | `./mvnw test` trong `Backend` báo `BUILD SUCCESS`, không có test lỗi | ✅ 9/9 |
| A3 | Khởi động SMTP giả `python scripts/smtp_stub.py <mail.log>` | ✅ |
| A4 | Khởi động backend với database mới; log có dòng tạo tài khoản mẫu `ketoan`, `cudan01`, `cudan02`, `cudankhoa` | ✅ |
| A5 | Chạy `python docs/qa/tu-dong/kiem_thu_api.py <mail.log> <ket-qua.json> <địa chỉ backend>`, lưu đầu ra làm bằng chứng | ✅ 33/38 |
| A6 | Frontend `npm start`, đăng nhập được bằng `admin` | ✅ |

## B. Xác nhận lỗi đã sửa (làm khi có bản sửa)

| # | Lỗi | Cách xác nhận | Lần 26/11/2026 |
|---|---|---|:---:|
| B1 | LOI-01 | TH-08 đạt; thử thêm `activate`, `delete`, `edit` đơn lẻ bằng `ketoan` lên tài khoản `admin` đều bị từ chối | ❌ |
| B2 | LOI-02 | TH-01 đạt; căn hộ đăng ký kèm chuyển `RENT` và sinh 3 khoản phí | ❌ |
| B3 | LOI-03 | TH-06 đạt; hồ sơ cư dân vẫn giữ căn hộ sau khi khóa rồi mở lại | ❌ |
| B4 | LOI-04 | TH-07 đạt | ❌ |
| B5 | LOI-05, LOI-06 | CN-16 đạt: trạng thái căn hộ mới đúng như nhập; thêm trùng số trả 400 | ❌ |
| B6 | LOI-07 | GD-10 đạt: thêm được căn hộ từ màn Apartment Management | ❌ |
| B7 | LOI-08 | GD-18 đạt: nhập giá âm thì báo lỗi, giá cũ giữ nguyên | ❌ |
| B8 | LOI-09 | GD-01 đạt: ô Username là ô chữ, gợi ý tên đăng nhập | ❌ |
| B9 | LOI-10 | GD-23 đạt: cư dân gõ `/admin/...` bị chuyển về trang cư dân | ❌ |
| B10 | LOI-11, LOI-12, LOI-13 | Mô tả khoản phí đúng dạng "phí thuê căn hộ A0012"; log khởi động ghi đúng 50 căn hộ; nút Google bị ẩn hoặc có chức năng | ❌ |

## C. Hồi quy các phần đang chạy đúng (bắt buộc)

Các mục dưới đây đã đạt ở lần 26/11/2026; lần sau phải vẫn đạt.

| # | Chức năng | Case | Lần 26/11/2026 |
|---|---|---|:---:|
| C1 | Đăng ký, OTP sai, gửi lại OTP | CN-01, CN-02, CN-03, GD-05 | ✅ |
| C2 | Đăng nhập, JWT, tài khoản bị khóa không vào được | CN-04, CN-05, GD-02, GD-03, GD-21 | ✅ |
| C3 | Đổi mật khẩu, quên mật khẩu, chặn OTP của email khác, hủy OTP sau 3 lần sai | CN-06…09 | ✅ |
| C4 | Đổi vai trò, khóa/mở đơn lẻ, khóa hàng loạt bỏ qua `admin` | CN-10, CN-11, CN-12, GD-12 | ✅ |
| C5 | Cư dân và người chưa đăng nhập bị chặn ở API quản trị | CN-13, CN-27 | ✅ |
| C6 | Thêm cư dân gắn căn hộ, căn hộ chuyển `RENT` và sinh phí | CN-14, CN-15, TH-02 | ✅ |
| C7 | Đổi trạng thái căn hộ hàng loạt, lọc căn hộ, xem cư dân | CN-17, CN-18, CN-19, GD-09 | ✅ |
| C8 | Lưu bảng đơn giá gồm gửi xe; backend chặn giá âm | CN-20, CN-21, GD-17 | ✅ |
| C9 | Tạo, tìm, sửa, xóa khoản thu; thông báo lỗi theo trường | CN-22, CN-23, CN-24, GD-13…16 | ✅ |
| C10 | Khoản thu điện nước hàng loạt dùng đơn giá mới | CN-25, TH-03, GD-19 | ✅ |
| C11 | Cư dân chỉ thấy khoản thu căn hộ mình, thấy trạng thái đã thanh toán | CN-26, TH-04, TH-05, GD-22 | ✅ |
| C12 | Xác nhận thanh toán tiền mặt, không xác nhận hai lần | CN-28 | ✅ |
| C13 | Loại và đợt đóng góp, đóng/hủy/mở lại | CN-29, CN-30, GD-20 | ✅ |
| C14 | Sự kiện sắp tới theo ngày hiện tại, xem thêm sự kiện | GD-07, GD-08 | ✅ |
| C15 | Đổi mật khẩu trên giao diện, màn quên mật khẩu | GD-06, GD-24 | ✅ |

## D. Kết luận lần chạy

| Lần | Ngày | Người kiểm thử | Mục B đạt | Mục C đạt | Đề xuất của kiểm thử | Quyết định của người duyệt |
|---|---|---|:---:|:---:|---|---|
| 1 | 26/11/2026 | Nguyễn Hoàng Giang | 0/10 (chưa sửa) | 15/15 | Chưa nghiệm thu, chờ sửa LOI-01…LOI-04 | (Nguyễn Đình Nam Khánh điền) |
