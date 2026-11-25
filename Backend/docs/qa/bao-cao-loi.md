# Báo cáo lỗi – đợt kiểm thử 26/11/2026

Người ghi nhận: Nguyễn Hoàng Giang (kiểm thử). Người duyệt: Nguyễn Đình Nam Khánh.

LOI-01…LOI-13 được phát hiện ở lần 1 (commit `4ffb52e`). Sau bản sửa lỗi `c2dd81c`, mọi lỗi được kiểm tra lại ở lần 2 (commit `5ec2491`); LOI-14 được phát hiện trong lần kiểm tra lại này. Nguyên nhân trong code được chỉ ra để người sửa đỡ phải dò lại.

Trạng thái: **Đã sửa** (đã kiểm tra lại, case liên quan đạt), **Sửa một phần**, **Mở** (chưa sửa).

Mức độ: **Cao** (sai quyền hoặc mất tính đúng của dữ liệu nghiệp vụ chính), **Trung bình** (sai chức năng, có cách làm khác tạm thời), **Thấp** (hiển thị, thông báo, trải nghiệm).

## Tổng hợp

| Mã | Mức độ | Tóm tắt | Case phát hiện | US | Giao cho | Trạng thái sau lần 2 |
|---|---|---|---|---|---|---|
| LOI-01 | Cao | ADMIN thường khóa được tài khoản super admin bằng API khóa đơn lẻ | TH-08 | US23 | Đặng Thiệu Minh | Đã sửa |
| LOI-02 | Cao | Cư dân tự đăng ký kèm căn hộ không được gắn vào căn hộ | TH-01 | US21 | Đặng Thiệu Minh | Đã sửa |
| LOI-03 | Trung bình | Khóa tài khoản không gỡ cư dân khỏi căn hộ mà lại xóa căn hộ khỏi hồ sơ cư dân | TH-06 | US23, US01 | Đặng Thiệu Minh | Đã sửa |
| LOI-04 | Trung bình | Tạo khoản đóng góp cho toàn bộ căn hộ lệch với danh sách cư dân của căn hộ | TH-07 | US15 | Nguyễn Đình Nam Khánh | Đã sửa |
| LOI-05 | Trung bình | Thêm căn hộ bỏ qua trạng thái được nhập, luôn lưu `VACANT` | CN-16 | US02 | Đặng Thiệu Minh | Đã sửa |
| LOI-06 | Thấp | Thêm căn hộ trùng số trả lỗi 500 "Runtime Exception occurred" | CN-16 | US02 | Đặng Thiệu Minh | Đã sửa |
| LOI-07 | Trung bình | Màn Apartment Management không có nút thêm căn hộ | GD-10 | US02 | Đặng Thiệu Minh | Đã sửa |
| LOI-08 | Trung bình | Nhập đơn giá âm, giao diện tự đổi thành 0 rồi lưu thành công | GD-18 | US05 | Nguyễn Đình Nam Khánh | Mở |
| LOI-09 | Thấp | Ô Username ở Sign In/Sign Up có kiểu email và gợi ý địa chỉ email | GD-01 | US22, US21 | Nguyễn Đình Nam Khánh | Sửa một phần |
| LOI-10 | Thấp | Cư dân mở được trang quản trị bằng cách gõ URL | GD-23 | US23 | Đặng Thiệu Minh | Mở |
| LOI-11 | Thấp | Mô tả khoản phí tự sinh bị lặp số căn hộ và thiếu dấu cách | TH-02, GD-22 | US06 | Đặng Thiệu Minh | Mở |
| LOI-12 | Thấp | Log khởi động báo tạo 150 căn hộ, thực tế tạo 50 | Bằng chứng BC-03 | US02 | Đặng Thiệu Minh | Đã sửa |
| LOI-13 | Thấp | Nút "Sign in with Google" không làm gì khi bấm | GD-06 (quan sát thêm) | US22 | Nguyễn Đình Nam Khánh | Mở |
| LOI-14 | Cao | ADMIN thường sửa được tài khoản super admin, hạ `admin` xuống `USER` | Checklist B1 (lần 2) | US23 | Đặng Thiệu Minh | Mở |

