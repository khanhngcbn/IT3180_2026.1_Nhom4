# Báo cáo lỗi – đợt kiểm thử 26/11/2026

Người ghi nhận: Nguyễn Hoàng Giang (kiểm thử). Người duyệt: Nguyễn Đình Nam Khánh. Mọi lỗi dưới đây đều tái hiện được trên mã nguồn nhánh `main` sau commit `4ffb52e`; nguyên nhân trong code được chỉ ra để người sửa đỡ phải dò lại.

Mức độ: **Cao** (sai quyền hoặc mất tính đúng của dữ liệu nghiệp vụ chính), **Trung bình** (sai chức năng, có cách làm khác tạm thời), **Thấp** (hiển thị, thông báo, trải nghiệm).

## Tổng hợp

| Mã | Mức độ | Tóm tắt | Case phát hiện | US | Giao cho | Trạng thái |
|---|---|---|---|---|---|---|
| LOI-01 | Cao | ADMIN thường khóa được tài khoản super admin bằng API khóa đơn lẻ | TH-08 | US23 | Đặng Thiệu Minh | Mở |
| LOI-02 | Cao | Cư dân tự đăng ký kèm căn hộ không được gắn vào căn hộ | TH-01 | US21 | Đặng Thiệu Minh | Mở |
| LOI-03 | Trung bình | Khóa tài khoản không gỡ cư dân khỏi căn hộ mà lại xóa căn hộ khỏi hồ sơ cư dân | TH-06 | US23, US01 | Đặng Thiệu Minh | Mở |
| LOI-04 | Trung bình | Tạo khoản đóng góp cho toàn bộ căn hộ lệch với danh sách cư dân của căn hộ | TH-07 | US15 | Nguyễn Đình Nam Khánh | Mở |
| LOI-05 | Trung bình | Thêm căn hộ bỏ qua trạng thái được nhập, luôn lưu `VACANT` | CN-16 | US02 | Đặng Thiệu Minh | Mở |
| LOI-06 | Thấp | Thêm căn hộ trùng số trả lỗi 500 "Runtime Exception occurred" | CN-16 | US02 | Đặng Thiệu Minh | Mở |
| LOI-07 | Trung bình | Màn Apartment Management không có nút thêm căn hộ | GD-10 | US02 | Đặng Thiệu Minh | Mở |
| LOI-08 | Trung bình | Nhập đơn giá âm, giao diện tự đổi thành 0 rồi lưu thành công | GD-18 | US05 | Nguyễn Đình Nam Khánh | Mở |
| LOI-09 | Thấp | Ô Username ở Sign In/Sign Up có kiểu email và gợi ý địa chỉ email | GD-01 | US22, US21 | Nguyễn Đình Nam Khánh | Mở |
| LOI-10 | Thấp | Cư dân mở được trang quản trị bằng cách gõ URL | GD-23 | US23 | Đặng Thiệu Minh | Mở |
| LOI-11 | Thấp | Mô tả khoản phí tự sinh bị lặp số căn hộ và thiếu dấu cách | TH-02, GD-22 | US06 | Đặng Thiệu Minh | Mở |
| LOI-12 | Thấp | Log khởi động báo tạo 150 căn hộ, thực tế tạo 50 | Bằng chứng BC-03 | US02 | Đặng Thiệu Minh | Mở |
| LOI-13 | Thấp | Nút "Sign in with Google" không làm gì khi bấm | GD-06 (quan sát thêm) | US22 | Nguyễn Đình Nam Khánh | Mở |

Thống kê: 2 Cao, 5 Trung bình, 6 Thấp.

## Chi tiết

### LOI-01 – ADMIN thường khóa được tài khoản super admin

- **Bước tái hiện:** đăng nhập `ketoan` (ADMIN thường); gọi `POST /api/admin/users/deactivate/1` (id của `admin`); đăng nhập `admin`.
- **Mong đợi:** bị từ chối như khi khóa hàng loạt (`batch/deactivate` trả `failedIds: [1]`).
- **Thực tế:** khóa hàng loạt bị chặn đúng, nhưng khóa đơn lẻ trả `200 success`; sau đó `admin` không đăng nhập được nữa.
- **Nguyên nhân:** `AdminListUserController.deactivateUser` không kiểm tra người gọi; chỉ giao diện ẩn nút nhờ cờ `canEdit`. Các API đơn lẻ `activate`, `delete`, `edit` cũng không kiểm tra, cần rà cùng lúc (chưa kiểm thử riêng).
- **Bằng chứng:** BC-01, dòng TH-08.

