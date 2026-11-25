# Báo cáo kiểm thử – BlueMoon ver1 (Sprint 1)

| Mục | Nội dung |
|---|---|
| Người lập | Nguyễn Hoàng Giang (kiểm thử) |
| Người duyệt | Nguyễn Đình Nam Khánh |
| Phát triển | Nguyễn Đình Nam Khánh, Đặng Thiệu Minh |
| Ngày kiểm thử | 26/11/2026 |
| Mã nguồn | nhánh `main`, sau commit `4ffb52e` |

## 1. Kết luận

**Chưa đạt điều kiện nghiệm thu ver1.** Tỉ lệ đạt chung là 85,5% (53/62 case), thấp hơn mức 90% đặt ra trong [kế hoạch](ke-hoach-kiem-thu.md#4-tiêu-chí). Ngoài ra còn 2 lỗi mức Cao đang mở:

- **LOI-01:** tài khoản ADMIN thường (kế toán) khóa được super admin.
- **LOI-02:** cư dân tự đăng ký kèm căn hộ không được gắn vào căn hộ, nên không có khoản thu nào.

Phần thu phí là phần chạy tốt nhất: tạo khoản thu, khoản thu điện nước hàng loạt, cư dân xem khoản thu, xác nhận thanh toán tiền mặt đều đạt cả ở mức API lẫn giao diện. Phần bảo mật OTP và đặt lại mật khẩu cũng đạt toàn bộ. Lỗi tập trung ở chỗ nối giữa tài khoản, cư dân và căn hộ.

## 2. Số liệu

| Nhóm | Số case | Đạt | Không đạt | Tỉ lệ đạt |
|---|:---:|:---:|:---:|:---:|
| Chức năng (API) | 30 | 29 | 1 | 96,7% |
| Tích hợp (API) | 8 | 4 | 4 | 50,0% |
| Giao diện (trình duyệt) | 24 | 20 | 4 | 83,3% |
| **Tổng** | **62** | **53** | **9** | **85,5%** |
| Test đơn vị backend | 9 | 9 | 0 | 100% |
| Kịch bản nghiệp vụ | 7 | 3 | 4 | 42,9% |

Lỗi: 13 lỗi, gồm 2 Cao, 5 Trung bình và 6 Thấp. Chi tiết ở [báo cáo lỗi](bao-cao-loi.md); kết quả từng case ở [báo cáo thực thi](ket-qua-thuc-thi.md).

## 3. Kết quả theo User Story

| US | Nội dung | Case | Đạt/Tổng | Đánh giá | Lỗi liên quan |
|---|---|---|:---:|---|---|
| US21 | Đăng ký + OTP | CN-01…03, TH-01, GD-04, GD-05 | 5/6 | Luồng OTP đúng; đăng ký kèm căn hộ không gắn căn hộ | LOI-02 |
| US22 | Đăng nhập, đổi/quên mật khẩu | CN-04…09, GD-01…03, GD-06, GD-24 | 10/11 | Đạt về nghiệp vụ và bảo mật OTP; ô Username dễ gây nhập nhầm email | LOI-09, LOI-13 |
| US23 | Quản trị tài khoản, phân quyền | CN-10…13, TH-06, TH-08, GD-11, GD-12, GD-23 | 6/9 | Phân quyền API cho cư dân đúng; thiếu kiểm tra giữa ADMIN thường và super admin; khóa tài khoản làm lệch dữ liệu căn hộ | LOI-01, LOI-03, LOI-10 |
| US01 | Hồ sơ cư dân | CN-14, CN-15, TH-02 | 3/3 | Đạt | – |
| US02 | Căn hộ, trạng thái hàng loạt | CN-16, CN-17, GD-09, GD-10 | 2/4 | Đổi trạng thái hàng loạt đạt; thêm căn hộ chưa đạt cả ở API và giao diện | LOI-05, LOI-06, LOI-07, LOI-12 |
| US03 | Lọc căn hộ, xem cư dân | CN-18, CN-19 | 2/2 | Đạt | – |
| US05 | Bảng đơn giá | CN-20, CN-21, TH-03, GD-17, GD-18 | 4/5 | Backend đạt; giao diện tự đổi giá âm thành 0 và lưu | LOI-08 |
| US06 | Khoản thu | CN-22…24, GD-13…16 | 7/7 | Đạt; mô tả khoản phí tự sinh bị lặp số căn hộ | LOI-11 |
| US07 | Điện nước hàng loạt | CN-25, GD-19 | 2/2 | Đạt | – |
| US08 | Cư dân xem khoản thu | CN-26, CN-27, TH-04, GD-21, GD-22 | 5/5 | Đạt | – |
| US12 | Xác nhận thanh toán | CN-28, TH-05 | 2/2 | Đạt | – |
| US15 | Đợt đóng góp | CN-29, CN-30, TH-07, GD-20 | 3/4 | Vòng đời đợt đóng góp đạt; tạo khoản cho mọi căn hộ bị lệch do dữ liệu cư dân/căn hộ | LOI-04 |
| Khác | Sự kiện theo ngày thực | GD-07, GD-08 | 2/2 | Đạt | – |

Một case có thể thuộc nhiều User Story, nên tổng ở bảng này lớn hơn 62.

## 4. Đánh giá chất lượng

- **Làm tốt:**
  - Kiểm tra dữ liệu đầu vào trả lỗi rõ ràng theo từng trường, cả ở API và giao diện khoản thu.
  - Các API dành cho Ban quản lý đều chặn cư dân và người chưa đăng nhập (403).
  - OTP chỉ dùng một lần, bị hủy sau 3 lần nhập sai, và không dùng được OTP của email khác để đổi mật khẩu.
- **Điểm yếu chính:**
  - Hệ thống lưu liên kết cư dân và căn hộ ở hai nơi: danh sách căn hộ trong hồ sơ cư dân, và danh sách cư dân trong căn hộ. Ba luồng (đăng ký, khóa tài khoản, tạo khoản đóng góp) cập nhật không đồng bộ hai nơi này, gây ra LOI-02, LOI-03 và LOI-04.
  - Phân quyền mới chia hai mức ADMIN/USER. Phân biệt super admin chỉ có ở API khóa hàng loạt và ở giao diện, chưa có ở các API đơn lẻ.
- **Giới hạn của đợt kiểm thử:**
  - Chạy trên H2 thay vì PostgreSQL, và dùng SMTP giả thay vì Gmail (rủi ro R1, R2 trong kế hoạch).
  - Chưa kiểm thử hiệu năng.
  - Giao diện mới kiểm tra trên một trình duyệt, chưa kiểm tra trên điện thoại.

## 5. Đề xuất

1. **Sửa trước khi nghiệm thu:** LOI-01 và LOI-02 (mức Cao), cùng LOI-03 và LOI-04 vì cùng nguyên nhân dữ liệu cư dân/căn hộ.
2. **Sửa trong Sprint 2:** LOI-05…LOI-08 (Trung bình). Riêng LOI-07 nên làm sớm vì US02 là Must have.
3. **Sửa khi tiện:** LOI-09…LOI-13 (Thấp).
4. Sau khi sửa, chạy lại `tu-dong/kiem_thu_api.py` trên database mới và làm theo [checklist hồi quy](checklist-hoi-quy.md). Nên chạy thêm một lần trên PostgreSQL thật.
5. Đưa script kiểm thử API vào quy trình trước mỗi lần bàn giao, để phát hiện sớm các lỗi tích hợp.
