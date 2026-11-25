# Sơ đồ UML BlueMoon

Sơ đồ chia theo loại trong từng thư mục. Mỗi hình PNG có tệp PlantUML đi kèm.

- `use-case/`: chức năng và vai trò.
- `activity/`: đăng ký tài khoản, tạo khoản thu điện, nước.
- `sequence/`: đăng nhập, quên mật khẩu.
- `class/`: lớp dữ liệu, kiểu liệt kê và quan hệ chính.
- `component/` và `deployment/`: thành phần ứng dụng và cấu hình triển khai.
- `erd/`: sơ đồ quan hệ thực thể của database PostgreSQL (11 bảng), có thêm bản SVG. Cột và kiểu dữ liệu lấy từ DDL mà Hibernate sinh ra. Nét liền là khóa ngoại có trong database, nét đứt (`FK*`) là tham chiếu do ứng dụng kiểm soát.

`style.iuml` giữ màu và phông chữ dùng chung cho mọi sơ đồ.
