"""Bộ kiểm thử API tự động cho BlueMoon Sprint 1.

Chạy 30 test case chức năng (CN-01..CN-30) và 8 test case tích hợp (TH-01..TH-08)
được mô tả trong docs/qa. Kết quả in ra màn hình và ghi thành JSON.

Điều kiện: backend vừa khởi động với database trống (tài khoản mẫu và 50 căn hộ mẫu
được tạo tự động), email OTP gửi tới SMTP giả scripts/smtp_stub.py.

    python scripts/smtp_stub.py <mail.log>
    # chạy backend với SPRING_MAIL_HOST=127.0.0.1, SPRING_MAIL_PORT=2525,
    # SPRING_MAIL_PROPERTIES_MAIL_SMTP_STARTTLS_ENABLE=false
    python docs/qa/tu-dong/kiem_thu_api.py <mail.log> <ket-qua.json> [http://localhost:9090]
"""
import base64
import datetime
import json
import re
import sys
import time
import urllib.error
import urllib.request

MAIL_LOG = sys.argv[1]
OUTPUT = sys.argv[2]
BASE = sys.argv[3] if len(sys.argv) > 3 else "http://localhost:9090"

TODAY = datetime.date.today()
IN_30_DAYS = (TODAY + datetime.timedelta(days=30)).isoformat()
YESTERDAY = (TODAY - datetime.timedelta(days=1)).isoformat()

ADMIN = ("admin", "1234567890")
KETOAN = ("ketoan", "Ketoan@123")
CUDAN01 = ("cudan01", "Cudan01@123")
CUDAN02 = ("cudan02", "Cudan02@123")
CUDANKHOA = ("cudankhoa", "Cudankhoa@123")


# ---------------------------------------------------------------- HTTP helpers
class Session:
    """Giữ cookie phiên (JSESSIONID) cho luồng đăng ký, kể cả khi cookie có cờ Secure."""

    def __init__(self):
        self.cookie = None


def http(method, path, body=None, token=None, session=None, raw=False):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    if session is not None and session.cookie:
        headers["Cookie"] = session.cookie
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        status, payload, resp_headers = resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as err:
        status, payload, resp_headers = err.code, err.read(), err.headers
    if session is not None:
        for set_cookie in resp_headers.get_all("Set-Cookie") or []:
            session.cookie = set_cookie.split(";")[0]
    if raw:
        return status, payload
    text = payload.decode("utf-8", "replace")
    try:
        return status, json.loads(text)
    except ValueError:
        return status, text


def login(account):
    status, body = http("POST", "/api/auth/login", {"name": account[0], "password": account[1]})
    return body if status == 200 and isinstance(body, str) and body.count(".") == 2 else None


def jwt_role(token):
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload)).get("role")


def latest_otp(email, wait=1.5):
    """Lấy mã OTP mới nhất gửi tới email từ log của SMTP giả."""
    time.sleep(wait)
    with open(MAIL_LOG, encoding="utf-8", errors="replace") as f:
        messages = f.read().split("=====END=====")
    for message in reversed(messages):
        if email.lower() in message.lower():
            body = message.split("\n\n", 1)[-1]
            codes = re.findall(r"\b(\d{6})\b", body)
            if codes:
                return codes[-1]
    return None


def wrong_otp(otp):
    return "000000" if otp != "000000" else "111111"


def users_by_name(admin_token):
    return {u["name"]: u for u in http("GET", "/api/admin/users", token=admin_token)[1]}


def apartments_by_number(admin_token):
    return {a["apartmentNumber"]: a for a in http("GET", "/api/admin/apartment-list", token=admin_token)[1]}


def short(value, limit=160):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return text if len(text) <= limit else text[:limit] + "..."


def register(username, email, password="Dangky@123", apartments=None, phone="0912000001"):
    session = Session()
    form = {"name": username, "password": password, "fullName": "Cư dân kiểm thử", "age": 30,
            "phone": phone, "email": email, "apartmentNumbers": apartments or []}
    status, body = http("POST", "/api/auth/register", form, session=session)
    return session, status, body


# ---------------------------------------------------------------- test registry
CASES = []


def case(case_id, title):
    def wrap(fn):
        CASES.append((case_id, title, fn))
        return fn
    return wrap


STATE = {}


def admin():
    if "admin" not in STATE:
        STATE["admin"] = login(ADMIN)
    return STATE["admin"]


