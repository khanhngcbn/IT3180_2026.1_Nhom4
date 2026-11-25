# Báo cáo kiểm thử – BlueMoon ver1 (Sprint 1)

| Mục | Nội dung |
|---|---|
| Người lập | Nguyễn Hoàng Giang (kiểm thử) |
| Người duyệt | Nguyễn Đình Nam Khánh |
| Phát triển | Nguyễn Đình Nam Khánh, Đặng Thiệu Minh |
| Ngày kiểm thử | 26/11/2026 |
| Lần 1 | nhánh `main` tại commit `4ffb52e` |
| Lần 2 (hồi quy) | nhánh `main` tại commit `5ec2491`, sau bản sửa lỗi `c2dd81c` |
| Lần 3 | sau bản sửa LOI-14; chạy lại API và test đơn vị |

## 1. Kết luận

**Đủ tiêu chí nghiệm thu ver1 theo [kế hoạch](ke-hoach-kiem-thu.md#4-tiêu-chí) sau lần 3.** Quyết định cuối cùng thuộc người duyệt.

| Tiêu chí | Kết quả |
|---|---|
| Tỉ lệ đạt ≥ 90% | 96,8% (60/62) |
| Không còn lỗi mức Cao đang mở | Đạt: LOI-01, LOI-02 sửa ở lần 2; LOI-14 phát hiện ở lần 2 và sửa ở lần 3 |
| Mỗi User Story có ít nhất một case đạt cho luồng chính | Đạt cả 12 User Story |

Còn 5 lỗi chưa sửa xong, không chặn nghiệm thu, đề xuất chuyển sang Sprint 2:
- **Trung bình:** LOI-08, đơn giá âm bị đổi thành 0 rồi lưu. Nên sửa sớm vì làm sai bảng giá mà không có cảnh báo.
- **Sửa một phần:** LOI-09, ô Username ở màn Sign Up.
- **Thấp:** LOI-10 (cư dân mở được trang quản trị qua URL), LOI-11 (mô tả phí lặp số căn hộ), LOI-13 (nút Google không có chức năng).

## 2. Số liệu

| Nhóm | Số case | Đạt lần 1 | Đạt lần 2 |
|---|:---:|:---:|:---:|
| Chức năng (API) | 30 | 29 (96,7%) | 30 (100%) |
| Tích hợp (API) | 8 | 4 (50,0%) | 8 (100%) |
| Giao diện (trình duyệt) | 24 | 20 (83,3%) | 22 (91,7%) |
| **Tổng** | **62** | **53 (85,5%)** | **60 (96,8%)** |
| Test đơn vị backend | 9 | 9 | 9 |
| Kịch bản nghiệp vụ | 7 | 3 | 5 |

Lần 3 chạy lại 38 case API (38/38 đạt) và 9 test đơn vị (9/9 đạt). Giao diện không chạy lại vì bản sửa chỉ thay đổi backend, nên tổng sau lần 3 vẫn là 60/62.

Lỗi: 14 lỗi, gồm 3 Cao, 5 Trung bình và 6 Thấp. Sau lần 3 có 9 lỗi đã sửa, 1 lỗi sửa một phần và 4 lỗi còn mở; không còn lỗi mức Cao. Chi tiết ở [báo cáo lỗi](bao-cao-loi.md); kết quả từng case ở [báo cáo thực thi](ket-qua-thuc-thi.md).

## 3. Kết quả theo User Story

| US | Nội dung | Case | Lần 1 | Lần 2 | Lỗi còn mở |
|---|---|---|:---:|:---:|---|
| US21 | Đăng ký + OTP | CN-01…03, TH-01, GD-04, GD-05 | 5/6 | 6/6 | LOI-09 (ô Username ở Sign Up) |
| US22 | Đăng nhập, đổi/quên mật khẩu | CN-04…09, GD-01…03, GD-06, GD-24 | 10/11 | 11/11 | LOI-13 |
| US23 | Quản trị tài khoản, phân quyền | CN-10…13, TH-06, TH-08, GD-11, GD-12, GD-23 | 6/9 | 8/9 | LOI-10 (LOI-14 đã sửa ở lần 3) |
| US01 | Hồ sơ cư dân | CN-14, CN-15, TH-02 | 3/3 | 3/3 | – |
| US02 | Căn hộ, trạng thái hàng loạt | CN-16, CN-17, GD-09, GD-10 | 2/4 | 4/4 | – |
| US03 | Lọc căn hộ, xem cư dân | CN-18, CN-19 | 2/2 | 2/2 | – |
| US05 | Bảng đơn giá | CN-20, CN-21, TH-03, GD-17, GD-18 | 4/5 | 4/5 | LOI-08 |
| US06 | Khoản thu | CN-22…24, GD-13…16 | 7/7 | 7/7 | LOI-11 |
| US07 | Điện nước hàng loạt | CN-25, GD-19 | 2/2 | 2/2 | – |
| US08 | Cư dân xem khoản thu | CN-26, CN-27, TH-04, GD-21, GD-22 | 5/5 | 5/5 | – |
| US12 | Xác nhận thanh toán | CN-28, TH-05 | 2/2 | 2/2 | – |
| US15 | Đợt đóng góp | CN-29, CN-30, TH-07, GD-20 | 3/4 | 4/4 | – |
| Khác | Sự kiện theo ngày thực | GD-07, GD-08 | 2/2 | 2/2 | – |

Một case có thể thuộc nhiều User Story, nên tổng ở bảng này lớn hơn 62.

## 4. Đánh giá chất lượng

**Làm tốt:**
- Kiểm tra dữ liệu đầu vào trả lỗi rõ ràng theo từng trường, cả ở API và giao diện khoản thu.
- Các API dành cho Ban quản lý đều chặn cư dân và người chưa đăng nhập (403).
- OTP chỉ dùng một lần, bị hủy sau 3 lần nhập sai, và không dùng được OTP của email khác để đổi mật khẩu.
- Bản sửa `c2dd81c` đã làm dữ liệu cư dân và căn hộ đồng bộ ở cả ba luồng: đăng ký, khóa/mở tài khoản, tạo khoản đóng góp. Cả 4 case tích hợp hỏng ở lần 1 đều đạt ở lần 2.

**Còn yếu:** phân quyền giữa super admin và ADMIN thường được bổ sung dần qua hai lần sửa. Lần 2 sửa khóa, mở, xóa; lần 3 mới sửa thêm API sửa tài khoản (LOI-14). Nay cả bốn API đơn lẻ và API khóa hàng loạt dùng chung một quy tắc. Ở giao diện, trang quản trị chưa chặn theo vai trò (LOI-10).

**Giới hạn của đợt kiểm thử:**
- Chạy trên H2 thay vì PostgreSQL, dùng SMTP giả thay vì Gmail (rủi ro R1, R2 trong kế hoạch).
- Chưa kiểm thử hiệu năng.
- Giao diện mới kiểm tra trên một trình duyệt.

## 5. Đề xuất

1. Người duyệt xem xét nghiệm thu ver1 dựa trên kết quả lần 3.
2. Đưa các lỗi còn mở vào Sprint Backlog Sprint 2. LOI-08 sửa trước.
3. Sau mỗi lần sửa, chạy lại `tu-dong/kiem_thu_api.py` trên database mới và làm theo [checklist hồi quy](checklist-hoi-quy.md). TH-08 đã được mở rộng để bắt lại lỗi kiểu LOI-14. Nên chạy thêm một lần trên PostgreSQL thật trước UAT.
4. Đưa script kiểm thử API vào quy trình trước mỗi lần bàn giao. Ở đợt này, mỗi lần chạy chỉ mất khoảng 20 giây, phát hiện 5 lỗi tích hợp và xác nhận được cả hai bản sửa.