Thống kê: 14 lỗi (3 Cao, 5 Trung bình, 6 Thấp). Sau lần 2: 8 đã sửa, 1 sửa một phần, 5 còn mở (trong đó 1 lỗi Cao: LOI-14).

## Chi tiết

### LOI-01 – ADMIN thường khóa được tài khoản super admin

- **Bước tái hiện:** đăng nhập `ketoan` (ADMIN thường); gọi `POST /api/admin/users/deactivate/1` (id của `admin`); đăng nhập `admin`.
- **Mong đợi:** bị từ chối như khi khóa hàng loạt (`batch/deactivate` trả `failedIds: [1]`).
- **Thực tế:** khóa hàng loạt bị chặn đúng, nhưng khóa đơn lẻ trả `200 success`; sau đó `admin` không đăng nhập được nữa.
- **Nguyên nhân:** `AdminListUserController.deactivateUser` không kiểm tra người gọi; chỉ giao diện ẩn nút nhờ cờ `canEdit`. Các API đơn lẻ `activate`, `delete`, `edit` cũng không kiểm tra, cần rà cùng lúc (chưa kiểm thử riêng).
- **Bằng chứng:** BC-01, dòng TH-08.

- **Kiểm tra lại (lần 2):** Đã sửa. Kế toán khóa đơn lẻ `admin` nhận 403; kích hoạt, xóa `admin` và tự khóa chính mình cũng nhận 403. Riêng API sửa tài khoản vẫn chưa chặn, ghi thành LOI-14.

### LOI-02 – Đăng ký kèm căn hộ không gắn cư dân vào căn hộ

- **Bước:** đăng ký `qa_th01` với `apartmentNumbers: ["A0035"]`, xác minh OTP; admin xem cư dân của `A0035`.
- **Mong đợi:** giống khi admin thêm cư dân (TH-02): căn hộ có cư dân, chuyển `RENT`, sinh 3 khoản phí.
- **Thực tế:** hồ sơ cư dân ghi `A0035`, nhưng căn hộ vẫn `VACANT`, không có cư dân, không có khoản phí; cư dân thấy 0 khoản thu; căn hộ không xuất hiện ở màn Utility Bills Creation.
- **Nguyên nhân:** `UserService.addUser(UserDTO)` (luồng đăng ký) không gọi `apartmentService.updateResident(...)` như `addUser(ManualUserDTO)`.
- **Bằng chứng:** BC-01, dòng TH-01; BC-02, GD-19.

- **Kiểm tra lại (lần 2):** Đã sửa. TH-01 đạt: `A0035` có cư dân mới, chuyển `RENT`, cư dân thấy 3 khoản thu; GD-19 hiện `A0035`.

### LOI-03 – Khóa tài khoản làm lệch dữ liệu cư dân và căn hộ

- **Bước:** `qa_cn14` đang ở `A0031`; admin vô hiệu hóa rồi kích hoạt lại `qa_cn14`; xem cư dân của `A0031` và hồ sơ `qa_cn14`.
- **Mong đợi:** khi khóa, cư dân bị gỡ khỏi `A0031` (hộp thoại khóa hàng loạt cũng ghi "removed from their apartments"); khi mở lại thì gắn lại.
- **Thực tế:** `A0031` vẫn ghi 1 cư dân trong suốt quá trình; còn hồ sơ `qa_cn14` thì mất căn hộ (danh sách căn hộ thành rỗng) và không được khôi phục khi kích hoạt lại.
- **Nguyên nhân:** `ApartmentService.deleteResident(Resident)` truyền chính tập `resident.getApartmentNumbers()` vào `deleteResident(Set, Resident)`; dòng `removeAll` đầu tiên làm rỗng tập này trước vòng lặp, nên vòng lặp không gỡ căn hộ nào.
- **Bằng chứng:** BC-01, dòng TH-06.

- **Kiểm tra lại (lần 2):** Đã sửa. TH-06 đạt: sau khi khóa `A0031` còn 0 cư dân, mở lại còn 1.

### LOI-04 – Khoản đóng góp tạo theo hồ sơ cư dân, lệch với căn hộ

