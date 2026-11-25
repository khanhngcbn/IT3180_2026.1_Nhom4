# Báo cáo kiểm thử – BlueMoon ver1 (Sprint 1)

| Mục | Nội dung |
|---|---|
| Người lập | Nguyễn Hoàng Giang (kiểm thử) |
| Người duyệt | Nguyễn Đình Nam Khánh |
| Phát triển | Nguyễn Đình Nam Khánh, Đặng Thiệu Minh |
| Ngày kiểm thử | 26/11/2026 |
| Lần 1 | nhánh `main` tại commit `4ffb52e` |
| Lần 2 (hồi quy) | nhánh `main` tại commit `5ec2491`, sau bản sửa lỗi `c2dd81c` |

## 1. Kết luận

**Chưa đạt điều kiện nghiệm thu ver1, nhưng đã gần đạt.**

- Lần 2 đạt 96,8% (60/62 case), vượt mức 90% đặt ra trong [kế hoạch](ke-hoach-kiem-thu.md#4-tiêu-chí).
- Hai lỗi mức Cao của lần 1 (LOI-01, LOI-02) đã được sửa và kiểm tra lại.
- Vẫn còn một lỗi mức Cao mới phát hiện khi kiểm thử hồi quy, nên chưa thể nghiệm thu: **LOI-14**, tài khoản ADMIN thường (kế toán) vẫn sửa được tài khoản super admin và hạ `admin` xuống `USER`.

Sau khi sửa LOI-14 và chạy lại mục B của [checklist hồi quy](checklist-hoi-quy.md), có thể đề xuất nghiệm thu. LOI-08 (đơn giá âm bị đổi thành 0) mức Trung bình nên sửa cùng đợt, vì làm sai lệch bảng giá mà không có cảnh báo.

## 2. Số liệu

| Nhóm | Số case | Đạt lần 1 | Đạt lần 2 |
|---|:---:|:---:|:---:|
| Chức năng (API) | 30 | 29 (96,7%) | 30 (100%) |
| Tích hợp (API) | 8 | 4 (50,0%) | 8 (100%) |
| Giao diện (trình duyệt) | 24 | 20 (83,3%) | 22 (91,7%) |
| **Tổng** | **62** | **53 (85,5%)** | **60 (96,8%)** |
| Test đơn vị backend | 9 | 9 | 9 |
| Kịch bản nghiệp vụ | 7 | 3 | 5 |

Lỗi: 14 lỗi, gồm 3 Cao, 5 Trung bình và 6 Thấp. Sau lần 2 có 8 lỗi đã sửa, 1 lỗi sửa một phần và 5 lỗi còn mở. Chi tiết ở [báo cáo lỗi](bao-cao-loi.md); kết quả từng case ở [báo cáo thực thi](ket-qua-thuc-thi.md).

## 3. Kết quả theo User Story

| US | Nội dung | Case | Lần 1 | Lần 2 | Lỗi còn mở |
|---|---|---|:---:|:---:|---|
| US21 | Đăng ký + OTP | CN-01…03, TH-01, GD-04, GD-05 | 5/6 | 6/6 | LOI-09 (ô Username ở Sign Up) |
| US22 | Đăng nhập, đổi/quên mật khẩu | CN-04…09, GD-01…03, GD-06, GD-24 | 10/11 | 11/11 | LOI-13 |
| US23 | Quản trị tài khoản, phân quyền | CN-10…13, TH-06, TH-08, GD-11, GD-12, GD-23 | 6/9 | 8/9 | LOI-10, **LOI-14** |
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

**Còn yếu:** phân quyền giữa super admin và ADMIN thường mới được bổ sung cho các thao tác khóa, mở, xóa, nhưng còn sót API sửa tài khoản (LOI-14). Ở giao diện, trang quản trị chưa chặn theo vai trò (LOI-10). Nên rà lại toàn bộ API trong `/api/admin/users/**` theo cùng một quy tắc.

**Giới hạn của đợt kiểm thử:**
- Chạy trên H2 thay vì PostgreSQL, dùng SMTP giả thay vì Gmail (rủi ro R1, R2 trong kế hoạch).
- Chưa kiểm thử hiệu năng.
- Giao diện mới kiểm tra trên một trình duyệt.

## 5. Đề xuất

1. **Sửa ngay:** LOI-14 (Cao): chặn `POST /api/admin/users/edit/{id}` theo cùng quy tắc với khóa/mở/xóa.
2. **Sửa cùng đợt:** LOI-08 (Trung bình), và phần còn lại của LOI-09 ở màn Sign Up.
3. **Sửa khi tiện:** LOI-10, LOI-11, LOI-13 (Thấp).
4. Sau khi sửa, chạy lại `tu-dong/kiem_thu_api.py` trên database mới và làm theo [checklist hồi quy](checklist-hoi-quy.md). Nên thêm một case API riêng cho LOI-14 vào script. Nên chạy thêm một lần trên PostgreSQL thật.
5. Đưa script kiểm thử API vào quy trình trước mỗi lần bàn giao. Lần này script đã phát hiện ngay 5 lỗi tích hợp và xác nhận bản sửa chỉ trong khoảng 20 giây chạy.
