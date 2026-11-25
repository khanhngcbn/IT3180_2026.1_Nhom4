# BC-02 – Ghi nhận khi kiểm thử giao diện

Ngày 26/11/2026, trình duyệt Chromium, frontend `http://localhost:3000` (React dev server) nối tới backend dùng cho đợt kiểm thử (cùng database với BC-01, chạy ngay sau BC-01). Giá trị dưới đây đọc trực tiếp từ trang (DOM) hoặc từ API ngay sau thao tác, không chép lại theo trí nhớ.

| Case | Thao tác | Giá trị quan sát được | Kết quả |
|---|---|---|---|
| GD-01 | Mở `/auth/sign-in` | Các ô: `email:mail@simmmple.com`, `password:Min. 8 characters`, `checkbox`; có nhãn Username, Password, nút Sign In, "Forgot password?", "Create an Account" | Không đạt (LOI-09): ô Username có kiểu email và gợi ý địa chỉ email |
| GD-02 | `admin` + mật khẩu sai, bấm Sign In | Ở `/auth/sign-in`, không có token, hiện "Error: You provided wrong information!" | Đạt |
| GD-03 | `admin` + mật khẩu đúng | Chuyển tới `/admin/data-tables`; menu: Admin Main Dashboard, Profile, Apartment Management, Resident Management, Bill Management, Contributions Management, Fee Unit Management, Utility Bills Creation | Đạt |
| GD-04 | Mở `/auth/sign-up` | Nhãn: Username, Password, Email, Phone, Full name, Age, Gender; ô Username `type="email"`; trình đọc trợ năng gọi ô Phone là "Username", ô Age là "Full name" | Đạt (ghi chú nhãn sai vào LOI-09) |
| GD-05 | Đăng ký `qa_gd05`, mật khẩu `abc12345`, SĐT `091200` | Ở lại `/auth/sign-up`; hiện "Password must contain 1 or more uppercase characters. Password must contain 1 or more special characters. Password contains the illegal numerical sequence '12345'." và "Phone must be 10 digits" | Đạt |
| GD-06 | Mở `/auth/forgot-password` | Nhãn Username, ô `text:nguyenvana123`, nút Submit, nút "Sign in with Google". Bấm "Sign in with Google": không đổi URL, không có request, không có thông báo | Đạt (ghi nhận LOI-13) |
| GD-07 | Trang chủ admin | 5 dòng; đầu tiên "28/11/2026 18:00 Ngày hội văn hóa", cuối "20/12/2026 16:00 Ngày hội gia đình" | Đạt |
| GD-08 | Bấm "Xem thêm sự kiện" | 10 dòng, ngày tăng dần, dòng cuối "17/01/2027 16:00 Ngày hội gia đình" | Đạt |
| GD-09 | Mở `/admin/apartment` | Cột: SELECT, ID, APARTMENT NUMBER, ROOM NUMBER, AREA (M²), FLOOR, STATUS, TYPE, OPTIONS; 5 dòng mỗi trang, phân trang 1–5; dòng đầu "A0001 1 36 1 VACANT KIOT" | Đạt |
| GD-10 | Tìm nút thêm căn hộ | Nút có trên trang: Filter, Select All, Set Status, Previous, 1–5, Next. Không có nút tạo căn hộ | Không đạt (LOI-07) |
| GD-11 | Mở `/admin/resident` | Nút: New Account, Filter, Select All, Activate, Deactivate, Delete, Export | Đạt |
| GD-12 | Chọn dòng `cudan01`, bấm Deactivate | Hộp thoại "Confirm Deactivation – Are you sure you want to deactivate 1 users? Deactivated accounts cannot sign in and are removed from their apartments."; bấm Cancel: dòng vẫn "Activated", API trả `activation: true` | Đạt |
| GD-13 | Bấm New Bill | Nhãn: Apartment Number, Bill Type, Due Date, Description, Amount (VND); ô hạn đóng `type=date`, `min=2026-11-26`; ô số tiền `type=number`; 51 căn hộ gợi ý (50 căn mẫu + `B0101`); loại: FIXED_COST, SERVICE_COST, ELECTRICITY, WATER, OTHER | Đạt |
| GD-14 | Căn hộ `1`, hạn 30/11/2026, mô tả "GD14 kiem thu", 15.000, bấm Save | Form hiện "Số căn hộ không tồn tại trong hệ thống" | Đạt |
| GD-15 | Đổi căn hộ thành `A0002`, bấm Save | Thông báo "Creation Successful!"; API: `A0002`, 15000, `2026-11-30`, `UNPAID` | Đạt |
| GD-16 | Gõ `A0002` vào ô tìm kiếm | Bảng còn 1 dòng: "A0002 FIXED_COST 15000 2026-11-30 GD14 kiem thu UNPAID" | Đạt |
| GD-17 | Mở `/admin/fee-units` | 3 nhóm Apartment/Utility/Parking Fee Settings; 6 ô: 300000, 15000, 18000, 4200, 120000, 5000 (khớp API sau CN-20 và TH-03) | Đạt |
| GD-18 | Nhập -1000 vào Hourly Parking, Save Changes | Ô tự đổi thành 0; thông báo "Success – Fee unit settings saved successfully"; API trả `parkingFeePerHour: 0` (giá cũ 5000 bị mất) | Không đạt (LOI-08) |
| GD-19 | Mở `/admin/utility-bills` | "Water: ₫18,000/m³", "Electricity: ₫4,200/kWh"; căn hộ có cư dân: A0012 (Phạm Văn B), A0023, A0024 (Nguyễn Thị C), A0031 (Hộ thử nghiệm). Không có A0035 dù có cư dân đăng ký ở TH-01 | Đạt (A0035 thiếu do LOI-02) |
| GD-20 | Mở `/admin/contributions` | Tab: Contributions, User Contributions, Contribution Types; thấy "QA Khuyến học cuối năm", "QA Quỹ vì người nghèo", loại "QA Quỹ khuyến học" | Đạt |
| GD-21 | Đăng xuất, đăng nhập `cudan01` | Chuyển tới `/user/profile`; menu: User Profile, User Homepage, Bill Payment Service, Contribution Service | Đạt |
| GD-22 | Mở `/user/payment` | Chỉ có căn hộ A0012; 5 dòng mỗi trang, ví dụ "Fixed Cost 15900000 2026-12-06 phí thuê căn hộ A0012A0012 Unpaid" | Đạt (mô tả lặp số căn hộ ghi ở LOI-11) |
| GD-23 | Đang là `cudan01`, gõ `/admin/bill` | Trang mở được; có menu quản trị (liên kết `/admin/fee-units`) và nút New Bill; bảng 0 dòng | Không đạt (LOI-10) |
| GD-24 | `/user/profile-user`, bấm "Change password" | Hộp thoại "Change your password", ô `oldPassword`, `newPassword`; nhãn Old Password, New Password | Đạt |

Tổng: 20 đạt, 4 không đạt (GD-01, GD-10, GD-18, GD-23).
