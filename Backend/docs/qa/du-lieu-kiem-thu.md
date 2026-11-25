# Bộ dữ liệu kiểm thử (5)

| Mã | Bộ dữ liệu | Nguồn | Dùng ở |
|---|---|---|---|
| DL-01 | Tài khoản mẫu theo vai trò | Tạo tự động khi backend khởi động (`AdminUserInitializer`, `DemoAccountInitializer`) | Mọi case |
| DL-02 | Căn hộ mẫu | Tạo tự động khi bảng căn hộ trống (`ApartmentConfig`) | CN-14…19, TH-01, TH-02, TH-06, TH-07 |
| DL-03 | Dữ liệu đăng ký và đặt lại mật khẩu | Do script kiểm thử gửi | CN-01…09, CN-15, TH-01, GD-05 |
| DL-04 | Bảng đơn giá và chỉ số điện nước | Do script kiểm thử gửi | CN-20, CN-21, CN-25, TH-03, GD-17, GD-18 |
| DL-05 | Khoản thu và đợt đóng góp | Do script kiểm thử gửi | CN-22…24, CN-28…30, TH-04, TH-05, TH-07, GD-13…16 |

## DL-01 Tài khoản mẫu

| Tên đăng nhập | Mật khẩu | Vai trò | Căn hộ | Trạng thái | Mục đích |
|---|---|---|---|---|---|
| `admin` | `1234567890` | ADMIN (super admin) | – | Hoạt động | Quản trị toàn quyền |
| `ketoan` | `Ketoan@123` | ADMIN | – | Hoạt động | Kiểm tra quyền của ADMIN thường (TH-08) |
| `cudan01` | `Cudan01@123` | USER | `A0012` | Hoạt động | Cư dân một căn hộ |
| `cudan02` | `Cudan02@123` | USER | `A0023`, `A0024` | Hoạt động | Cư dân nhiều căn hộ |
| `cudankhoa` | `Cudankhoa@123` | USER | – | Đã vô hiệu hóa | Kiểm tra đăng nhập bị chặn (CN-05) |

Email của tài khoản mẫu dùng tên miền `bluemoon.test`, nên OTP không bao giờ gửi tới hộp thư thật.

## DL-02 Căn hộ mẫu

- 50 căn hộ `A0001`–`A0050`, 10 tầng, mỗi tầng 5 căn, đều ở trạng thái `VACANT` khi mới tạo.
- Tầng 1 (`A0001`–`A0005`) loại `KIOT`, 20–40 m², 1 phòng; tầng 2–10 loại `STANDARD`, 45–90 m², 2–3 phòng. Diện tích sinh ngẫu nhiên, nên số tiền phí theo m² khác nhau giữa các lần khởi động.
- Khi tạo tài khoản mẫu, `A0012`, `A0023`, `A0024` có cư dân và chuyển sang `RENT`, kèm 3 khoản phí tự sinh mỗi căn.
- Căn hộ do kiểm thử dùng thêm: `A0031` (gắn cư dân CN-14), `A0035` (đăng ký kèm căn hộ TH-01), `A0041`/`A0042` (đổi trạng thái hàng loạt CN-17), `B0101` (căn hộ mới CN-16).

## DL-03 Đăng ký và đặt lại mật khẩu

Quy tắc mật khẩu của backend (Passay): 8–16 ký tự, có ít nhất 1 chữ hoa, 1 chữ thường, 1 chữ số, 1 ký tự đặc biệt, không có khoảng trắng, không chứa dãy số liên tiếp như `12345`.

| Loại | Giá trị | Kết quả mong đợi |
|---|---|---|
| Mật khẩu hợp lệ | `Dangky@123`, `MoiMoi@123`, `DatLai@123`, `CuDan@1234` | Chấp nhận |
| Mật khẩu không hợp lệ | `abc12345` (thiếu chữ hoa, ký tự đặc biệt, có dãy `12345`), `yeu` (quá ngắn) | Từ chối, báo lỗi ở trường `password` |
| Số điện thoại | `0912000001` (10 chữ số) hợp lệ; `091200` không hợp lệ | Không hợp lệ thì báo "Phone must be 10 digits" |
| Email | Mỗi case một địa chỉ riêng `qa.<mã case>@bluemoon.test` | Tránh giới hạn 3 OTP trong 15 phút cho mỗi email |
| OTP | Lấy mã 6 chữ số trong email ghi ở log SMTP giả; OTP sai dùng `000000` (hoặc `111111` nếu OTP thật là `000000`) | |

## DL-04 Đơn giá và chỉ số điện nước

| Dữ liệu | Giá trị |
|---|---|
| Đơn giá mặc định khi tạo bảng | Căn hộ 300.000 đ/m², dịch vụ 15.000 đ/m², nước 15.000 đ/m³, điện 3.500 đ/kWh, gửi xe 0 |
| Đơn giá CN-20 | Điện 3.800, nước 18.000, gửi xe 120.000 đ/tháng và 5.000 đ/giờ |
| Đơn giá TH-03 | Điện 4.200 đ/kWh |
| Đơn giá không hợp lệ | Gửi xe theo giờ -1.000 (CN-21, GD-18) |
| Chỉ số CN-25 | `A0012`: 120 kWh, 8 m³ → 456.000 đ và 144.000 đ; `A0023`: 75 kWh, ô nước để trống → 285.000 đ, không tạo khoản nước |
| Chỉ số TH-03 | `A0024`: 10 kWh → 42.000 đ |

## DL-05 Khoản thu và đợt đóng góp

| Dữ liệu | Giá trị |
|---|---|
| Khoản thu hợp lệ | `A0012`, `SERVICE_COST`, "QA phí dịch vụ tháng 11", 350.000 đ, hạn đóng là ngày chạy kiểm thử |
| Khoản thu không hợp lệ | Căn hộ `1`; số tiền 0; hạn đóng hôm qua |
| Khoản thu để sửa và xóa | `A0024`, `OTHER`, 50.000 đ, sửa thành 65.000 đ |
| Khoản thu tích hợp | `A0012`, "QA phí sửa thang máy", 90.000 đ |
| Khoản thu từ giao diện | `A0002`, `FIXED_COST`, "GD14 kiem thu", 15.000 đ, hạn 30/11/2026 |
| Loại đóng góp | "QA Quỹ khuyến học" |
| Đợt đóng góp | "QA Khuyến học cuối năm", mục tiêu 20.000.000 đ; "QA Quỹ vì người nghèo", mục tiêu 5.000.000 đ, mỗi căn hộ 100.000 đ |
