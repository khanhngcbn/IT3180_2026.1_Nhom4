# BlueMoon

Ứng dụng web quản lý cư dân, căn hộ và thu phí chung cư cho ban quản lý, kế toán và cư dân. Backend dùng Spring Boot (thư mục `Backend`), giao diện dùng React và Chakra UI (thư mục `Frontend`).

## Chức năng

- Cư dân tự đăng ký tài khoản và xác minh email bằng OTP; đăng nhập bằng JWT, đổi mật khẩu, quên mật khẩu thì đặt lại bằng OTP gửi tới email đã đăng ký.
- Quản trị tài khoản: thêm, sửa, đổi vai trò, kích hoạt hoặc vô hiệu hóa từng tài khoản hoặc hàng loạt, xóa và xuất Excel.
- Quản lý căn hộ (số căn hộ, số phòng, tầng, diện tích, loại, trạng thái), cập nhật trạng thái hàng loạt, lọc theo nhiều tiêu chí và xem cư dân trong từng căn hộ; hồ sơ cư dân gắn với một hoặc nhiều căn hộ.
- Thiết lập đơn giá: phí căn hộ và phí dịch vụ theo m², điện theo kWh, nước theo m³, gửi xe theo tháng và theo giờ.
- Tạo, sửa, xóa và tìm khoản thu theo căn hộ; tạo khoản thu điện, nước hàng loạt từ lượng tiêu thụ; xác nhận thanh toán tiền mặt. Cư dân chỉ xem được khoản thu của căn hộ mình.
- Quản lý loại và đợt đóng góp (mục tiêu số tiền, thời gian), đóng, hủy, mở lại đợt, tạo khoản đóng góp cho toàn bộ căn hộ và xuất Excel; cư dân xem và đăng ký đóng góp.

## Cài đặt và chạy

Cần **JDK 17**, **Node.js 18** trở lên kèm npm, Git, Docker Desktop đang chạy và một tài khoản Gmail có **App Password** để gửi OTP. Backend dùng Maven Wrapper, không cần cài Maven riêng. Lần chạy đầu cần mạng để tải thư viện.