# ---------------------------------------------------------------- functional
@case("CN-01", "Đăng ký tài khoản hợp lệ và xác minh bằng OTP")
def cn01():
    session, status, body = register("qa_cn01", "qa.cn01@bluemoon.test")
    if status != 200:
        return False, f"register {status} {short(body)}"
    http("GET", "/api/auth/send-otp", session=session)
    otp = latest_otp("qa.cn01@bluemoon.test")
    status, body = http("POST", "/api/auth/verify-otp", {"otp": otp}, session=session)
    token = login(("qa_cn01", "Dangky@123"))
    return status == 200 and token is not None, f"verify {status} {short(body)}; đăng nhập {'được' if token else 'không được'}"


@case("CN-02", "Đăng ký với dữ liệu sai định dạng bị từ chối")
def cn02():
    _, status, body = register("qa_cn02", "qa.cn02@bluemoon.test", password="abc12345", phone="091200")
    errors = body.get("errors", {}) if isinstance(body, dict) else {}
    ok = status == 400 and "password" in errors and "phone" in errors
    return ok, f"{status} lỗi ở các trường {sorted(errors)}"


@case("CN-03", "OTP sai bị từ chối, gửi lại OTP rồi nhập mã mới thì thành công")
def cn03():
    email = "qa.cn03@bluemoon.test"
    session, status, _ = register("qa_cn03", email, phone="0912000003")
    http("GET", "/api/auth/send-otp", session=session)
    first = latest_otp(email)
    s_wrong, b_wrong = http("POST", "/api/auth/verify-otp", {"otp": wrong_otp(first)}, session=session)
    s_resend, _ = http("POST", "/api/auth/resend-otp", session=session)
    second = latest_otp(email)
    s_ok, _ = http("POST", "/api/auth/verify-otp", {"otp": second}, session=session)
    ok = s_wrong == 400 and s_resend == 200 and s_ok == 200 and login(("qa_cn03", "Dangky@123"))
    return bool(ok), f"OTP sai {s_wrong} ({short(b_wrong, 60)}), gửi lại {s_resend}, OTP mới {s_ok}"


@case("CN-04", "Đăng nhập đúng nhận JWT có vai trò tương ứng")
def cn04():
    t_admin, t_res = login(ADMIN), login(CUDAN01)
    roles = (jwt_role(t_admin) if t_admin else None, jwt_role(t_res) if t_res else None)
    return roles == ("ROLE_ADMIN", "ROLE_USER"), f"vai trò trong JWT: admin={roles[0]}, cudan01={roles[1]}"


@case("CN-05", "Sai mật khẩu hoặc tài khoản bị khóa thì không đăng nhập được")
def cn05():
    s_wrong, _ = http("POST", "/api/auth/login", {"name": "cudan01", "password": "SaiMatKhau@1"})
    s_locked, _ = http("POST", "/api/auth/login", {"name": CUDANKHOA[0], "password": CUDANKHOA[1]})
    return s_wrong == 401 and s_locked == 401, f"sai mật khẩu {s_wrong}, tài khoản bị khóa {s_locked}"


@case("CN-06", "Đổi mật khẩu phải nhập đúng mật khẩu cũ")
def cn06():
    token = login(("qa_cn01", "Dangky@123"))
    uid = http("GET", "/api/user/change-password", token=token)[1].get("userId")
    s_bad, b_bad = http("POST", "/api/user/change-password",
                        {"userId": str(uid), "oldPassword": "KhongDung@1", "newPassword": "MoiMoi@123"}, token)
    s_ok, _ = http("POST", "/api/user/change-password",
                   {"userId": str(uid), "oldPassword": "Dangky@123", "newPassword": "MoiMoi@123"}, token)
    new_login, old_login = login(("qa_cn01", "MoiMoi@123")), login(("qa_cn01", "Dangky@123"))
    ok = s_bad == 400 and s_ok == 200 and new_login and not old_login
    return bool(ok), f"mật khẩu cũ sai {s_bad} ({short(b_bad, 50)}), đúng {s_ok}; mật khẩu mới đăng nhập {'được' if new_login else 'không'}"


@case("CN-07", "Quên mật khẩu: đặt lại bằng OTP gửi tới email đã đăng ký")
def cn07():
    s_send, _ = http("POST", "/api/auth/forgot-password", {"username": "qa_cn03"})
    otp = latest_otp("qa.cn03@bluemoon.test")
    s_reset, b_reset = http("POST", "/api/auth/reset-password", {"username": "qa_cn03", "email": "qa.cn03@bluemoon.test",
                                                                "otp": otp, "newPassword": "DatLai@123"})
    new_login, old_login = login(("qa_cn03", "DatLai@123")), login(("qa_cn03", "Dangky@123"))
    ok = s_send == 200 and s_reset == 200 and new_login and not old_login
    return bool(ok), f"gửi OTP {s_send}, đặt lại {s_reset} {short(b_reset, 60)}"


