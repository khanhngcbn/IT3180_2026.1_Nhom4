# Báo cáo thực thi kiểm thử – 26/11/2026

| Mục | Lần 1 | Lần 2 (hồi quy) |
|---|---|---|
| Mã nguồn | `main` tại commit `4ffb52e` | `main` tại commit `5ec2491` (gồm bản sửa lỗi `c2dd81c`) |
| Chạy API | 2026-11-26 05:20:44 → 05:21:06 | 2026-11-26 05:37:31 → 05:37:53 |
| Chạy giao diện | Ngay sau lần 1 của API, cùng backend | Ngay sau lần 2 của API, cùng backend |
| Người thực hiện | Nguyễn Hoàng Giang (kiểm thử) | Nguyễn Hoàng Giang (kiểm thử) |
| Người duyệt | Nguyễn Đình Nam Khánh | Nguyễn Đình Nam Khánh |

Môi trường như [kế hoạch kiểm thử, mục 5](ke-hoach-kiem-thu.md#5-môi-trường). Mỗi lần chạy đều khởi động lại backend với database trống.

## Tổng hợp

| Nhóm | Số case | Đạt lần 1 | Đạt lần 2 | Tỉ lệ lần 1 | Tỉ lệ lần 2 |
|---|:---:|:---:|:---:|:---:|:---:|
| Chức năng (CN) | 30 | 29 | 30 | 96.7% | 100.0% |
| Tích hợp (TH) | 8 | 4 | 8 | 50.0% | 100.0% |
| Giao diện (GD) | 24 | 20 | 22 | 83.3% | 91.7% |
| **Tổng** | **62** | **53** | **60** | **85.5%** | **96.8%** |

Test đơn vị backend (`./mvnw test`): 9/9 đạt ở cả hai lần (BC-03).

## Ghi chú

- Trước lần 1 có một lần chạy thử. Ở lần đó, ngoài 5 lỗi thật, còn 2 case báo không đạt vì lỗi của chính script: CN-12 dùng một tài khoản chưa được tạo, TH-03 thiếu ô nước mà giao diện luôn gửi. Hai chỗ này đã sửa trong script, sau đó khởi động lại backend với database mới rồi mới chạy lần 1.
- Lần 1, TH-08 đã khóa được `admin` (lỗi LOI-01); script tự kích hoạt lại `admin` bằng tài khoản `ketoan`. Lần 2 thao tác này bị chặn (403).
- Ở lần 2, ngoài 62 case, đã thử thêm theo mục B1 của [checklist hồi quy](checklist-hoi-quy.md): tài khoản `ketoan` vẫn **sửa** được tài khoản `admin` và hạ xuống `USER`. Đây là lỗi mới LOI-14 (BC-03, mục 4.3).
- GD-18 ở cả hai lần đều làm giá gửi xe theo giờ trong database thành 0 (lỗi LOI-08).

## Lần 3 – sau khi sửa LOI-14

| Mục | Nội dung |
|---|---|
| Mã nguồn | commit `1150a10` cộng bản sửa LOI-14 (`AdminListUserController.editUser`) và TH-08 mở rộng |
| Chạy API | 2026-11-26 05:47:42 → 05:48:01, backend khởi động mới |
| Kết quả API | 38/38 đạt (CN 30/30, TH 8/8); TH-08: khóa/mở/sửa/xóa đơn lẻ `admin` bằng `ketoan` = 403, 403, 403, 403; `admin` vẫn `ROLE_ADMIN` |
| Test đơn vị | 9/9 đạt |
| Giao diện | Không chạy lại vì bản sửa chỉ thay đổi backend; giữ kết quả lần 2: 22/24 (GD-18, GD-23 không đạt) |
| Tổng sau lần 3 | 60/62 đạt (96,8%) |

## Chức năng (CN-01…CN-30)

Nguồn: [BC-01](bang-chung/BC-01-kiem-thu-api.txt). Cột "Thực tế ghi nhận" chép nguyên từ đầu ra của script.

| Mã | Tên | Lần 1 | Lần 2 | Thực tế ghi nhận (lần 1) | Thực tế ghi nhận (lần 2, chỉ ghi khi khác lần 1) | Lỗi |
|---|---|:---:|:---:|---|---|---|
| CN-01 | Đăng ký tài khoản hợp lệ và xác minh bằng OTP | Đạt | Đạt | verify 200 {"message": "Xác thực thành công!"}; đăng nhập được |  |  |
| CN-02 | Đăng ký với dữ liệu sai định dạng bị từ chối | Đạt | Đạt | 400 lỗi ở các trường ['password', 'phone'] |  |  |
| CN-03 | OTP sai bị từ chối, gửi lại OTP rồi nhập mã mới thì thành công | Đạt | Đạt | OTP sai 400 ({"message": "OTP không đúng. Vui lòng thử lại!"}), gửi lại 200, OTP mới 200 |  |  |
| CN-04 | Đăng nhập đúng nhận JWT có vai trò tương ứng | Đạt | Đạt | vai trò trong JWT: admin=ROLE_ADMIN, cudan01=ROLE_USER |  |  |
| CN-05 | Sai mật khẩu hoặc tài khoản bị khóa thì không đăng nhập được | Đạt | Đạt | sai mật khẩu 401, tài khoản bị khóa 401 |  |  |
| CN-06 | Đổi mật khẩu phải nhập đúng mật khẩu cũ | Đạt | Đạt | mật khẩu cũ sai 400 ({"error": "error_wrong_old_password"}), đúng 200; mật khẩu mới đăng nhập được |  |  |
| CN-07 | Quên mật khẩu: đặt lại bằng OTP gửi tới email đã đăng ký | Đạt | Đạt | gửi OTP 200, đặt lại 200 {"message": "Password changed successfully", "success": true... |  |  |
| CN-08 | Không dùng được OTP của email khác để đặt lại mật khẩu | Đạt | Đạt | 400 {"message": "Invalid OTP!", "success": false}; cudan02 vẫn dùng mật khẩu cũ: True |  |  |
| CN-09 | Nhập sai OTP 3 lần thì OTP bị hủy | Đạt | Đạt | 3 lần sai [400, 400, 400], OTP đúng sau đó 400 |  |  |
| CN-10 | Ban quản lý đổi vai trò tài khoản | Đạt | Đạt | 200 updated; vai trò sau khi đổi: ROLE_ADMIN |  |  |
| CN-11 | Vô hiệu hóa và kích hoạt lại một tài khoản | Đạt | Đạt | khóa 200 (đăng nhập bị chặn: True), mở 200 (đăng nhập lại: True) |  |  |
| CN-12 | Vô hiệu hóa hàng loạt, bỏ qua tài khoản admin | Đạt | Đạt | 200 {"deactivatedCount": 2, "success": true, "failedIds": [1]}; 2 tài khoản bị khóa: True; admin vẫn đăng nhập: True |  |  |
| CN-13 | Cư dân và người chưa đăng nhập không vào được API quản trị | Đạt | Đạt | cư dân 403, không token 403, cư dân xem đơn giá 403 |  |  |
| CN-14 | Thêm hồ sơ cư dân và gắn với căn hộ | Đạt | Đạt | 200 User added successfully; hồ sơ có căn hộ ['A0031']; căn hộ A0031 có 1 cư dân |  |  |
| CN-15 | Thêm cư dân với dữ liệu sai bị từ chối | Đạt | Đạt | căn hộ sai 400 {"apartmentNumbers": "Apartment không tồn tại trong hệ thống...; mật khẩu yếu 400 |  |  |
| CN-16 | Thêm căn hộ mới với đủ thuộc tính | **Không đạt** | Đạt | tạo 201; lưu được (tầng, diện tích, loại, trạng thái) = (11, 68.5, 'STANDARD', 'VACANT'); thêm trùng số căn hộ 500 Runtime Exception occurred: could not execute stat... | tạo 201; lưu được (tầng, diện tích, loại, trạng thái) = (11, 68.5, 'STANDARD', 'OCCUPIED'); thêm trùng số căn hộ 400 {"apartmentNumber": "Số căn hộ đã tồn tại"} | LOI-05, LOI-06 |
| CN-17 | Cập nhật trạng thái nhiều căn hộ cùng lúc | Đạt | Đạt | cập nhật 200 -> OCCUPIED/OCCUPIED; trạng thái không hợp lệ 400 |  |  |
| CN-18 | Lọc căn hộ theo tầng, trạng thái và loại | Đạt | Đạt | 200 kết quả ['A0001', 'A0002', 'A0003', 'A0004', 'A0005'] |  |  |
| CN-19 | Xem danh sách cư dân trong một căn hộ | Đạt | Đạt | 200 cư dân của A0023: ['Nguyễn Thị C'] |  |  |
| CN-20 | Lưu bảng đơn giá, gồm phí gửi xe theo tháng và theo giờ | Đạt | Đạt | 200; giá sau khi lưu (điện, nước, xe tháng, xe giờ) = (3800, 18000, 120000, 5000) |  |  |
| CN-21 | Đơn giá âm bị từ chối và không ghi đè giá cũ | Đạt | Đạt | 400 {"message": "Giá trị phí không thể là số âm!"}; giá giữ nguyên: True |  |  |
| CN-22 | Tạo khoản thu hợp lệ, trạng thái mặc định chưa thanh toán, tìm được theo căn hộ | Đạt | Đạt | 200 Bill added successfully; tìm theo căn hộ thấy 1 khoản, trạng thái UNPAID |  |  |
| CN-23 | Khoản thu sai dữ liệu báo lỗi theo từng trường | Đạt | Đạt | căn hộ không tồn tại 400 ['apartmentNumber']; số tiền 0 + hạn hôm qua 400 ['amount', 'dueDate'] |  |  |
| CN-24 | Sửa rồi xóa một khoản thu | Đạt | Đạt | sửa 200 (số tiền mới 65000.0), xóa 204, xem lại 404 |  |  |
| CN-25 | Tạo khoản thu điện, nước hàng loạt từ lượng tiêu thụ | Đạt | Đạt | 200; tạo [('ELECTRICITY', 'A0012', 456000.0), ('ELECTRICITY', 'A0023', 285000.0), ('WATER', 'A0012', 144000.0)] |  |  |
| CN-26 | Cư dân chỉ thấy khoản thu của căn hộ mình | Đạt | Đạt | 200 6 khoản, căn hộ ['A0012'] |  |  |
| CN-27 | Cư dân không xem được khoản thu của căn hộ khác | Đạt | Đạt | mở khoản thu A0023: 403; xem chi tiết căn hộ A0023: 403 |  |  |
| CN-28 | Xác nhận thanh toán tiền mặt, cư dân không có quyền này | Đạt | Đạt | cư dân 403; ban quản lý 200 -> PAID; xác nhận lần hai 400 |  |  |
| CN-29 | Tạo loại đóng góp và đợt đóng góp có mục tiêu, thời gian | Đạt | Đạt | loại 200, đợt 200; đợt có trong danh sách: True, trạng thái ACTIVE |  |  |
| CN-30 | Đóng, mở lại và hủy đợt đóng góp | Đạt | Đạt | đóng/mở lại/hủy/mở lại sau khi hủy = [200, 200, 200, 400] |  |  |

## Tích hợp (TH-01…TH-08)

| Mã | Tên | Lần 1 | Lần 2 | Thực tế ghi nhận (lần 1) | Thực tế ghi nhận (lần 2, chỉ ghi khi khác lần 1) | Lỗi |
|---|---|:---:|:---:|---|---|---|
| TH-01 | Cư dân tự đăng ký kèm căn hộ thì được gắn vào căn hộ đó | **Không đạt** | Đạt | xác minh 200; A0035 có cư dân mới: False, trạng thái căn hộ VACANT, cư dân thấy 0 khoản thu | xác minh 200; A0035 có cư dân mới: True, trạng thái căn hộ RENT, cư dân thấy 3 khoản thu | LOI-02 |
| TH-02 | Gắn cư dân đầu tiên vào căn hộ trống: căn hộ chuyển RENT và sinh 3 khoản phí | Đạt | Đạt | A0031 trạng thái RENT, 3 khoản phí: ['phí thuê căn hộ A0031A', 'phí dịch vụ căn hộA003', 'phí quản lý căn hộA003'] |  |  |
| TH-03 | Đổi đơn giá rồi tạo khoản thu điện: số tiền dùng đơn giá mới | Đạt | Đạt | 200; 10 kWh × 4200 = 42000.0 |  |  |
| TH-04 | Khoản thu mới của A0012 hiện cho cư dân A0012, không hiện cho cư dân khác | Đạt | Đạt | cudan01 thấy: True; cudan02 thấy: False |  |  |
| TH-05 | Ban quản lý xác nhận thanh toán, cư dân thấy trạng thái đã thanh toán | Đạt | Đạt | cư dân thấy khoản 13 trạng thái PAID |  |  |
| TH-06 | Vô hiệu hóa cư dân gỡ cư dân khỏi căn hộ, kích hoạt lại thì gắn lại | **Không đạt** | Đạt | số cư dân A0031 sau khi khóa 1, sau khi mở lại 1 | số cư dân A0031 sau khi khóa 0, sau khi mở lại 1 | LOI-03 |
| TH-07 | Tạo khoản đóng góp cho toàn bộ căn hộ: chỉ căn hộ có cư dân nhận khoản | **Không đạt** | Đạt | 200; căn hộ nhận khoản ['A0012', 'A0023', 'A0024', 'A0035']; căn hộ đang có cư dân ['A0012', 'A0023', 'A0024', 'A0031'] | 200; căn hộ nhận khoản ['A0012', 'A0023', 'A0024', 'A0031', 'A0035']; căn hộ đang có cư dân ['A0012', 'A0023', 'A0024', 'A0031', 'A0035'] | LOI-04 |
| TH-08 | Kế toán (ADMIN thường) không khóa được tài khoản super admin | **Không đạt** | Đạt | khóa hàng loạt 200 {"deactivatedCount": 0, "success": false, "failedIds": [1]}; khóa đơn lẻ 200 success; admin còn đăng nhập được: False | khóa hàng loạt 200 {"deactivatedCount": 0, "success": false, "failedIds": [1]}; khóa đơn lẻ 403 Bạn không có quyền k...; admin còn đăng nhập được: True | LOI-01 |

## Giao diện (GD-01…GD-24)

Giá trị quan sát chi tiết: [BC-02](bang-chung/BC-02-kiem-thu-giao-dien.md).

| Mã | Tên | Lần 1 | Lần 2 | Lỗi |
|---|---|:---:|:---:|---|
| GD-01 | Bố cục màn đăng nhập | **Không đạt** | Đạt | LOI-09 |
| GD-02 | Báo lỗi khi đăng nhập sai | Đạt | Đạt |  |
| GD-03 | Đăng nhập Ban quản lý | Đạt | Đạt |  |
| GD-04 | Bố cục màn đăng ký | Đạt | Đạt |  |
| GD-05 | Báo lỗi theo từng ô khi đăng ký sai | Đạt | Đạt |  |
| GD-06 | Bố cục màn quên mật khẩu | Đạt | Đạt |  |
| GD-07 | Sự kiện sắp tới theo ngày thực | Đạt | Đạt |  |
| GD-08 | Xem thêm sự kiện | Đạt | Đạt |  |
| GD-09 | Bảng căn hộ | Đạt | Đạt |  |
| GD-10 | Thêm căn hộ từ giao diện | **Không đạt** | Đạt | LOI-07 |
| GD-11 | Thanh công cụ quản lý tài khoản | Đạt | Đạt |  |
| GD-12 | Hộp thoại xác nhận vô hiệu hóa | Đạt | Đạt |  |
| GD-13 | Form tạo khoản thu | Đạt | Đạt |  |
| GD-14 | Báo lỗi căn hộ không tồn tại | Đạt | Đạt |  |
| GD-15 | Tạo khoản thu thành công | Đạt | Đạt |  |
| GD-16 | Tìm kiếm khoản thu | Đạt | Đạt |  |
| GD-17 | Bố cục bảng đơn giá | Đạt | Đạt |  |
| GD-18 | Nhập đơn giá âm | **Không đạt** | **Không đạt** | LOI-08 |
| GD-19 | Màn nhập chỉ số điện nước | Đạt | Đạt |  |
| GD-20 | Màn đóng góp | Đạt | Đạt |  |
| GD-21 | Đăng nhập cư dân | Đạt | Đạt |  |
| GD-22 | Cư dân xem khoản phải thu | Đạt | Đạt |  |
| GD-23 | Cư dân không vào được trang quản trị | **Không đạt** | **Không đạt** | LOI-10 |
| GD-24 | Hộp thoại đổi mật khẩu | Đạt | Đạt |  |