- **Bước:** sau TH-01 và TH-06, tạo đợt đóng góp và gọi `create-for-all` với 100.000 đ.
- **Mong đợi:** mọi căn hộ đang có cư dân (`A0012`, `A0023`, `A0024`, `A0031`) nhận khoản đóng góp.
- **Thực tế:** nhận khoản là `A0012`, `A0023`, `A0024`, `A0035`; `A0031` (đang có cư dân) không nhận, `A0035` (căn hộ trống) lại nhận.
- **Nguyên nhân:** `ContributionService.createContributionForApartment` tìm cư dân theo hồ sơ (`residentRepository.findByApartmentNumber`), trong khi màn căn hộ dùng `apartment.residentIds`. Hai nguồn này lệch nhau do LOI-02 và LOI-03. Sửa hai lỗi đó sẽ hết lệch; nên dùng chung một nguồn dữ liệu.
- **Bằng chứng:** BC-01, dòng TH-07.

- **Kiểm tra lại (lần 2):** Đã sửa (nhờ sửa LOI-02 và LOI-03). TH-07 đạt: căn hộ nhận khoản trùng khớp với căn hộ có cư dân.

### LOI-05 – Thêm căn hộ bỏ qua trạng thái

- **Bước:** `POST /api/admin/apartment-list/add-apartment` với `status: "OCCUPIED"`.
- **Mong đợi:** căn hộ lưu trạng thái `OCCUPIED` (US02: thêm căn hộ gồm trạng thái).
- **Thực tế:** lưu `VACANT`; các thuộc tính khác đúng.
- **Nguyên nhân:** `ApartmentService.saveApartment` không gọi `setStatus`.
- **Bằng chứng:** BC-01, dòng CN-16.

- **Kiểm tra lại (lần 2):** Đã sửa. CN-16 lưu đúng trạng thái `OCCUPIED`.

### LOI-06 – Thêm căn hộ trùng số trả lỗi 500

- **Bước:** thêm lại căn hộ `B0101` đã tồn tại.
- **Mong đợi:** 400 kèm thông báo "Số căn hộ đã tồn tại".
- **Thực tế:** 500 "Runtime Exception occurred: could not execute statement…" (vi phạm ràng buộc `unique` của database).
- **Bằng chứng:** BC-01, dòng CN-16.

- **Kiểm tra lại (lần 2):** Đã sửa. Thêm trùng số căn hộ trả 400 `{"apartmentNumber": "Số căn hộ đã tồn tại"}`.

### LOI-07 – Không có nút thêm căn hộ trên giao diện

- **Bước:** đăng nhập `admin`, mở Apartment Management.
- **Mong đợi:** có nút mở form tạo căn hộ.
- **Thực tế:** chỉ có **Filter**, **Select All**, **Set Status**. `ApartmentTable.js` có sẵn chế độ `create` gọi `add-apartment` nhưng không nút nào chuyển sang chế độ này, nên chỉ thêm căn hộ được qua API.
- **Bằng chứng:** BC-02, GD-10.

- **Kiểm tra lại (lần 2):** Đã sửa. GD-10 đạt: có nút **New Apartment**, tạo `C0101` từ giao diện lưu đúng cả trạng thái `RENT`.

### LOI-08 – Đơn giá âm bị đổi thành 0 và lưu

- **Bước:** Fee Unit Management, nhập -1000 vào Hourly Parking, bấm **Save Changes**.
- **Mong đợi:** báo lỗi, giữ giá cũ 5.000 đ/giờ.
- **Thực tế:** ô tự đổi thành 0 (do `NumberInput min={0}`), hiện "Fee unit settings saved successfully", giá gửi xe theo giờ trong database thành 0. Backend vẫn chặn giá âm đúng (CN-21), lỗi nằm ở giao diện.
- **Bằng chứng:** BC-02, GD-18.

- **Kiểm tra lại (lần 2):** Chưa sửa. GD-18 vẫn đổi -1000 thành 0 và lưu.

### LOI-09 – Ô Username gợi ý nhập email

- **Bước:** mở Sign In và Sign Up.
- **Mong đợi:** ô Username là ô chữ thường, gợi ý tên đăng nhập.
- **Thực tế:** ô có `type="email"` và gợi ý `mail@simmmple.com` (Sign In), `username` (Sign Up). Người dùng dễ nhập email (ví dụ `admin@gmail.com`) và đăng nhập thất bại vì hệ thống chỉ nhận tên đăng nhập. Ở Sign Up, nhãn của ô Phone và Age bị gắn nhầm vào ô khác (trình đọc màn hình đọc là "Username", "Full name").
- **Bằng chứng:** BC-02, GD-01, GD-04.

