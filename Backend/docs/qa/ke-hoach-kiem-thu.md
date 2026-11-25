# Kế hoạch kiểm thử – BlueMoon ver1 (Sprint 1)

| Mục | Nội dung |
|---|---|
| Sản phẩm | BlueMoon – hệ thống quản lý cư dân, căn hộ và thu phí chung cư |
| Phiên bản | ver1 (Sprint 1), nhánh `main`: lần 1 tại commit `4ffb52e`, lần 2 (hồi quy) tại commit `5ec2491` |
| Người lập | Nguyễn Hoàng Giang (kiểm thử) |
| Người duyệt | Nguyễn Đình Nam Khánh |
| Ngày lập | 26/11/2026 |

## 1. Mục tiêu

- Xác nhận 12 User Story của Sprint 1 đáp ứng tiêu chí chấp nhận đã chốt với PO.
- Phát hiện lỗi về nghiệp vụ, phân quyền, tính nhất quán dữ liệu giữa các module và giao diện trước buổi nghiệm thu ver1.
- Có số liệu đạt/không đạt làm căn cứ quyết định nghiệm thu và lập danh sách sửa lỗi.

## 2. Phạm vi

### 2.1 Trong phạm vi

| Epic | User Story | Nội dung kiểm thử |
|---|---|---|
| EP-05 Tài khoản & phân quyền | US21, US22, US23 | Đăng ký kèm OTP, đăng nhập JWT, đổi/quên mật khẩu, quản trị tài khoản, phân quyền ADMIN/USER |
| EP-01 Cư dân & căn hộ | US01, US02, US03 | Hồ sơ cư dân, căn hộ, cập nhật trạng thái hàng loạt, lọc căn hộ, xem cư dân trong căn hộ |
| EP-02 Thu phí | US05, US06, US07, US08, US12 | Bảng đơn giá, khoản thu, khoản thu điện nước hàng loạt, cư dân xem khoản thu, xác nhận thanh toán tiền mặt |
| EP-03 Đóng góp | US15 | Loại đóng góp, đợt đóng góp, đóng/hủy/mở lại, tạo khoản đóng góp cho toàn bộ căn hộ |

Kiểm thử thêm hai phần đã có trong ver1: trang chủ hiển thị sự kiện cộng đồng theo ngày hiện tại, và tài khoản mẫu tạo sẵn khi khởi động.

### 2.2 Ngoài phạm vi

- Các chức năng thuộc Sprint 2: hóa đơn tổng hợp Word/PDF (US09), thanh toán QR SePay (US10, US11), xuất Excel (US04, US13), gửi xe (US14), cư dân đăng ký đóng góp (US16), thông báo và phản ánh (US17–US20). Một số phần đã có code (xuất Excel, cư dân đóng góp) nhưng không được đánh giá trong đợt này.
- Kiểm thử hiệu năng (NFR-001: 10.000 bản ghi, ≤ 3 giây) và kiểm thử bảo mật chuyên sâu: thuộc giai đoạn kiểm thử hệ thống tháng 12/2026.
- Kiểm thử trên PostgreSQL thật và Gmail thật (xem mục 5 và rủi ro R1).

## 3. Cách tiếp cận

| Mức | Cách làm | Công cụ |
|---|---|---|
| Đơn vị | Chạy bộ test JUnit có sẵn của backend | `./mvnw test` |
| Chức năng (30 case) | Gọi REST API theo từng tiêu chí chấp nhận, kiểm tra mã trạng thái, dữ liệu trả về và dữ liệu sau thao tác | Script `tu-dong/kiem_thu_api.py` (Python, chỉ dùng thư viện chuẩn) |
| Tích hợp (8 case) | Kiểm tra dữ liệu đi qua nhiều module: tài khoản → căn hộ → khoản thu → đóng góp | Cùng script trên |
| Giao diện (24 case) | Thao tác trên trình duyệt như người dùng: nhập liệu, bấm nút, đọc thông báo; đối chiếu dữ liệu hiển thị với API | Trình duyệt Chromium, React dev server |
| Kịch bản (7) | Ghép các case thành luồng nghiệp vụ trọn vẹn của từng vai trò | Theo các case ở trên |

Kỹ thuật thiết kế case: phân vùng tương đương (dữ liệu hợp lệ/không hợp lệ), giá trị biên (hạn đóng hôm qua/hôm nay, số tiền 0, đơn giá âm, OTP sai lần thứ 3), bảng quyết định cho phân quyền (super admin, ADMIN thường, cư dân, chưa đăng nhập) và kiểm thử dựa trên trạng thái (đợt đóng góp ACTIVE → CLOSED → ACTIVE → CANCELED).

