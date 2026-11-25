# Test case tích hợp (8)

Mỗi case kiểm tra dữ liệu đi qua ít nhất hai module: tài khoản, cư dân, căn hộ, đơn giá, khoản thu, đóng góp. Các case chạy tự động cùng script [tu-dong/kiem_thu_api.py](tu-dong/kiem_thu_api.py), ngay sau 30 case chức năng và dùng dữ liệu do chúng tạo ra.

| Mã | Module liên quan | Tên | Bước | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|:---:|
| TH-01 | Đăng ký (US21) → Căn hộ (US02) → Khoản thu (US08) | Cư dân tự đăng ký kèm căn hộ được gắn vào căn hộ | Đăng ký `qa_th01` kèm căn hộ `A0035`, xác minh OTP; admin xem cư dân của `A0035`; `qa_th01` xem khoản thu | `A0035` có cư dân mới, chuyển sang `RENT` giống như khi admin thêm cư dân (TH-02) | C |
| TH-02 | Hồ sơ cư dân (US01) → Căn hộ (US02) → Khoản thu (US06) | Gắn cư dân đầu tiên làm căn hộ đổi trạng thái và sinh phí | Dùng kết quả CN-14 (`qa_cn14` vào `A0031` đang trống); xem căn hộ và khoản thu của `A0031` | `A0031` chuyển `RENT`; có đúng 3 khoản phí tự sinh: thuê, dịch vụ, quản lý | C |
| TH-03 | Đơn giá (US05) → Điện nước (US07) | Khoản thu điện dùng đơn giá mới nhất | Đổi giá điện thành 4.200 đ/kWh; tạo khoản điện 10 kWh cho `A0024` (ô nước để trống) | Số tiền = 42.000 đ | C |
| TH-04 | Khoản thu (US06) → Cư dân xem (US08) | Khoản thu mới chỉ hiện cho đúng căn hộ | Admin tạo "QA phí sửa thang máy" cho `A0012`; `cudan01` và `cudan02` xem danh sách khoản thu | `cudan01` thấy khoản này, `cudan02` không thấy | C |
| TH-05 | Xác nhận thanh toán (US12) → Cư dân xem (US08) | Cư dân thấy trạng thái đã thanh toán | Sau CN-28, `cudan01` xem lại khoản thu đã xác nhận | Khoản thu hiện trạng thái `PAID` phía cư dân | C |
| TH-06 | Quản trị tài khoản (US23) → Căn hộ (US02) | Khóa tài khoản gỡ cư dân khỏi căn hộ, mở lại thì gắn lại | Vô hiệu hóa `qa_cn14`, đếm cư dân của `A0031`; kích hoạt lại, đếm lại | Sau khi khóa: 0 cư dân; sau khi mở: 1 cư dân. Hộp thoại xác nhận khóa trên giao diện ghi đúng hành vi này | TB |
| TH-07 | Đóng góp (US15) → Căn hộ (US02) → Cư dân (US01) | Tạo khoản đóng góp cho mọi căn hộ đang có cư dân | Tạo đợt "QA Quỹ vì người nghèo"; `POST /api/contributions/admin/create-for-all?amount=100000`; so sánh căn hộ nhận khoản với căn hộ đang có cư dân | Hai danh sách trùng khớp | TB |
| TH-08 | Phân quyền (US23) giữa super admin và ADMIN thường | Kế toán không khóa được super admin | `ketoan` (ADMIN thường) gọi khóa hàng loạt và khóa đơn lẻ tài khoản `admin`; thử đăng nhập `admin` | Cả hai đường đều bị từ chối; `admin` vẫn đăng nhập được | C |

Nếu TH-08 làm khóa `admin`, script tự kích hoạt lại bằng tài khoản `ketoan` để các lần chạy sau không bị ảnh hưởng.
