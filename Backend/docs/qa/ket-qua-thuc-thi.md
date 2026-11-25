# Báo cáo thực thi kiểm thử – 26/11/2026

| Mục | Nội dung |
|---|---|
| Người thực hiện | Nguyễn Hoàng Giang (kiểm thử) |
| Người duyệt | Nguyễn Đình Nam Khánh |
| Mã nguồn | nhánh `main`, sau commit `4ffb52e` |
| Môi trường | Xem [kế hoạch kiểm thử, mục 5](ke-hoach-kiem-thu.md#5-môi-trường) |
| Đợt chạy API | 2026-11-26 05:20:44 → 2026-11-26 05:21:06, backend khởi động mới trước khi chạy |
| Đợt chạy giao diện | Ngay sau đợt API, trên cùng backend |

## Tổng hợp

| Nhóm | Số case | Đạt | Không đạt | Tỉ lệ đạt |
|---|:---:|:---:|:---:|:---:|
| Chức năng (CN) | 30 | 29 | 1 | 96.7% |
| Tích hợp (TH) | 8 | 4 | 4 | 50.0% |
| Giao diện (GD) | 24 | 20 | 4 | 83.3% |
| **Tổng** | **62** | **53** | **9** | **85.5%** |

Test đơn vị backend (`./mvnw test`): 9/9 đạt (BC-03).

## Ghi chú về lần chạy

- Trước lần chạy chính thức có một lần chạy thử. Ở lần đó, ngoài 5 lỗi thật, còn 2 case báo không đạt vì lỗi của chính script: CN-12 dùng một tài khoản chưa được tạo, TH-03 thiếu ô nước mà giao diện luôn gửi. Hai chỗ này đã sửa trong script, sau đó khởi động lại backend với database mới rồi mới chạy lần chính thức ghi trong báo cáo này.
- Case TH-08 đã khóa được `admin` (đúng lỗi LOI-01); script tự kích hoạt lại `admin` bằng tài khoản `ketoan` ngay sau đó.
- Kết quả giao diện GD-18 làm giá gửi xe theo giờ trong database thành 0 (đúng lỗi LOI-08).

## Chức năng (CN-01…CN-30)

Nguồn: [BC-01](bang-chung/BC-01-kiem-thu-api.txt). Cột "Thực tế ghi nhận" chép nguyên từ đầu ra của script.

| Mã | Tên | Kết quả | Thực tế ghi nhận | Thời gian (giây) | Lỗi |
|---|---|:---:|---|:---:|---|
| CN-01 | Đăng ký tài khoản hợp lệ và xác minh bằng OTP | Đạt | verify 200 {"message": "Xác thực thành công!"}; đăng nhập được | 2.36 |  |
| CN-02 | Đăng ký với dữ liệu sai định dạng bị từ chối | Đạt | 400 lỗi ở các trường ['password', 'phone'] | 0.02 |  |
| CN-03 | OTP sai bị từ chối, gửi lại OTP rồi nhập mã mới thì thành công | Đạt | OTP sai 400 ({"message": "OTP không đúng. Vui lòng thử lại!"}), gửi lại 200, OTP mới 200 | 3.9 |  |
| CN-04 | Đăng nhập đúng nhận JWT có vai trò tương ứng | Đạt | vai trò trong JWT: admin=ROLE_ADMIN, cudan01=ROLE_USER | 0.27 |  |
| CN-05 | Sai mật khẩu hoặc tài khoản bị khóa thì không đăng nhập được | Đạt | sai mật khẩu 401, tài khoản bị khóa 401 | 0.31 |  |
| CN-06 | Đổi mật khẩu phải nhập đúng mật khẩu cũ | Đạt | mật khẩu cũ sai 400 ({"error": "error_wrong_old_password"}), đúng 200; mật khẩu mới đăng nhập được | 0.87 |  |
| CN-07 | Quên mật khẩu: đặt lại bằng OTP gửi tới email đã đăng ký | Đạt | gửi OTP 200, đặt lại 200 {"message": "Password changed successfully", "success": true... | 2.28 |  |
| CN-08 | Không dùng được OTP của email khác để đặt lại mật khẩu | Đạt | 400 {"message": "Invalid OTP!", "success": false}; cudan02 vẫn dùng mật khẩu cũ: True | 1.81 |  |
| CN-09 | Nhập sai OTP 3 lần thì OTP bị hủy | Đạt | 3 lần sai [400, 400, 400], OTP đúng sau đó 400 | 2.24 |  |
| CN-10 | Ban quản lý đổi vai trò tài khoản | Đạt | 200 updated; vai trò sau khi đổi: ROLE_ADMIN | 0.35 |  |
| CN-11 | Vô hiệu hóa và kích hoạt lại một tài khoản | Đạt | khóa 200 (đăng nhập bị chặn: True), mở 200 (đăng nhập lại: True) | 0.34 |  |
| CN-12 | Vô hiệu hóa hàng loạt, bỏ qua tài khoản admin | Đạt | 200 {"deactivatedCount": 2, "success": true, "failedIds": [1]}; 2 tài khoản bị khóa: True; admin vẫn đăng nhập: True | 0.5 |  |
| CN-13 | Cư dân và người chưa đăng nhập không vào được API quản trị | Đạt | cư dân 403, không token 403, cư dân xem đơn giá 403 | 0.4 |  |
| CN-14 | Thêm hồ sơ cư dân và gắn với căn hộ | Đạt | 200 User added successfully; hồ sơ có căn hộ ['A0031']; căn hộ A0031 có 1 cư dân | 0.37 |  |
| CN-15 | Thêm cư dân với dữ liệu sai bị từ chối | Đạt | căn hộ sai 400 {"apartmentNumbers": "Apartment không tồn tại trong hệ thống...; mật khẩu yếu 400 | 0.11 |  |
| CN-16 | Thêm căn hộ mới với đủ thuộc tính | **Không đạt** | tạo 201; lưu được (tầng, diện tích, loại, trạng thái) = (11, 68.5, 'STANDARD', 'VACANT'); thêm trùng số căn hộ 500 Runtime Exception occurred: could not execute stat... | 0.17 | LOI-05, LOI-06 |
| CN-17 | Cập nhật trạng thái nhiều căn hộ cùng lúc | Đạt | cập nhật 200 -> OCCUPIED/OCCUPIED; trạng thái không hợp lệ 400 | 0.16 |  |
| CN-18 | Lọc căn hộ theo tầng, trạng thái và loại | Đạt | 200 kết quả ['A0001', 'A0002', 'A0003', 'A0004', 'A0005'] | 0.06 |  |
| CN-19 | Xem danh sách cư dân trong một căn hộ | Đạt | 200 cư dân của A0023: ['Nguyễn Thị C'] | 0.06 |  |
| CN-20 | Lưu bảng đơn giá, gồm phí gửi xe theo tháng và theo giờ | Đạt | 200; giá sau khi lưu (điện, nước, xe tháng, xe giờ) = (3800, 18000, 120000, 5000) | 0.06 |  |
| CN-21 | Đơn giá âm bị từ chối và không ghi đè giá cũ | Đạt | 400 {"message": "Giá trị phí không thể là số âm!"}; giá giữ nguyên: True | 0.04 |  |
| CN-22 | Tạo khoản thu hợp lệ, trạng thái mặc định chưa thanh toán, tìm được theo căn hộ | Đạt | 200 Bill added successfully; tìm theo căn hộ thấy 1 khoản, trạng thái UNPAID | 0.08 |  |
| CN-23 | Khoản thu sai dữ liệu báo lỗi theo từng trường | Đạt | căn hộ không tồn tại 400 ['apartmentNumber']; số tiền 0 + hạn hôm qua 400 ['amount', 'dueDate'] | 0.03 |  |
| CN-24 | Sửa rồi xóa một khoản thu | Đạt | sửa 200 (số tiền mới 65000.0), xóa 204, xem lại 404 | 0.16 |  |
| CN-25 | Tạo khoản thu điện, nước hàng loạt từ lượng tiêu thụ | Đạt | 200; tạo [('ELECTRICITY', 'A0012', 456000.0), ('ELECTRICITY', 'A0023', 285000.0), ('WATER', 'A0012', 144000.0)] | 0.05 |  |
| CN-26 | Cư dân chỉ thấy khoản thu của căn hộ mình | Đạt | 200 6 khoản, căn hộ ['A0012'] | 0.21 |  |
| CN-27 | Cư dân không xem được khoản thu của căn hộ khác | Đạt | mở khoản thu A0023: 403; xem chi tiết căn hộ A0023: 403 | 0.38 |  |
| CN-28 | Xác nhận thanh toán tiền mặt, cư dân không có quyền này | Đạt | cư dân 403; ban quản lý 200 -> PAID; xác nhận lần hai 400 | 0.22 |  |
| CN-29 | Tạo loại đóng góp và đợt đóng góp có mục tiêu, thời gian | Đạt | loại 200, đợt 200; đợt có trong danh sách: True, trạng thái ACTIVE | 0.17 |  |
| CN-30 | Đóng, mở lại và hủy đợt đóng góp | Đạt | đóng/mở lại/hủy/mở lại sau khi hủy = [200, 200, 200, 400] | 0.06 |  |

## Tích hợp (TH-01…TH-08)

| Mã | Tên | Kết quả | Thực tế ghi nhận | Thời gian (giây) | Lỗi |
|---|---|:---:|---|:---:|---|
| TH-01 | Cư dân tự đăng ký kèm căn hộ thì được gắn vào căn hộ đó | **Không đạt** | xác minh 200; A0035 có cư dân mới: False, trạng thái căn hộ VACANT, cư dân thấy 0 khoản thu | 2.23 | LOI-02 |
| TH-02 | Gắn cư dân đầu tiên vào căn hộ trống: căn hộ chuyển RENT và sinh 3 khoản phí | Đạt | A0031 trạng thái RENT, 3 khoản phí: ['phí thuê căn hộ A0031A', 'phí dịch vụ căn hộA003', 'phí quản lý căn hộA003'] | 0.04 |  |
| TH-03 | Đổi đơn giá rồi tạo khoản thu điện: số tiền dùng đơn giá mới | Đạt | 200; 10 kWh × 4200 = 42000.0 | 0.05 |  |
| TH-04 | Khoản thu mới của A0012 hiện cho cư dân A0012, không hiện cho cư dân khác | Đạt | cudan01 thấy: True; cudan02 thấy: False | 0.52 |  |
| TH-05 | Ban quản lý xác nhận thanh toán, cư dân thấy trạng thái đã thanh toán | Đạt | cư dân thấy khoản 13 trạng thái PAID | 0.15 |  |
| TH-06 | Vô hiệu hóa cư dân gỡ cư dân khỏi căn hộ, kích hoạt lại thì gắn lại | **Không đạt** | số cư dân A0031 sau khi khóa 1, sau khi mở lại 1 | 0.08 | LOI-03 |
| TH-07 | Tạo khoản đóng góp cho toàn bộ căn hộ: chỉ căn hộ có cư dân nhận khoản | **Không đạt** | 200; căn hộ nhận khoản ['A0012', 'A0023', 'A0024', 'A0035']; căn hộ đang có cư dân ['A0012', 'A0023', 'A0024', 'A0031'] | 0.25 | LOI-04 |
| TH-08 | Kế toán (ADMIN thường) không khóa được tài khoản super admin | **Không đạt** | khóa hàng loạt 200 {"deactivatedCount": 0, "success": false, "failedIds": [1]}; khóa đơn lẻ 200 success; admin còn đăng nhập được: False | 0.35 | LOI-01 |

## Giao diện (GD-01…GD-24)

Nguồn và giá trị quan sát chi tiết: [BC-02](bang-chung/BC-02-kiem-thu-giao-dien.md).

| Mã | Tên | Kết quả | Lỗi |
|---|---|:---:|---|
| GD-01 | Bố cục màn đăng nhập | **Không đạt** | LOI-09 |
| GD-02 | Báo lỗi khi đăng nhập sai | Đạt |  |
| GD-03 | Đăng nhập Ban quản lý | Đạt |  |
| GD-04 | Bố cục màn đăng ký | Đạt |  |
| GD-05 | Báo lỗi theo từng ô khi đăng ký sai | Đạt |  |
| GD-06 | Bố cục màn quên mật khẩu | Đạt |  |
| GD-07 | Sự kiện sắp tới theo ngày thực | Đạt |  |
| GD-08 | Xem thêm sự kiện | Đạt |  |
| GD-09 | Bảng căn hộ | Đạt |  |
| GD-10 | Thêm căn hộ từ giao diện | **Không đạt** | LOI-07 |
| GD-11 | Thanh công cụ quản lý tài khoản | Đạt |  |
| GD-12 | Hộp thoại xác nhận vô hiệu hóa | Đạt |  |
| GD-13 | Form tạo khoản thu | Đạt |  |
| GD-14 | Báo lỗi căn hộ không tồn tại | Đạt |  |
| GD-15 | Tạo khoản thu thành công | Đạt |  |
| GD-16 | Tìm kiếm khoản thu | Đạt |  |
| GD-17 | Bố cục bảng đơn giá | Đạt |  |
| GD-18 | Nhập đơn giá âm | **Không đạt** | LOI-08 |
| GD-19 | Màn nhập chỉ số điện nước | Đạt |  |
| GD-20 | Màn đóng góp | Đạt |  |
| GD-21 | Đăng nhập cư dân | Đạt |  |
| GD-22 | Cư dân xem khoản phải thu | Đạt |  |
| GD-23 | Cư dân không vào được trang quản trị | **Không đạt** | LOI-10 |
| GD-24 | Hộp thoại đổi mật khẩu | Đạt |  |