@case("CN-08", "Không dùng được OTP của email khác để đặt lại mật khẩu")
def cn08():
    email = "qa.cn08@bluemoon.test"
    session, _, _ = register("qa_cn08", email, phone="0912000008")
    http("GET", "/api/auth/send-otp", session=session)
    attacker_otp = latest_otp(email)
    status, body = http("POST", "/api/auth/reset-password", {"username": "cudan02", "email": email,
                                                            "otp": attacker_otp, "newPassword": "ChiemQuyen@1"})
    still_old = login(CUDAN02) is not None
    return status == 400 and still_old, f"{status} {short(body, 60)}; cudan02 vẫn dùng mật khẩu cũ: {still_old}"


@case("CN-09", "Nhập sai OTP 3 lần thì OTP bị hủy")
def cn09():
    http("POST", "/api/auth/forgot-password", {"username": "cudan02"})
    otp = latest_otp("cudan02@bluemoon.test")
    codes = []
    for _ in range(3):
        codes.append(http("POST", "/api/auth/reset-password", {"username": "cudan02", "email": "cudan02@bluemoon.test",
                                                               "otp": wrong_otp(otp), "newPassword": "Thu@12345"})[0])
    s_after, _ = http("POST", "/api/auth/reset-password", {"username": "cudan02", "email": "cudan02@bluemoon.test",
                                                           "otp": otp, "newPassword": "Thu@12345"})
    return codes == [400, 400, 400] and s_after == 400 and login(CUDAN02) is not None, \
        f"3 lần sai {codes}, OTP đúng sau đó {s_after}"


@case("CN-10", "Ban quản lý đổi vai trò tài khoản")
def cn10():
    uid = users_by_name(admin())["qa_cn01"]["id"]
    status, body = http("POST", f"/api/admin/users/edit/{uid}", {"fullName": "Cư dân kiểm thử", "age": 30,
                        "phone": "0912000001", "role": "ADMIN", "apartmentNumbers": [], "status": "THUONGTRU"}, admin())
    token = login(("qa_cn01", "MoiMoi@123"))
    role = jwt_role(token) if token else None
    http("POST", f"/api/admin/users/edit/{uid}", {"fullName": "Cư dân kiểm thử", "age": 30, "phone": "0912000001",
         "role": "USER", "apartmentNumbers": [], "status": "THUONGTRU"}, admin())
    return status == 200 and role == "ROLE_ADMIN", f"{status} {short(body, 40)}; vai trò sau khi đổi: {role}"


@case("CN-11", "Vô hiệu hóa và kích hoạt lại một tài khoản")
def cn11():
    uid = users_by_name(admin())["qa_cn03"]["id"]
    s_off, _ = http("POST", f"/api/admin/users/deactivate/{uid}", token=admin())
    locked = login(("qa_cn03", "DatLai@123")) is None
    s_on, _ = http("POST", f"/api/admin/users/activate/{uid}", token=admin())
    back = login(("qa_cn03", "DatLai@123")) is not None
    return s_off == 200 and locked and s_on == 200 and back, f"khóa {s_off} (đăng nhập bị chặn: {locked}), mở {s_on} (đăng nhập lại: {back})"


@case("CN-12", "Vô hiệu hóa hàng loạt, bỏ qua tài khoản admin")
def cn12():
    users = users_by_name(admin())
    ids = [users["qa_cn01"]["id"], users["qa_cn03"]["id"], users["admin"]["id"]]
    status, body = http("POST", "/api/admin/users/batch/deactivate", {"ids": ids}, admin())
    locked = [login(("qa_cn01", "MoiMoi@123")) is None, login(("qa_cn03", "DatLai@123")) is None]
    admin_ok = login(ADMIN) is not None
    http("POST", "/api/admin/users/batch/activate", {"ids": ids[:2]}, admin())
    ok = status == 200 and body.get("deactivatedCount") == 2 and body.get("failedIds") == [ids[2]] and all(locked) and admin_ok
    return ok, f"{status} {short(body, 90)}; 2 tài khoản bị khóa: {all(locked)}; admin vẫn đăng nhập: {admin_ok}"