### LOI-02 – Đăng ký kèm căn hộ không gắn cư dân vào căn hộ

- **Bước:** đăng ký `qa_th01` với `apartmentNumbers: ["A0035"]`, xác minh OTP; admin xem cư dân của `A0035`.
- **Mong đợi:** giống khi admin thêm cư dân (TH-02): căn hộ có cư dân, chuyển `RENT`, sinh 3 khoản phí.
- **Thực tế:** hồ sơ cư dân ghi `A0035`, nhưng căn hộ vẫn `VACANT`, không có cư dân, không có khoản phí; cư dân thấy 0 khoản thu; căn hộ không xuất hiện ở màn Utility Bills Creation.
- **Nguyên nhân:** `UserService.addUser(UserDTO)` (luồng đăng ký) không gọi `apartmentService.updateResident(...)` như `addUser(ManualUserDTO)`.
- **Bằng chứng:** BC-01, dòng TH-01; BC-02, GD-19.

### LOI-03 – Khóa tài khoản làm lệch dữ liệu cư dân và căn hộ

- **Bước:** `qa_cn14` đang ở `A0031`; admin vô hiệu hóa rồi kích hoạt lại `qa_cn14`; xem cư dân của `A0031` và hồ sơ `qa_cn14`.
- **Mong đợi:** khi khóa, cư dân bị gỡ khỏi `A0031` (hộp thoại khóa hàng loạt cũng ghi "removed from their apartments"); khi mở lại thì gắn lại.
- **Thực tế:** `A0031` vẫn ghi 1 cư dân trong suốt quá trình; còn hồ sơ `qa_cn14` thì mất căn hộ (danh sách căn hộ thành rỗng) và không được khôi phục khi kích hoạt lại.
- **Nguyên nhân:** `ApartmentService.deleteResident(Resident)` truyền chính tập `resident.getApartmentNumbers()` vào `deleteResident(Set, Resident)`; dòng `removeAll` đầu tiên làm rỗng tập này trước vòng lặp, nên vòng lặp không gỡ căn hộ nào.
- **Bằng chứng:** BC-01, dòng TH-06.

### LOI-04 – Khoản đóng góp tạo theo hồ sơ cư dân, lệch với căn hộ

- **Bước:** sau TH-01 và TH-06, tạo đợt đóng góp và gọi `create-for-all` với 100.000 đ.
- **Mong đợi:** mọi căn hộ đang có cư dân (`A0012`, `A0023`, `A0024`, `A0031`) nhận khoản đóng góp.
- **Thực tế:** nhận khoản là `A0012`, `A0023`, `A0024`, `A0035`; `A0031` (đang có cư dân) không nhận, `A0035` (căn hộ trống) lại nhận.
- **Nguyên nhân:** `ContributionService.createContributionForApartment` tìm cư dân theo hồ sơ (`residentRepository.findByApartmentNumber`), trong khi màn căn hộ dùng `apartment.residentIds`. Hai nguồn này lệch nhau do LOI-02 và LOI-03. Sửa hai lỗi đó sẽ hết lệch; nên dùng chung một nguồn dữ liệu.
- **Bằng chứng:** BC-01, dòng TH-07.

### LOI-05 – Thêm căn hộ bỏ qua trạng thái

- **Bước:** `POST /api/admin/apartment-list/add-apartment` với `status: "OCCUPIED"`.
- **Mong đợi:** căn hộ lưu trạng thái `OCCUPIED` (US02: thêm căn hộ gồm trạng thái).
- **Thực tế:** lưu `VACANT`; các thuộc tính khác đúng.
- **Nguyên nhân:** `ApartmentService.saveApartment` không gọi `setStatus`.
- **Bằng chứng:** BC-01, dòng CN-16.

