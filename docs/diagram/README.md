# Sơ đồ thiết kế BlueMoon

Mỗi sơ đồ gồm file nguồn PlantUML (`.puml`) và ảnh đã xuất (`.png`) cùng tên. Nội dung bám theo mã nguồn hiện tại trong `Backend` và `Frontend`.

| Loại sơ đồ | Nội dung | Nguồn | Ảnh |
|---|---|---|---|
| Use Case | Tác nhân (khách, cư dân, Ban quản lý/Kế toán, Gmail SMTP) và các chức năng Sprint 1 theo User Story | [01-use-case.puml](01-use-case.puml) | [01-use-case.png](01-use-case.png) |
| Activity | Đăng ký tài khoản và xác minh email bằng OTP (US21) | [02-activity-dang-ky-otp.puml](02-activity-dang-ky-otp.puml) | [02-activity-dang-ky-otp.png](02-activity-dang-ky-otp.png) |
| Activity | Tạo khoản thu điện, nước hàng loạt (US07) | [03-activity-tao-khoan-thu-dien-nuoc.puml](03-activity-tao-khoan-thu-dien-nuoc.puml) | [03-activity-tao-khoan-thu-dien-nuoc.png](03-activity-tao-khoan-thu-dien-nuoc.png) |
| Class | Mô hình dữ liệu: các entity, enum và liên kết giữa chúng | [04-class.puml](04-class.puml) | [04-class.png](04-class.png) |
| Sequence | Đăng nhập JWT và cư dân xem khoản phải thu (US22, US08) | [05-sequence-dang-nhap-jwt.puml](05-sequence-dang-nhap-jwt.puml) | [05-sequence-dang-nhap-jwt.png](05-sequence-dang-nhap-jwt.png) |
| Sequence | Quên mật khẩu, đặt lại bằng OTP (US22) | [06-sequence-quen-mat-khau.puml](06-sequence-quen-mat-khau.puml) | [06-sequence-quen-mat-khau.png](06-sequence-quen-mat-khau.png) |
| Component | Các thành phần frontend, backend (security, controller, service, repository) và hệ thống ngoài | [07-component.puml](07-component.puml) | [07-component.png](07-component.png) |
| Deployment | Trình duyệt, máy chủ web tĩnh, máy chủ ứng dụng Spring Boot, PostgreSQL trong Docker, Gmail SMTP | [08-deployment.puml](08-deployment.puml) | [08-deployment.png](08-deployment.png) |

## Xuất lại ảnh PNG

Cần Java 17 và file `plantuml.jar` (tải tại https://plantuml.com/download). Các sơ đồ Use Case, Class, Component và Deployment dùng Graphviz để dàn trang; nếu máy chưa có Graphviz, thêm dòng `!pragma layout smetana` ngay sau `@startuml` để dùng bộ dàn trang có sẵn trong PlantUML.

```powershell
Set-Location docs\diagram
java -jar plantuml.jar -charset UTF-8 -tpng *.puml
```