@case("CN-13", "Cư dân và người chưa đăng nhập không vào được API quản trị")
def cn13():
    s_res, _ = http("GET", "/api/admin/users", token=login(CUDAN01))
    s_anon, _ = http("GET", "/api/admin/users")
    s_fee, _ = http("GET", "/api/fee-units", token=login(CUDAN01))
    return s_res == 403 and s_anon == 403 and s_fee == 403, f"cư dân {s_res}, không token {s_anon}, cư dân xem đơn giá {s_fee}"


@case("CN-14", "Thêm hồ sơ cư dân và gắn với căn hộ")
def cn14():
    status, body = http("POST", "/api/admin/users/add", {"name": "qa_cn14", "password": "CuDan@1234", "role": "USER",
                        "fullName": "Hộ thử nghiệm", "age": 40, "phone": "0912000014", "email": "qa.cn14@bluemoon.test",
                        "apartmentNumbers": ["A0031"], "status": "THUONGTRU"}, admin())
    user = users_by_name(admin()).get("qa_cn14", {})
    apt = apartments_by_number(admin())["A0031"]
    ok = status == 200 and "A0031" in (user.get("apartmentNumbers") or []) and user.get("phone") == "0912000014"
    return ok, f"{status} {short(body, 40)}; hồ sơ có căn hộ {user.get('apartmentNumbers')}; căn hộ A0031 có {len(apt.get('residentIds') or [])} cư dân"


@case("CN-15", "Thêm cư dân với dữ liệu sai bị từ chối")
def cn15():
    s_apt, b_apt = http("POST", "/api/admin/users/add", {"name": "qa_cn15a", "password": "CuDan@1234", "role": "USER",
                        "fullName": "Sai căn hộ", "email": "qa.cn15a@bluemoon.test", "apartmentNumbers": ["Z9999"],
                        "status": "THUONGTRU"}, admin())
    s_pw, b_pw = http("POST", "/api/admin/users/add", {"name": "qa_cn15b", "password": "yeu", "role": "USER",
                      "fullName": "Mật khẩu yếu", "email": "qa.cn15b@bluemoon.test", "apartmentNumbers": [],
                      "status": "THUONGTRU"}, admin())
    created = {"qa_cn15a", "qa_cn15b"} & set(users_by_name(admin()))
    return s_apt == 400 and s_pw == 400 and not created, f"căn hộ sai {s_apt} {short(b_apt, 60)}; mật khẩu yếu {s_pw}"


@case("CN-16", "Thêm căn hộ mới với đủ thuộc tính")
def cn16():
    status, body = http("POST", "/api/admin/apartment-list/add-apartment", {"apartmentNumber": "B0101", "roomNumber": "2",
                        "floor": 11, "area": 68.5, "status": "OCCUPIED", "type": "STANDARD"}, admin())
    apt = apartments_by_number(admin()).get("B0101", {})
    got = (apt.get("floor"), apt.get("area"), apt.get("type"), apt.get("status"))
    s_dup, b_dup = http("POST", "/api/admin/apartment-list/add-apartment", {"apartmentNumber": "B0101", "roomNumber": "2",
                        "floor": 11, "area": 68.5, "status": "VACANT", "type": "STANDARD"}, admin())
    ok = status == 201 and got == (11, 68.5, "STANDARD", "OCCUPIED") and s_dup == 400
    return ok, f"tạo {status}; lưu được (tầng, diện tích, loại, trạng thái) = {got}; thêm trùng số căn hộ {s_dup} {short(b_dup, 50)}"


@case("CN-17", "Cập nhật trạng thái nhiều căn hộ cùng lúc")
def cn17():
    apts = apartments_by_number(admin())
    ids = [apts["A0041"]["id"], apts["A0042"]["id"]]
    s_ok, _ = http("POST", "/api/apartments/batch-update-status", {"ids": ids, "status": "OCCUPIED"}, admin())
    after = apartments_by_number(admin())
    s_bad, _ = http("POST", "/api/apartments/batch-update-status", {"ids": ids, "status": "KHONGCO"}, admin())
    ok = s_ok == 200 and after["A0041"]["status"] == after["A0042"]["status"] == "OCCUPIED" and s_bad == 400
    return ok, f"cập nhật {s_ok} -> {after['A0041']['status']}/{after['A0042']['status']}; trạng thái không hợp lệ {s_bad}"


@case("CN-18", "Lọc căn hộ theo tầng, trạng thái và loại")
def cn18():
    status, body = http("GET", "/api/apartments/filter?floors=1&type=KIOT&status=VACANT", token=admin())
    numbers = sorted(a["apartmentNumber"] for a in body) if status == 200 else []
    expected = ["A0001", "A0002", "A0003", "A0004", "A0005"]
    return numbers == expected, f"{status} kết quả {numbers}"