### LOI-06 – Thêm căn hộ trùng số trả lỗi 500

- **Bước:** thêm lại căn hộ `B0101` đã tồn tại.
- **Mong đợi:** 400 kèm thông báo "Số căn hộ đã tồn tại".
- **Thực tế:** 500 "Runtime Exception occurred: could not execute statement…" (vi phạm ràng buộc `unique` của database).
- **Bằng chứng:** BC-01, dòng CN-16.

### LOI-07 – Không có nút thêm căn hộ trên giao diện

- **Bước:** đăng nhập `admin`, mở Apartment Management.
- **Mong đợi:** có nút mở form tạo căn hộ.
- **Thực tế:** chỉ có **Filter**, **Select All**, **Set Status**. `ApartmentTable.js` có sẵn chế độ `create` gọi `add-apartment` nhưng không nút nào chuyển sang chế độ này, nên chỉ thêm căn hộ được qua API.
- **Bằng chứng:** BC-02, GD-10.

### LOI-08 – Đơn giá âm bị đổi thành 0 và lưu

- **Bước:** Fee Unit Management, nhập -1000 vào Hourly Parking, bấm **Save Changes**.
- **Mong đợi:** báo lỗi, giữ giá cũ 5.000 đ/giờ.
- **Thực tế:** ô tự đổi thành 0 (do `NumberInput min={0}`), hiện "Fee unit settings saved successfully", giá gửi xe theo giờ trong database thành 0. Backend vẫn chặn giá âm đúng (CN-21), lỗi nằm ở giao diện.
- **Bằng chứng:** BC-02, GD-18.

### LOI-09 – Ô Username gợi ý nhập email

- **Bước:** mở Sign In và Sign Up.
- **Mong đợi:** ô Username là ô chữ thường, gợi ý tên đăng nhập.
- **Thực tế:** ô có `type="email"` và gợi ý `mail@simmmple.com` (Sign In), `username` (Sign Up). Người dùng dễ nhập email (ví dụ `admin@gmail.com`) và đăng nhập thất bại vì hệ thống chỉ nhận tên đăng nhập. Ở Sign Up, nhãn của ô Phone và Age bị gắn nhầm vào ô khác (trình đọc màn hình đọc là "Username", "Full name").
- **Bằng chứng:** BC-02, GD-01, GD-04.

### LOI-10 – Cư dân mở được trang quản trị bằng URL

- **Bước:** đăng nhập `cudan01`, gõ `/admin/bill`.
- **Mong đợi:** bị chặn hoặc chuyển về trang cư dân.
- **Thực tế:** trang mở được, hiện menu quản trị và nút **New Bill**; bảng trống vì API trả 403. Dữ liệu vẫn được bảo vệ, nhưng giao diện gây hiểu nhầm. `AuthGuard` chỉ kiểm tra có token, không kiểm tra vai trò.
- **Bằng chứng:** BC-02, GD-23.

### LOI-11 – Mô tả khoản phí tự sinh bị lặp số căn hộ

- **Thực tế:** "phí thuê căn hộ A0012A0012", "phí dịch vụ căn hộA0012A0012", "phí quản lý căn hộA0012A0012".
- **Nguyên nhân:** `ApartmentService.updateResident` đã nối số căn hộ vào mô tả, `BillService.saveApartmentBill` lại nối thêm lần nữa; hai mô tả sau thiếu dấu cách.
- **Bằng chứng:** BC-01, dòng TH-02; BC-02, GD-22.

### LOI-12 – Log khởi động sai số căn hộ

- **Thực tế:** log in "Đã khởi tạo 150 căn hộ!" nhưng vòng lặp chỉ tạo 10 tầng × 5 căn = 50 căn hộ (`A0001`–`A0050`). Nhánh tạo `PENHOUSE` cho tầng 15 không bao giờ chạy.
- **Bằng chứng:** BC-03.

### LOI-13 – Nút "Sign in with Google" không có chức năng

- **Thực tế:** bấm nút trên Sign In/Forgot password không chuyển trang, không gửi request, không có thông báo. Đăng nhập Google không nằm trong User Story nào; nên ẩn nút.
- **Bằng chứng:** BC-02, ghi chú ở GD-06.
