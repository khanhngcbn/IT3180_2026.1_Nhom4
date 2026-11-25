# Kịch bản kiểm thử (7)

Mỗi kịch bản là một luồng nghiệp vụ trọn vẹn của một vai trò, ghép từ các test case chức năng (CN), tích hợp (TH) và giao diện (GD). Kịch bản đạt khi mọi case thành phần đều đạt. Lần 1 chạy trên commit `4ffb52e`, lần 2 (hồi quy) trên commit `5ec2491`.

| Mã | Vai trò | Kịch bản | Các case thành phần | Lần 1 | Lần 2 |
|---|---|---|---|---|---|
| KB-01 | Cư dân mới | Tự đăng ký tài khoản, xác minh OTP, đăng nhập và xem khoản phải thu của căn hộ mình | GD-04, GD-05, CN-01, CN-02, CN-03, TH-01, GD-21, GD-22 | **Không đạt** do TH-01: đăng ký kèm căn hộ nhưng không được gắn vào căn hộ nên không có khoản thu nào | **Đạt** |
| KB-02 | Ban quản lý | Đầu kỳ: thiết lập căn hộ và bảng đơn giá, gồm phí gửi xe | GD-09, GD-10, CN-16, CN-17, GD-17, CN-20, CN-21, GD-18 | **Không đạt** do GD-10 (không có nút thêm căn hộ), CN-16 (trạng thái căn hộ mới bị bỏ qua) và GD-18 (giá âm bị đổi thành 0 rồi lưu) | **Không đạt** do GD-18 |
| KB-03 | Kế toán | Lập khoản thu tháng: điện nước hàng loạt, khoản thu lẻ, tìm, sửa, xóa | GD-19, CN-25, TH-03, GD-13, GD-14, GD-15, CN-22, CN-23, CN-24, GD-16 | **Đạt** | **Đạt** |
| KB-04 | Kế toán + Cư dân | Cư dân nộp tiền mặt, kế toán xác nhận, cư dân thấy đã thanh toán | CN-26, CN-27, CN-28, TH-04, TH-05 | **Đạt** | **Đạt** |
| KB-05 | Người dùng | Quên mật khẩu, đặt lại qua OTP; thử các cách dùng OTP sai | GD-06, CN-07, CN-08, CN-09, CN-05 | **Đạt** | **Đạt** |
| KB-06 | Ban quản lý | Quản trị tài khoản: thêm cư dân, đổi vai trò, khóa/mở đơn lẻ và hàng loạt, phân quyền | GD-11, GD-12, CN-10, CN-11, CN-12, CN-13, CN-14, CN-15, TH-02, TH-06, TH-08, GD-23 | **Không đạt** do TH-08 (kế toán khóa được super admin), TH-06 (khóa tài khoản làm lệch dữ liệu căn hộ) và GD-23 (cư dân mở được trang quản trị) | **Không đạt** do GD-23; ngoài ra phát hiện LOI-14 (kế toán sửa được vai trò super admin) |
| KB-07 | Ban quản lý | Vận động đóng góp: tạo loại và đợt, tạo khoản cho mọi căn hộ có cư dân, đóng/hủy/mở lại đợt | CN-29, CN-30, TH-07, GD-20 | **Không đạt** do TH-07 (khoản đóng góp tạo theo hồ sơ cư dân, lệch với danh sách cư dân của căn hộ) | **Đạt** |

Tổng: lần 1 có 3/7 kịch bản đạt, lần 2 có 5/7 kịch bản đạt. Lỗi gây không đạt được ghi trong [báo cáo lỗi](bao-cao-loi.md).