@case("CN-19", "Xem danh sách cư dân trong một căn hộ")
def cn19():
    apt_id = apartments_by_number(admin())["A0023"]["id"]
    status, body = http("GET", f"/api/admin/apartment-list/residents/{apt_id}", token=admin())
    names = sorted(r.get("fullName") for r in body) if status == 200 else []
    return status == 200 and names == ["Nguyễn Thị C"], f"{status} cư dân của A0023: {names}"


@case("CN-20", "Lưu bảng đơn giá, gồm phí gửi xe theo tháng và theo giờ")
def cn20():
    fee = http("GET", "/api/fee-units", token=admin())[1]
    fee.update({"electricityFeePerKWh": 3800, "waterFeePerM3": 18000, "parkingFeePerMonth": 120000, "parkingFeePerHour": 5000})
    status, body = http("POST", "/api/fee-units", fee, admin())
    saved = http("GET", "/api/fee-units", token=admin())[1]
    got = (saved.get("electricityFeePerKWh"), saved.get("waterFeePerM3"), saved.get("parkingFeePerMonth"), saved.get("parkingFeePerHour"))
    return status == 200 and got == (3800, 18000, 120000, 5000), f"{status}; giá sau khi lưu (điện, nước, xe tháng, xe giờ) = {got}"


@case("CN-21", "Đơn giá âm bị từ chối và không ghi đè giá cũ")
def cn21():
    fee = http("GET", "/api/fee-units", token=admin())[1]
    status, body = http("POST", "/api/fee-units", {**fee, "parkingFeePerHour": -1000}, admin())
    after = http("GET", "/api/fee-units", token=admin())[1]
    return status == 400 and after == fee, f"{status} {short(body, 60)}; giá giữ nguyên: {after == fee}"


@case("CN-22", "Tạo khoản thu hợp lệ, trạng thái mặc định chưa thanh toán, tìm được theo căn hộ")
def cn22():
    bill = {"apartmentNumber": "A0012", "billType": "SERVICE_COST", "description": "QA phí dịch vụ tháng 11",
            "amount": 350000, "dueDate": TODAY.isoformat()}
    status, body = http("POST", "/api/admin/bills", bill, admin())
    s_find, found = http("GET", "/api/bills/filter?apartmentNumber=A0012&description=QA", token=admin())
    match = [b for b in found if b["description"] == bill["description"]] if s_find == 200 else []
    STATE["bill_a0012"] = match[0]["id"] if match else None
    ok = status == 200 and len(match) == 1 and match[0]["status"] == "UNPAID"
    return ok, f"{status} {short(body, 40)}; tìm theo căn hộ thấy {len(match)} khoản, trạng thái {match[0]['status'] if match else None}"


@case("CN-23", "Khoản thu sai dữ liệu báo lỗi theo từng trường")
def cn23():
    s1, b1 = http("POST", "/api/admin/bills", {"apartmentNumber": "1", "billType": "WATER", "description": "x",
                  "amount": 15000, "dueDate": TODAY.isoformat()}, admin())
    s2, b2 = http("POST", "/api/admin/bills", {"apartmentNumber": "A0012", "billType": "WATER", "description": "x",
                  "amount": 0, "dueDate": YESTERDAY}, admin())
    keys = (sorted(b1) if isinstance(b1, dict) else b1, sorted(b2) if isinstance(b2, dict) else b2)
    ok = s1 == 400 and keys[0] == ["apartmentNumber"] and s2 == 400 and keys[1] == ["amount", "dueDate"]
    return ok, f"căn hộ không tồn tại {s1} {keys[0]}; số tiền 0 + hạn hôm qua {s2} {keys[1]}"


@case("CN-24", "Sửa rồi xóa một khoản thu")
def cn24():
    bill = {"apartmentNumber": "A0024", "billType": "OTHER", "description": "QA khoản tạm", "amount": 50000, "dueDate": IN_30_DAYS}
    http("POST", "/api/admin/bills", bill, admin())
    bid = [b for b in http("GET", "/api/admin/bills", token=admin())[1] if b["description"] == "QA khoản tạm"][0]["id"]
    s_edit, _ = http("PUT", f"/api/admin/bills/edit/{bid}", {**bill, "amount": 65000}, admin())
    amount = http("GET", f"/api/admin/bills/{bid}", token=admin())[1].get("amount")
    s_del, _ = http("DELETE", f"/api/admin/bills/{bid}", token=admin())
    s_get, _ = http("GET", f"/api/admin/bills/{bid}", token=admin())
    return s_edit == 200 and amount == 65000 and s_del in (200, 204) and s_get == 404, \
        f"sửa {s_edit} (số tiền mới {amount}), xóa {s_del}, xem lại {s_get}"


