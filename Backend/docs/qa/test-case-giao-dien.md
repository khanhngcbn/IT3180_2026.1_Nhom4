# Test case giao diện (24)

Kiểm thử trên trình duyệt tại `http://localhost:3000`, thao tác như người dùng thật (gõ phím, bấm nút). Sau mỗi thao tác, đối chiếu nội dung hiển thị với dữ liệu trả về từ API. Giá trị quan sát được ghi ở [bằng chứng BC-02](bang-chung/BC-02-kiem-thu-giao-dien.md).

**Tiền điều kiện:** đã chạy xong bộ API ([CN](test-case-chuc-nang.md), [TH](test-case-tich-hop.md)) trên cùng backend, nên có sẵn khoản thu, đợt đóng góp và căn hộ `B0101`.

## Xác thực

| Mã | Màn hình | Tên | Bước | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|:---:|
| GD-01 | Sign In | Bố cục màn đăng nhập | Mở `/auth/sign-in` khi chưa đăng nhập | Có ô Username, ô Password, nút **Sign In**, liên kết **Forgot password?** và **Create an Account**. Ô Username gợi ý đúng loại dữ liệu cần nhập (tên đăng nhập, không phải email) | TB |
| GD-02 | Sign In | Báo lỗi khi đăng nhập sai | Nhập `admin` và mật khẩu sai, bấm **Sign In** | Ở lại màn đăng nhập, hiện thông báo lỗi, không lưu token | C |
| GD-03 | Sign In → Admin | Đăng nhập Ban quản lý | Nhập `admin` / mật khẩu đúng, bấm **Sign In** | Chuyển tới `/admin/data-tables`; menu có đủ 8 mục quản trị | C |
| GD-04 | Sign Up | Bố cục màn đăng ký | Mở `/auth/sign-up` | Có các ô bắt buộc: Username, Password, Email, Phone, Full name, Age, Gender | TB |
| GD-05 | Sign Up | Báo lỗi theo từng ô khi đăng ký sai | Nhập mật khẩu `abc12345` và số điện thoại `091200`, các ô khác hợp lệ, bấm **Sign Up** | Ở lại màn đăng ký; hiện lỗi mật khẩu (thiếu chữ hoa, ký tự đặc biệt, có dãy số `12345`) và lỗi "Phone must be 10 digits" | C |
| GD-06 | Forgot password | Bố cục màn quên mật khẩu | Mở `/auth/forgot-password` | Có ô Username và nút **Submit** | T |

## Trang chủ

| Mã | Màn hình | Tên | Bước | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|:---:|
| GD-07 | Admin Main Dashboard | Sự kiện sắp tới theo ngày thực | Đăng nhập `admin`, xem bảng "Sự kiện sắp tới" | Hiện 5 sự kiện, ngày đầu tiên không trước hôm nay, mỗi dòng có ngày và giờ | TB |
| GD-08 | Admin Main Dashboard | Xem thêm sự kiện | Bấm **Xem thêm sự kiện** | Bảng tăng lên 10 sự kiện, sắp xếp theo ngày tăng dần | T |

## Căn hộ và tài khoản

| Mã | Màn hình | Tên | Bước | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|:---:|
| GD-09 | Apartment Management | Bảng căn hộ | Mở `/admin/apartment` | Bảng có cột số căn hộ, số phòng, diện tích, tầng, trạng thái, loại; chia trang; có nút **Filter** và **Set Status** | TB |
| GD-10 | Apartment Management | Thêm căn hộ từ giao diện | Tìm nút thêm căn hộ mới trên màn hình | Có nút mở form tạo căn hộ (US02) | C |
| GD-11 | Resident Management | Thanh công cụ quản lý tài khoản | Mở `/admin/resident` | Có các nút **New Account**, **Filter**, **Select All**, **Activate**, **Deactivate**, **Delete**, **Export** | TB |
| GD-12 | Resident Management | Hộp thoại xác nhận vô hiệu hóa | Chọn `cudan01`, bấm **Deactivate**, sau đó bấm **Cancel** | Hiện hộp thoại "Confirm Deactivation" ghi số tài khoản được chọn; bấm Cancel thì tài khoản vẫn `Activated` | TB |

## Khoản thu, đơn giá, điện nước, đóng góp

| Mã | Màn hình | Tên | Bước | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|:---:|
| GD-13 | Bill Management | Form tạo khoản thu | Bấm **New Bill** | Form có 5 ô bắt buộc; số tiền ghi đơn vị VND; hạn đóng chọn bằng lịch, không chọn được ngày trước hôm nay; ô căn hộ gợi ý danh sách căn hộ; có 5 loại khoản thu | C |
| GD-14 | Bill Management | Báo lỗi căn hộ không tồn tại | Nhập căn hộ `1`, hạn 30/11/2026, mô tả, số tiền 15.000, bấm **Save** | Form hiện "Số căn hộ không tồn tại trong hệ thống", không tạo khoản thu | C |
| GD-15 | Bill Management | Tạo khoản thu thành công | Sửa căn hộ thành `A0002`, bấm **Save** | Hiện "Creation Successful!"; khoản thu được lưu với trạng thái `UNPAID` | C |
| GD-16 | Bill Management | Tìm kiếm khoản thu | Gõ `A0002` vào ô tìm kiếm | Bảng chỉ còn khoản thu của `A0002` | TB |
| GD-17 | Fee Unit Management | Bố cục bảng đơn giá | Mở `/admin/fee-units` | Có 3 nhóm: Apartment Fee, Utility Fee, Parking Fee, với 6 ô giá có đơn vị; giá hiển thị khớp với `GET /api/fee-units` | TB |
| GD-18 | Fee Unit Management | Nhập đơn giá âm | Nhập -1000 vào ô Hourly Parking, bấm **Save Changes** | Báo lỗi, không lưu; giá cũ giữ nguyên | TB |
| GD-19 | Utility Bills Creation | Màn nhập chỉ số điện nước | Mở `/admin/utility-bills` | Hiện đơn giá điện, nước hiện hành và danh sách căn hộ đang có cư dân để nhập chỉ số | TB |
| GD-20 | Contributions Management | Màn đóng góp | Mở `/admin/contributions` | Có 3 tab Contributions, User Contributions, Contribution Types; hiện các đợt và loại đóng góp đã tạo | TB |

## Cư dân

| Mã | Màn hình | Tên | Bước | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|:---:|
| GD-21 | Sign In → User | Đăng nhập cư dân | Đăng xuất, đăng nhập `cudan01` | Chuyển tới `/user/profile`; menu có 4 mục của cư dân, không có mục quản trị | C |
| GD-22 | Bill Payment Service | Cư dân xem khoản phải thu | Mở `/user/payment` | Chỉ hiện khoản thu của căn hộ `A0012`, có số tiền, hạn đóng, trạng thái | C |
| GD-23 | Admin (URL trực tiếp) | Cư dân không vào được trang quản trị | Đang đăng nhập `cudan01`, gõ thẳng `/admin/bill` | Bị chặn hoặc chuyển về trang của cư dân; không hiện menu và nút quản trị | TB |
| GD-24 | User Profile | Hộp thoại đổi mật khẩu | Mở `/user/profile-user`, bấm **Change password** | Hiện hộp thoại "Change your password" có ô Old Password và New Password | TB |