Chạy backend trong một cửa sổ PowerShell. Các biến môi trường phải được đặt trong cùng cửa sổ trước khi chạy Docker Compose và backend (giải thích ở mục [Cấu hình kết nối](#cấu-hình-kết-nối)):

```powershell
git clone https://github.com/khanhngcbn/IT3180_2026.1_Nhom4.git
Set-Location IT3180_2026.1_Nhom4\Backend
$env:DB_PASSWORD = 'mat-khau-cua-ban'
$env:MAIL_USERNAME = 'ban@gmail.com'
$env:MAIL_PASSWORD = 'app-password-gmail'
$env:JWT_SECRET = [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }) -as [byte[]])
docker compose up -d
docker compose ps
```

Chờ dịch vụ `db` (PostgreSQL 16) hiện trạng thái `Up` trong `docker compose ps`, rồi chạy backend tại `http://localhost:9090`:

```powershell
.\mvnw.cmd spring-boot:run
```

Docker Compose chỉ chạy PostgreSQL; backend chạy bằng Java trên máy.

Chạy giao diện trong một cửa sổ PowerShell khác, từ thư mục gốc của repo:

```powershell
Set-Location Frontend
Set-Content .env 'REACT_APP_API_BASE_URL=http://localhost:9090'
npm install --legacy-peer-deps --ignore-scripts
npm start
```

Giao diện mở tại `http://localhost:3000`. `--legacy-peer-deps` tránh lỗi xung đột phiên bản thư viện; `--ignore-scripts` bỏ qua bước `preinstall` (`npx npm-force-resolutions`).

Lần chạy đầu, backend tự tạo bảng và tài khoản quản trị dưới đây; đổi mật khẩu ngay sau lần đăng nhập đầu.

| Vai trò | Tên đăng nhập | Email | Số điện thoại | Mật khẩu ban đầu |
|---|---|---|---|---|
| Ban quản lý (`ADMIN`) | `admin` | `admin@gmail.com` | `0123456789` | `1234567890` |

Không có tài khoản cư dân mẫu. Cư dân tự đăng ký ở màn hình **Sign Up** (liên kết **Create an Account** ở màn hình đăng nhập) rồi nhập OTP gửi về email, hoặc Ban quản lý thêm tài khoản ở màn hình **Resident Management**. Khi đăng ký cần tên đăng nhập chưa dùng, họ tên, tuổi (1–120), số điện thoại 10 chữ số và email chưa dùng; số căn hộ không bắt buộc, nhưng nếu nhập thì phải có trong hệ thống. Mật khẩu dài 8–16 ký tự, có chữ hoa, chữ thường, chữ số, ký tự đặc biệt và không chứa khoảng trắng. Phiên đăng ký hết hạn sau 5 phút nên cần nhập OTP trong thời gian này.

Màn hình đăng nhập nhận **tên đăng nhập** và mật khẩu (không đăng nhập bằng email hay số điện thoại). Ban quản lý được chuyển tới trang quản trị, cư dân tới trang cá nhân. Phiên đăng nhập (JWT) hết hạn sau 1 giờ. Người dùng có thể chọn **Forgot password?** ở màn hình đăng nhập để nhập tên đăng nhập; OTP được gửi tới email đã đăng ký của tài khoản đó, và ở bước đặt lại phải nhập đúng email này. OTP có hiệu lực 5 phút, chỉ dùng được một lần và bị hủy sau 3 lần nhập sai; mỗi email được yêu cầu tối đa 3 OTP trong 15 phút. Khi đã đăng nhập, thao tác **Change password** ở trang cá nhân yêu cầu mật khẩu hiện tại.

## Khởi tạo lại dữ liệu

Backend dùng Hibernate với `ddl-auto=update`: mỗi lần khởi động tự tạo bảng và thêm cột mới nếu thiếu, nhưng không xóa hay đổi tên cột cũ. Khi khởi động, backend tạo tài khoản `admin` nếu chưa có, và tạo 50 căn hộ mẫu nếu bảng căn hộ đang trống: `A0001`–`A0050`, 10 tầng, mỗi tầng 5 căn; tầng 1 là `KIOT`, các tầng còn lại là `STANDARD`; tất cả ở trạng thái trống (`VACANT`) với diện tích ngẫu nhiên.

Dữ liệu PostgreSQL nằm trong volume Docker `bluemoon_pgdata`. Để làm lại từ database trống, sao lưu dữ liệu cần giữ rồi chạy trong thư mục `Backend`, với `DB_PASSWORD` đã đặt:

```powershell
docker compose down -v
docker compose up -d
```

Lệnh `down -v` xóa toàn bộ dữ liệu trong volume. Lần chạy backend tiếp theo sẽ tạo lại bảng, tài khoản `admin` và 50 căn hộ mẫu.

## Cấu hình kết nối

Backend đọc cấu hình từ biến môi trường, mặc định trỏ tới PostgreSQL trong Docker tại `localhost:5432`, database `chungcu_db`.

| Biến | Bắt buộc | Mặc định | Ý nghĩa |
|---|:---:|---|---|
| `DB_URL` | | `jdbc:postgresql://localhost:5432/chungcu_db` | Địa chỉ database |
| `DB_USERNAME` | | `postgres` | Tài khoản database |
| `DB_PASSWORD` | ✅ | – | Mật khẩu database; Docker Compose cũng dùng biến này để tạo PostgreSQL |
| `MAIL_USERNAME` | ✅ | – | Địa chỉ Gmail gửi OTP |
| `MAIL_PASSWORD` | ✅ | – | App Password của Gmail (không dùng mật khẩu Gmail thường) |
| `JWT_SECRET` | ✅ | – | Chuỗi Base64 dài ít nhất 32 byte, dùng để ký JWT |

```powershell
$env:DB_URL = 'jdbc:postgresql://localhost:5432/chungcu_db'
$env:DB_USERNAME = 'postgres'
$env:DB_PASSWORD = 'mat-khau-cua-ban'
```

Spring Boot không tự đọc file `.env`. File mẫu `Backend/.env.example` liệt kê đủ các biến; có thể giữ cấu hình thật trong `Backend/src/main/resources/application-local.properties` (đã được `.gitignore`) và chạy `.\mvnw.cmd spring-boot:run "-Dspring-boot.run.profiles=local"`. Đổi `JWT_SECRET` làm mọi phiên đăng nhập hiện có mất hiệu lực.

Để dùng PostgreSQL riêng thay cho Docker, tạo database `chungcu_db` trước, sau đó đặt `DB_URL`, `DB_USERNAME`, `DB_PASSWORD` trong cùng cửa sổ PowerShell chạy backend. Backend chạy ở cổng `9090` (`server.port` trong `application.properties`).

Giao diện đọc địa chỉ backend từ `REACT_APP_API_BASE_URL` trong `Frontend/.env`. Biến này chỉ được đọc khi khởi động, nên sau khi sửa cần dừng và chạy lại `npm start`; khi build bản chạy thật (`npm run build`) cũng phải đặt đúng biến này. Backend chỉ nhận request từ các địa chỉ có trong danh sách CORS ở `HomeSecurity.corsConfigurationSource()` (đã có `http://localhost:3000`); nếu chạy giao diện ở địa chỉ hoặc cổng khác, thêm địa chỉ đó vào danh sách rồi chạy lại backend.