@case("CN-25", "Tạo khoản thu điện, nước hàng loạt từ lượng tiêu thụ")
def cn25():
    fee = http("GET", "/api/fee-units", token=admin())[1]
    status, body = http("POST", "/api/utility-bills/generate", {"dueDate": IN_30_DAYS, "formData": {
        "electricity_A0012": "120", "water_A0012": "8", "electricity_A0023": "75", "water_A0023": ""}}, admin())
    bills = sorted((b["billType"], b["apartmentNumber"], b["amount"]) for b in body.get("bills", [])) if isinstance(body, dict) else []
    expected = sorted([("ELECTRICITY", "A0012", 120.0 * fee["electricityFeePerKWh"]),
                       ("WATER", "A0012", 8.0 * fee["waterFeePerM3"]),
                       ("ELECTRICITY", "A0023", 75.0 * fee["electricityFeePerKWh"])])
    return status == 200 and bills == expected, f"{status}; tạo {bills}"


@case("CN-26", "Cư dân chỉ thấy khoản thu của căn hộ mình")
def cn26():
    status, body = http("GET", "/api/bills/list", token=login(CUDAN01))
    apts = sorted({b["apartmentNumber"] for b in body}) if status == 200 else []
    return status == 200 and apts == ["A0012"] and len(body) >= 4, f"{status} {len(body) if status == 200 else 0} khoản, căn hộ {apts}"


@case("CN-27", "Cư dân không xem được khoản thu của căn hộ khác")
def cn27():
    other = [b for b in http("GET", "/api/admin/bills", token=admin())[1] if b["apartmentNumber"] == "A0023"][0]["id"]
    status, _ = http("GET", f"/api/bills/{other}", token=login(CUDAN01))
    s_detail, _ = http("GET", "/api/user/apartment-detail?apartmentNumber=A0023", token=login(CUDAN01))
    return status == 403 and s_detail == 403, f"mở khoản thu A0023: {status}; xem chi tiết căn hộ A0023: {s_detail}"


@case("CN-28", "Xác nhận thanh toán tiền mặt, cư dân không có quyền này")
def cn28():
    bid = STATE.get("bill_a0012")
    s_res, _ = http("POST", f"/api/admin/bills/{bid}/confirm-payment", token=login(CUDAN01))
    s_adm, body = http("POST", f"/api/admin/bills/{bid}/confirm-payment", token=admin())
    s_twice, _ = http("POST", f"/api/admin/bills/{bid}/confirm-payment", token=admin())
    status_now = http("GET", f"/api/admin/bills/{bid}", token=admin())[1].get("status")
    return s_res == 403 and s_adm == 200 and status_now == "PAID" and s_twice == 400, \
        f"cư dân {s_res}; ban quản lý {s_adm} -> {status_now}; xác nhận lần hai {s_twice}"


@case("CN-29", "Tạo loại đóng góp và đợt đóng góp có mục tiêu, thời gian")
def cn29():
    s_type, t_body = http("POST", "/api/contribution-types/create", {"name": "QA Quỹ khuyến học", "description": "Kiểm thử"}, admin())
    tid = t_body.get("id") if isinstance(t_body, dict) else None
    drive = {"contributionTypeId": tid, "title": "QA Khuyến học cuối năm", "description": "Kiểm thử",
             "startDate": TODAY.isoformat(), "endDate": IN_30_DAYS, "targetAmount": 20000000}
    s_drive, d_body = http("POST", "/api/contributions/admin/create", drive, admin())
    STATE["drive"] = d_body if isinstance(d_body, int) else (d_body.get("id") if isinstance(d_body, dict) else None)
    listed = [c for c in http("GET", "/api/contributions/admin", token=admin())[1]["contributions"] if c["title"] == drive["title"]]
    ok = s_type == 200 and s_drive == 200 and len(listed) == 1 and listed[0]["targetAmount"] == 20000000
    return ok, f"loại {s_type}, đợt {s_drive}; đợt có trong danh sách: {len(listed) == 1}, trạng thái {listed[0]['status'] if listed else None}"