- **Kiểm tra lại (lần 2):** Sửa một phần. Ô Username ở Sign In đã là ô chữ, gợi ý "Tên đăng nhập, VD: admin". Ở Sign Up ô Username vẫn `type="email"` và nhãn trợ năng của ô Phone/Age vẫn gắn nhầm.

### LOI-10 – Cư dân mở được trang quản trị bằng URL

- **Bước:** đăng nhập `cudan01`, gõ `/admin/bill`.
- **Mong đợi:** bị chặn hoặc chuyển về trang cư dân.
- **Thực tế:** trang mở được, hiện menu quản trị và nút **New Bill**; bảng trống vì API trả 403. Dữ liệu vẫn được bảo vệ, nhưng giao diện gây hiểu nhầm. `AuthGuard` chỉ kiểm tra có token, không kiểm tra vai trò.
- **Bằng chứng:** BC-02, GD-23.

- **Kiểm tra lại (lần 2):** Chưa sửa. GD-23 vẫn mở được `/admin/bill` bằng tài khoản cư dân.

### LOI-11 – Mô tả khoản phí tự sinh bị lặp số căn hộ

- **Thực tế:** "phí thuê căn hộ A0012A0012", "phí dịch vụ căn hộA0012A0012", "phí quản lý căn hộA0012A0012".
- **Nguyên nhân:** `ApartmentService.updateResident` đã nối số căn hộ vào mô tả, `BillService.saveApartmentBill` lại nối thêm lần nữa; hai mô tả sau thiếu dấu cách.
- **Bằng chứng:** BC-01, dòng TH-02; BC-02, GD-22.

- **Kiểm tra lại (lần 2):** Chưa sửa. Vẫn thấy "phí thuê căn hộ A0031A0031", "phí dịch vụ căn hộA0031A0031".

### LOI-12 – Log khởi động sai số căn hộ

- **Thực tế:** log in "Đã khởi tạo 150 căn hộ!" nhưng vòng lặp chỉ tạo 10 tầng × 5 căn = 50 căn hộ (`A0001`–`A0050`). Nhánh tạo `PENHOUSE` cho tầng 15 không bao giờ chạy.
- **Bằng chứng:** BC-03.

- **Kiểm tra lại (lần 2):** Đã sửa. Log khởi động in "Đã khởi tạo 50 căn hộ!" (BC-03, mục 4.2).

### LOI-13 – Nút "Sign in with Google" không có chức năng

- **Thực tế:** bấm nút trên Sign In/Forgot password không chuyển trang, không gửi request, không có thông báo. Đăng nhập Google không nằm trong User Story nào; nên ẩn nút.
- **Bằng chứng:** BC-02, ghi chú ở GD-06.
- **Kiểm tra lại (lần 2):** Chưa sửa. Nút vẫn hiện và vẫn không làm gì khi bấm.

### LOI-14 – ADMIN thường sửa được tài khoản super admin

- **Phát hiện:** lần 2, khi làm mục B1 của checklist hồi quy (thử mọi API đơn lẻ của kế toán lên tài khoản `admin`).
- **Bước tái hiện:** đăng nhập `ketoan`; gọi `POST /api/admin/users/edit/1` với `role: "USER"`; xem danh sách tài khoản; đăng nhập `admin`.
- **Mong đợi:** bị từ chối (403) như các API khóa, mở khóa, xóa đã được sửa ở LOI-01.
- **Thực tế:** 200 `updated`; `admin` bị hạ xuống `USER`, đăng nhập lại chỉ nhận `ROLE_USER` nên mất toàn bộ quyền quản trị. Đã khôi phục bằng cách cho `ketoan` sửa lại `role: "ADMIN"`.
- **Nguyên nhân:** `AdminListUserController.editUser` chưa có kiểm tra người gọi như `deactivateUser`, `activateUser`, `deleteUser` sau bản sửa `c2dd81c`.
- **Bằng chứng:** BC-03, mục 4.3.
