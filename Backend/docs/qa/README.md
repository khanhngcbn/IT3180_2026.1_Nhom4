# Tài liệu kiểm thử BlueMoon – Sprint 1

Bộ tài liệu kiểm thử cho bản ver1 (Sprint 1) của hệ thống quản lý chung cư BlueMoon: 12 User Story US01, US02, US03, US05, US06, US07, US08, US12, US15, US21, US22, US23. Mọi kết quả trong thư mục này lấy từ lần chạy kiểm thử ngày 26/11/2026 trên mã nguồn nhánh `main` (sau commit `4ffb52e`).

## Phân công

| Thành viên | Vai trò trong kiểm thử | Trách nhiệm |
|---|---|---|
| Nguyễn Hoàng Giang | Kiểm thử | Thiết kế test case, chạy kiểm thử, ghi nhận lỗi, lập báo cáo |
| Nguyễn Đình Nam Khánh | Phát triển | Sửa lỗi thuộc US05, US08, US15, US22 và giao diện đăng nhập |
| Đặng Thiệu Minh | Phát triển | Sửa lỗi thuộc US01, US02, US03, US06, US07, US12, US21, US23 |
| Nguyễn Đình Nam Khánh | Duyệt | Duyệt kế hoạch, kết quả kiểm thử và quyết định nghiệm thu |

Việc chia lỗi cho hai người phát triển bám theo người phụ trách từng User Story trong timeline dự án.

## Danh mục

| Tài liệu | Số lượng | Tệp |
|---|:---:|---|
| Kế hoạch kiểm thử | 1 | [ke-hoach-kiem-thu.md](ke-hoach-kiem-thu.md) |
| Test case chức năng | 30 | [test-case-chuc-nang.md](test-case-chuc-nang.md) (`CN-01`…`CN-30`) |
| Test case giao diện | 24 | [test-case-giao-dien.md](test-case-giao-dien.md) (`GD-01`…`GD-24`) |
| Test case tích hợp | 8 | [test-case-tich-hop.md](test-case-tich-hop.md) (`TH-01`…`TH-08`) |
| Kịch bản kiểm thử | 7 | [kich-ban-kiem-thu.md](kich-ban-kiem-thu.md) (`KB-01`…`KB-07`) |
| Bộ dữ liệu kiểm thử | 5 | [du-lieu-kiem-thu.md](du-lieu-kiem-thu.md) (`DL-01`…`DL-05`) |
| Báo cáo kiểm thử | 1 | [bao-cao-kiem-thu.md](bao-cao-kiem-thu.md) |
| Báo cáo thực thi | 1 | [ket-qua-thuc-thi.md](ket-qua-thuc-thi.md) |
| Báo cáo lỗi | 1 | [bao-cao-loi.md](bao-cao-loi.md) (13 lỗi `LOI-01`…`LOI-13`) |
| Bằng chứng | 3 | [bang-chung/](bang-chung/) (`BC-01`…`BC-03`) |
| Checklist hồi quy | 1 | [checklist-hoi-quy.md](checklist-hoi-quy.md) |

Script kiểm thử API tự động: [tu-dong/kiem_thu_api.py](tu-dong/kiem_thu_api.py). Script này chạy lại được toàn bộ 30 test case chức năng và 8 test case tích hợp.

## Kết quả nhanh (26/11/2026)

| Nhóm | Số case | Đạt | Không đạt |
|---|:---:|:---:|:---:|
| Chức năng (API) | 30 | 29 | 1 |
| Tích hợp (API) | 8 | 4 | 4 |
| Giao diện (trình duyệt) | 24 | 20 | 4 |
| **Tổng** | **62** | **53** | **9** |

Ngoài ra 9/9 test đơn vị của backend (`./mvnw test`) đều đạt. Chi tiết, đánh giá và đề xuất nằm trong [báo cáo kiểm thử](bao-cao-kiem-thu.md).