@case("CN-30", "Đóng, mở lại và hủy đợt đóng góp")
def cn30():
    cid = STATE.get("drive")
    steps = [http("POST", f"/api/contributions/admin/{cid}/{action}", token=admin())[0]
             for action in ("close", "reactivate", "cancel", "reactivate")]
    return steps == [200, 200, 200, 400], f"đóng/mở lại/hủy/mở lại sau khi hủy = {steps}"


# ---------------------------------------------------------------- integration
@case("TH-01", "Cư dân tự đăng ký kèm căn hộ thì được gắn vào căn hộ đó")
def th01():
    email = "qa.th01@bluemoon.test"
    session, _, _ = register("qa_th01", email, apartments=["A0035"], phone="0912000101")
    http("GET", "/api/auth/send-otp", session=session)
    s_verify, _ = http("POST", "/api/auth/verify-otp", {"otp": latest_otp(email)}, session=session)
    apt = apartments_by_number(admin())["A0035"]
    residents = http("GET", f"/api/admin/apartment-list/residents/{apt['id']}", token=admin())[1]
    bills = [b for b in http("GET", "/api/bills/list", token=login(("qa_th01", "Dangky@123")))[1]]
    linked = any(r.get("email") == email for r in residents)
    return s_verify == 200 and linked, (f"xác minh {s_verify}; A0035 có cư dân mới: {linked}, trạng thái căn hộ {apt['status']}, "
                                        f"cư dân thấy {len(bills)} khoản thu")


@case("TH-02", "Gắn cư dân đầu tiên vào căn hộ trống: căn hộ chuyển RENT và sinh 3 khoản phí")
def th02():
    apt = apartments_by_number(admin())["A0031"]
    bills = [b for b in http("GET", "/api/admin/bills", token=admin())[1] if b["apartmentNumber"] == "A0031"]
    return apt["status"] == "RENT" and len(bills) == 3, f"A0031 trạng thái {apt['status']}, {len(bills)} khoản phí: {[b['description'][:22] for b in bills]}"


@case("TH-03", "Đổi đơn giá rồi tạo khoản thu điện: số tiền dùng đơn giá mới")
def th03():
    fee = http("GET", "/api/fee-units", token=admin())[1]
    http("POST", "/api/fee-units", {**fee, "electricityFeePerKWh": 4200}, admin())
    status, body = http("POST", "/api/utility-bills/generate", {"dueDate": IN_30_DAYS, "formData": {"electricity_A0024": "10", "water_A0024": ""}}, admin())
    amount = body["bills"][0]["amount"] if isinstance(body, dict) and body.get("bills") else None
    return status == 200 and amount == 42000.0, f"{status}; 10 kWh × 4200 = {amount}"


@case("TH-04", "Khoản thu mới của A0012 hiện cho cư dân A0012, không hiện cho cư dân khác")
def th04():
    http("POST", "/api/admin/bills", {"apartmentNumber": "A0012", "billType": "OTHER", "description": "QA phí sửa thang máy",
         "amount": 90000, "dueDate": IN_30_DAYS}, admin())
    seen_01 = any(b["description"] == "QA phí sửa thang máy" for b in http("GET", "/api/bills/list", token=login(CUDAN01))[1])
    seen_02 = any(b["description"] == "QA phí sửa thang máy" for b in http("GET", "/api/bills/list", token=login(CUDAN02))[1])
    return seen_01 and not seen_02, f"cudan01 thấy: {seen_01}; cudan02 thấy: {seen_02}"


@case("TH-05", "Ban quản lý xác nhận thanh toán, cư dân thấy trạng thái đã thanh toán")
def th05():
    bid = STATE.get("bill_a0012")
    mine = [b for b in http("GET", "/api/bills/list", token=login(CUDAN01))[1] if b["id"] == bid]
    return bool(mine) and mine[0]["status"] == "PAID", f"cư dân thấy khoản {bid} trạng thái {mine[0]['status'] if mine else None}"


@case("TH-06", "Vô hiệu hóa cư dân gỡ cư dân khỏi căn hộ, kích hoạt lại thì gắn lại")
def th06():
    apt_id = apartments_by_number(admin())["A0031"]["id"]
    uid = users_by_name(admin())["qa_cn14"]["id"]
    http("POST", f"/api/admin/users/deactivate/{uid}", token=admin())
    after_off = len(http("GET", f"/api/admin/apartment-list/residents/{apt_id}", token=admin())[1])
    http("POST", f"/api/admin/users/activate/{uid}", token=admin())
    after_on = len(http("GET", f"/api/admin/apartment-list/residents/{apt_id}", token=admin())[1])
    return after_off == 0 and after_on == 1, f"số cư dân A0031 sau khi khóa {after_off}, sau khi mở lại {after_on}"