## 4. Tiêu chí

**Bắt đầu:** backend build thành công; database trống, backend vừa khởi động nên đã tạo 50 căn hộ mẫu và 5 tài khoản mẫu; SMTP giả đang chạy; frontend kết nối được backend.

**Kết thúc đợt:** đã chạy hết 62 case; mọi case không đạt đều có lỗi tương ứng trong báo cáo lỗi kèm bằng chứng.

**Đạt để nghiệm thu ver1:** không còn lỗi mức Cao đang mở; tỉ lệ đạt ≥ 90%; mỗi User Story có ít nhất một case đạt cho luồng chính.

## 5. Môi trường

| Thành phần | Cấu hình dùng khi chạy |
|---|---|
| Hệ điều hành | Windows 11 Home |
| Backend | Spring Boot 3.4.3, JDK 17.0.21, chạy bằng `mvnw spring-boot:run` |
| Database | H2 in-memory, chế độ tương thích PostgreSQL (`MODE=PostgreSQL`), tạo mới mỗi lần khởi động |
| Email OTP | `scripts/smtp_stub.py` (SMTP giả ở cổng 2525, ghi email vào tệp log) |
| Frontend | React 18 + Chakra UI, `npm start` ở `http://localhost:3000`, Node.js v26.13.1 |
| Trình duyệt | Chromium |

Máy kiểm thử chưa cài Docker nên không chạy được PostgreSQL bằng `docker compose`. Database H2 dùng đúng các entity và Hibernate như bản PostgreSQL; phần khác biệt về kiểu dữ liệu được ghi ở rủi ro R1.

## 6. Lịch và phân công

| Việc | Người thực hiện | Thời gian |
|---|---|---|
| Lập kế hoạch, thiết kế case, chuẩn bị dữ liệu | Nguyễn Hoàng Giang | 26/11/2026 |
| Chạy kiểm thử API (chức năng, tích hợp) | Nguyễn Hoàng Giang | 26/11/2026, 05:20–05:21 |
| Chạy kiểm thử giao diện | Nguyễn Hoàng Giang | 26/11/2026 |
| Sửa lỗi (bản `c2dd81c`) | Nguyễn Đình Nam Khánh, Đặng Thiệu Minh | 26/11/2026 |
| Kiểm thử hồi quy theo checklist (lần 2) | Nguyễn Hoàng Giang | 26/11/2026, API 05:37–05:38, sau đó giao diện |
| Sửa LOI-14 và hồi quy lần 3 (API, test đơn vị) | Phát triển (phụ trách US23: Đặng Thiệu Minh), sau đó kiểm thử (Nguyễn Hoàng Giang) | 26/11/2026, API 05:47–05:48 |
| Sửa các lỗi còn mở (LOI-08, LOI-09, LOI-10, LOI-11, LOI-13) | Nguyễn Đình Nam Khánh, Đặng Thiệu Minh | Sprint 2 |
| Duyệt kết quả, quyết định nghiệm thu | Nguyễn Đình Nam Khánh | Sau hồi quy |

## 7. Rủi ro

| Mã | Rủi ro | Cách giảm thiểu |
|---|---|---|
| R1 | Chạy trên H2 thay vì PostgreSQL, có thể khác về ràng buộc và kiểu dữ liệu | Chạy lại script API trên PostgreSQL khi môi trường có Docker; ERD trong `docs/diagram/erd` lấy theo DDL PostgreSQL |
| R2 | OTP gửi qua SMTP giả, chưa thử với Gmail thật | Kiểm tra gửi Gmail thật trong UAT |
| R3 | Mỗi email chỉ được yêu cầu 3 OTP trong 15 phút, chạy lại liên tục có thể bị chặn | Mỗi case dùng một email riêng; khởi động lại backend trước mỗi lần chạy |
| R4 | Kiểm thử giao diện làm thủ công nên khó lặp lại giống hệt | Ghi giá trị quan sát được vào bằng chứng `BC-02` |

## 8. Sản phẩm bàn giao

Kế hoạch này; 30 + 24 + 8 test case; 7 kịch bản; 5 bộ dữ liệu; báo cáo thực thi; báo cáo lỗi; báo cáo kiểm thử; 3 bằng chứng; checklist hồi quy; script kiểm thử API.
