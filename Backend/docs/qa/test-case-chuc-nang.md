# Test case chức năng (30)

Kiểm thử qua REST API của backend, mỗi case ứng với một tiêu chí chấp nhận của User Story. Cả 30 case được tự động hóa trong [tu-dong/kiem_thu_api.py](tu-dong/kiem_thu_api.py), cùng mã `CN-xx`. Kết quả chạy ở [ket-qua-thuc-thi.md](ket-qua-thuc-thi.md).

**Tiền điều kiện chung:** backend vừa khởi động với database trống (có 50 căn hộ `A0001`–`A0050` và 5 tài khoản mẫu ở bộ dữ liệu [DL-01](du-lieu-kiem-thu.md#dl-01-tài-khoản-mẫu)); SMTP giả đang chạy; các case chạy theo thứ tự vì case sau dùng tài khoản do case trước tạo.

Mức ưu tiên: **C** (cao), **TB** (trung bình), **T** (thấp).

## US21 – Đăng ký tài khoản và xác minh email bằng OTP

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-01 | Đăng ký hợp lệ và xác minh OTP | `POST /api/auth/register` với `qa_cn01`, mật khẩu `Dangky@123`, email `qa.cn01@bluemoon.test`; `GET /api/auth/send-otp`; lấy OTP trong email; `POST /api/auth/verify-otp` | Xác minh trả 200 "Xác thực thành công!"; đăng nhập `qa_cn01` được | C |
| CN-02 | Dữ liệu đăng ký sai định dạng | Đăng ký với mật khẩu `abc12345` (thiếu chữ hoa, ký tự đặc biệt) và số điện thoại 6 chữ số | 400, trả lỗi ở cả hai trường `password` và `phone`; không tạo phiên đăng ký | C |
| CN-03 | OTP sai rồi gửi lại OTP | Đăng ký `qa_cn03`; nhập OTP sai; `POST /api/auth/resend-otp`; nhập OTP mới | OTP sai trả 400 "OTP không đúng"; gửi lại 200; OTP mới 200 và tài khoản đăng nhập được | C |

## US22 – Đăng nhập, đổi mật khẩu, quên mật khẩu

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-04 | Đăng nhập đúng nhận JWT | `POST /api/auth/login` với `admin` và `cudan01` | 200, JWT gồm 3 phần; vai trò trong token là `ROLE_ADMIN` và `ROLE_USER` | C |
| CN-05 | Sai mật khẩu hoặc tài khoản bị khóa | Đăng nhập `cudan01` mật khẩu sai; đăng nhập `cudankhoa` (đã vô hiệu hóa) đúng mật khẩu | Cả hai trả 401, không có token | C |
| CN-06 | Đổi mật khẩu cần mật khẩu cũ | `qa_cn01` gọi `POST /api/user/change-password` với mật khẩu cũ sai, rồi với mật khẩu cũ đúng và mật khẩu mới `MoiMoi@123` | Lần sai trả 400 `error_wrong_old_password`; lần đúng 200; mật khẩu mới đăng nhập được, mật khẩu cũ không | C |
| CN-07 | Quên mật khẩu, đặt lại bằng OTP | `POST /api/auth/forgot-password` cho `qa_cn03`; lấy OTP gửi tới `qa.cn03@bluemoon.test`; `POST /api/auth/reset-password` với mật khẩu mới `DatLai@123` | 200 "Password changed successfully"; mật khẩu mới đăng nhập được, mật khẩu cũ không | C |
| CN-08 | Không dùng OTP của email khác để đặt lại | Lấy OTP đăng ký gửi tới `qa.cn08@bluemoon.test`, rồi gửi `reset-password` cho `cudan02` kèm email và OTP đó | 400; mật khẩu của `cudan02` không đổi | C |
| CN-09 | OTP bị hủy sau 3 lần nhập sai | Yêu cầu OTP quên mật khẩu cho `cudan02`; nhập sai 3 lần; nhập OTP đúng | 3 lần sai đều 400; OTP đúng sau đó cũng 400 vì đã bị hủy; mật khẩu không đổi | C |

## US23 – Quản trị tài khoản và phân quyền

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-10 | Đổi vai trò tài khoản | `admin` gọi `POST /api/admin/users/edit/{id}` đổi `qa_cn01` sang `ADMIN`, sau đó đổi lại `USER` | 200; token mới của `qa_cn01` có `ROLE_ADMIN` | C |
| CN-11 | Vô hiệu hóa rồi kích hoạt một tài khoản | `POST /api/admin/users/deactivate/{id}` cho `qa_cn03`, thử đăng nhập; `POST .../activate/{id}`, thử đăng nhập | Sau khi khóa không đăng nhập được; sau khi mở đăng nhập lại được | C |
| CN-12 | Vô hiệu hóa hàng loạt | `POST /api/admin/users/batch/deactivate` với `qa_cn01`, `qa_cn03` và `admin` | 200, `deactivatedCount` = 2, `failedIds` chỉ chứa id của `admin`; hai tài khoản bị khóa, `admin` vẫn đăng nhập được | C |
| CN-13 | Chặn truy cập API quản trị | Gọi `GET /api/admin/users` bằng token cư dân và không có token; cư dân gọi `GET /api/fee-units` | Cả ba trả 403 | C |

## US01 – Hồ sơ cư dân

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-14 | Thêm cư dân gắn căn hộ | `POST /api/admin/users/add` tạo `qa_cn14` (họ tên, tuổi, SĐT `0912000014`, email, trạng thái `THUONGTRU`) gắn căn hộ `A0031` | 200; danh sách tài khoản có `qa_cn14` với căn hộ `A0031` và đúng SĐT | C |
| CN-15 | Thêm cư dân dữ liệu sai | Thêm cư dân gắn căn hộ `Z9999` không tồn tại; thêm cư dân mật khẩu `yeu` | Cả hai trả 400 kèm lỗi theo trường; không tạo tài khoản nào | TB |

## US02 – Căn hộ

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-16 | Thêm căn hộ đủ thuộc tính | `POST /api/admin/apartment-list/add-apartment` với `B0101`, 2 phòng, tầng 11, 68,5 m², `STANDARD`, trạng thái `OCCUPIED`; thêm lại `B0101` | Tạo 201 và lưu đúng cả 4 thuộc tính, gồm trạng thái `OCCUPIED`; thêm trùng số căn hộ trả 400 kèm thông báo | C |
| CN-17 | Cập nhật trạng thái hàng loạt | `POST /api/apartments/batch-update-status` cho `A0041`, `A0042` sang `OCCUPIED`; gửi lại với trạng thái `KHONGCO` | Lần 1 trả 200 và cả hai căn hộ thành `OCCUPIED`; trạng thái không hợp lệ trả 400 | C |

## US03 – Lọc căn hộ và xem cư dân

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-18 | Lọc theo tầng, loại, trạng thái | `GET /api/apartments/filter?floors=1&type=KIOT&status=VACANT` | Trả đúng 5 căn hộ tầng 1: `A0001`–`A0005` | TB |
| CN-19 | Xem cư dân trong căn hộ | `GET /api/admin/apartment-list/residents/{id}` của `A0023` | Trả đúng một cư dân "Nguyễn Thị C" (`cudan02`) | TB |

## US05 – Bảng đơn giá

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-20 | Lưu đơn giá gồm phí gửi xe | `POST /api/fee-units` với điện 3.800 đ/kWh, nước 18.000 đ/m³, gửi xe 120.000 đ/tháng và 5.000 đ/giờ | 200; đọc lại `GET /api/fee-units` đúng 4 giá vừa lưu | C |
| CN-21 | Đơn giá âm bị từ chối | Lưu bảng giá với phí gửi xe theo giờ = -1.000 | 400 "Giá trị phí không thể là số âm!"; bảng giá giữ nguyên | TB |

## US06 – Khoản thu

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-22 | Tạo khoản thu và tìm theo căn hộ | `POST /api/admin/bills`: `A0012`, `SERVICE_COST`, 350.000 đ, hạn đóng hôm nay; `GET /api/bills/filter?apartmentNumber=A0012&description=QA` | Tạo 200; tìm thấy đúng 1 khoản, trạng thái `UNPAID` | C |
| CN-23 | Khoản thu sai dữ liệu | Tạo khoản thu cho căn hộ `1`; tạo khoản thu số tiền 0, hạn đóng hôm qua | Cả hai 400; lỗi trả theo trường: lần 1 `apartmentNumber`, lần 2 `amount` và `dueDate` | C |
| CN-24 | Sửa và xóa khoản thu | Tạo khoản 50.000 đ cho `A0024`; `PUT /api/admin/bills/edit/{id}` sửa thành 65.000 đ; `DELETE /api/admin/bills/{id}`; xem lại | Sửa 200, số tiền thành 65.000; xóa 204; xem lại 404 | TB |

## US07 – Khoản thu điện, nước hàng loạt

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-25 | Tạo hàng loạt theo lượng tiêu thụ | `POST /api/utility-bills/generate`: `A0012` dùng 120 kWh và 8 m³, `A0023` dùng 75 kWh, ô nước để trống | Tạo đúng 3 khoản; số tiền = lượng tiêu thụ × đơn giá hiện hành; không tạo khoản nước cho `A0023` | C |

## US08 – Cư dân xem khoản phải thu

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-26 | Chỉ thấy khoản thu căn hộ mình | `cudan01` (căn hộ `A0012`) gọi `GET /api/bills/list` | 200; mọi khoản thu đều thuộc `A0012` | C |
| CN-27 | Không xem được căn hộ khác | `cudan01` mở một khoản thu của `A0023` và gọi `GET /api/user/apartment-detail?apartmentNumber=A0023` | Cả hai trả 403 | C |

## US12 – Xác nhận thanh toán tiền mặt

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-28 | Xác nhận thanh toán thủ công | `cudan01` gọi `POST /api/admin/bills/{id}/confirm-payment` cho khoản ở CN-22; `admin` gọi lại; `admin` gọi lần hai | Cư dân 403; `admin` 200 và khoản thu thành `PAID`; xác nhận lần hai 400 | C |

## US15 – Đợt đóng góp

| Mã | Tên | Bước và dữ liệu | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|:---:|
| CN-29 | Tạo loại và đợt đóng góp | `POST /api/contribution-types/create` "QA Quỹ khuyến học"; `POST /api/contributions/admin/create` "QA Khuyến học cuối năm", mục tiêu 20.000.000 đ, từ hôm nay đến 30 ngày sau | Cả hai 200; đợt có trong danh sách, trạng thái `ACTIVE`, đúng mục tiêu | C |
| CN-30 | Đóng, mở lại, hủy đợt | Trên đợt của CN-29 lần lượt gọi `close`, `reactivate`, `cancel`, `reactivate` | Ba bước đầu 200; mở lại đợt đã hủy trả 400 | TB |