@case("TH-07", "Tạo khoản đóng góp cho toàn bộ căn hộ: chỉ căn hộ có cư dân nhận khoản")
def th07():
    tid = http("GET", "/api/contribution-types/active", token=admin())[1][0]["id"]
    title = "QA Quỹ vì người nghèo"
    http("POST", "/api/contributions/admin/create", {"contributionTypeId": tid, "title": title, "description": "Kiểm thử",
         "startDate": TODAY.isoformat(), "endDate": IN_30_DAYS, "targetAmount": 5000000}, admin())
    cid = [c for c in http("GET", "/api/contributions/admin", token=admin())[1]["contributions"] if c["title"] == title][0]["id"]
    status, _ = http("POST", f"/api/contributions/admin/create-for-all?contributionId={cid}&amount=100000", token=admin())
    rows = http("GET", f"/api/contributions/admin/{cid}", token=admin())[1].get("residentContributions", [])
    apts = sorted({r["apartmentNumber"] for r in rows})
    occupied = sorted({n for n, a in apartments_by_number(admin()).items() if a.get("residentIds")})
    return status == 200 and apts == occupied, f"{status}; căn hộ nhận khoản {apts}; căn hộ đang có cư dân {occupied}"


@case("TH-08", "Kế toán (ADMIN thường) không khóa, mở, sửa hay xóa được tài khoản super admin")
def th08():
    ketoan = login(KETOAN)
    admin_id = users_by_name(admin())["admin"]["id"]
    demote = {"fullName": "Admin User", "age": 30, "phone": "0123456789", "role": "USER",
              "apartmentNumbers": [], "status": "THUONGTRU"}
    s_batch, b_batch = http("POST", "/api/admin/users/batch/deactivate", {"ids": [admin_id]}, ketoan)
    s_single, _ = http("POST", f"/api/admin/users/deactivate/{admin_id}", token=ketoan)
    s_activate, _ = http("POST", f"/api/admin/users/activate/{admin_id}", token=ketoan)
    s_edit, _ = http("POST", f"/api/admin/users/edit/{admin_id}", demote, ketoan)
    s_delete, _ = http("POST", f"/api/admin/users/delete/{admin_id}", token=ketoan)
    token = login(ADMIN)
    role = jwt_role(token) if token else None
    if role != "ROLE_ADMIN":
        # khôi phục để không ảnh hưởng các lần chạy sau trên cùng database
        http("POST", f"/api/admin/users/activate/{admin_id}", token=ketoan)
        http("POST", f"/api/admin/users/edit/{admin_id}", {**demote, "role": "ADMIN"}, ketoan)
    batch_blocked = isinstance(b_batch, dict) and b_batch.get("deactivatedCount") == 0
    ok = batch_blocked and [s_single, s_activate, s_edit, s_delete] == [403, 403, 403, 403] and role == "ROLE_ADMIN"
    return ok, (f"khóa hàng loạt {s_batch} {short(b_batch, 60)}; khóa/mở/sửa/xóa đơn lẻ = "
                f"{[s_single, s_activate, s_edit, s_delete]}; vai trò của admin sau đó: {role}")


# ---------------------------------------------------------------- runner
def main():
    started = datetime.datetime.now()
    results = []
    for case_id, title, fn in CASES:
        t0 = time.time()
        try:
            passed, actual = fn()
        except Exception as exc:  # lỗi bất ngờ cũng ghi là FAIL kèm thông tin
            passed, actual = False, f"lỗi khi chạy: {type(exc).__name__}: {exc}"
        results.append({"id": case_id, "title": title, "result": "PASS" if passed else "FAIL",
                        "actual": actual, "seconds": round(time.time() - t0, 2)})
        print(f"{'PASS' if passed else 'FAIL'}  {case_id}  {title}\n      -> {actual}")
    summary = {"base_url": BASE, "started_at": started.isoformat(timespec="seconds"),
               "finished_at": datetime.datetime.now().isoformat(timespec="seconds"),
               "total": len(results), "passed": sum(r["result"] == "PASS" for r in results),
               "failed": [r["id"] for r in results if r["result"] == "FAIL"], "results": results}
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\nTổng {summary['total']} | đạt {summary['passed']} | không đạt {len(summary['failed'])} {summary['failed']}")


if __name__ == "__main__":
    main()
