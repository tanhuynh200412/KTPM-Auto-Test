"""Tao file resources/testdata/testcases.xlsx (chay lai neu muon reset du lieu test)."""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

OUT = os.path.join(os.path.dirname(__file__), "..", "resources", "testdata", "testcases.xlsx")
FONT = "Arial"
thin = Side(style="thin", color="999999")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HEAD_FILL = PatternFill("solid", fgColor="1F4E78")

PW = "Test@12345"
# (ID, Type, Title, Technique, Email, Password, Expected, Expected Result, Notes)
LOGIN = [
 ("LOGIN_001", "Positive", "Đăng nhập với tài khoản hợp lệ", "EP",
  "${REGISTERED_EMAIL}", "${REGISTERED_PASS}", "success",
  "Đăng nhập thành công, rời khỏi trang /signin", "Dùng tài khoản vừa đăng ký ở SIGNUP_001"),
 ("LOGIN_002", "Negative", "Đúng email, sai mật khẩu", "EP",
  "${REGISTERED_EMAIL}", "WrongPass@999", "fail",
  "Đăng nhập thất bại, ở lại trang /signin, có thông báo lỗi", ""),
 ("LOGIN_003", "Negative", "Email chưa đăng ký", "EP",
  "unregistered_{unique}@test.com", PW, "fail",
  "Đăng nhập thất bại, ở lại trang /signin, có thông báo lỗi", ""),
 ("LOGIN_004", "Validation", "Để trống email", "EP",
  "", PW, "fail", "Báo bắt buộc nhập email, không đăng nhập", ""),
 ("LOGIN_005", "Validation", "Để trống mật khẩu", "EP",
  "${REGISTERED_EMAIL}", "", "fail", "Báo bắt buộc nhập mật khẩu, không đăng nhập", ""),
 ("LOGIN_006", "Validation", "Để trống cả email và mật khẩu", "EP",
  "", "", "fail", "Báo bắt buộc nhập thông tin, không đăng nhập", ""),
 ("LOGIN_007", "Validation", "Email thiếu ký tự @", "EP",
  "invalidemail.com", PW, "fail", "Báo email sai định dạng, không đăng nhập", ""),
 ("LOGIN_008", "Validation", "Email thiếu tên miền sau @", "EP",
  "user@", PW, "fail", "Báo email sai định dạng, không đăng nhập", ""),
 ("LOGIN_009", "Validation", "Email chỉ chứa khoảng trắng", "EP",
  "   ", PW, "fail", "Không đăng nhập, ở lại trang /signin", ""),
 ("LOGIN_010", "Security", "Email chứa chuỗi SQL injection", "Error guessing",
  "' OR '1'='1", "' OR '1'='1", "fail", "Không đăng nhập, ở lại trang /signin", ""),
 ("LOGIN_011", "Negative", "Mật khẩu sai chữ hoa/thường", "EP",
  "${REGISTERED_EMAIL}", "TEST@12345", "fail",
  "Đăng nhập thất bại (mật khẩu phân biệt hoa thường)", "Giả định mật khẩu đăng ký là Test@12345"),
 ("LOGIN_012", "Session", "Đăng xuất sau khi đăng nhập", "State",
  "${REGISTERED_EMAIL}", "${REGISTERED_PASS}", "logout",
  "Đăng xuất thành công, nút Login hiện lại trên header", "Cần khai báo đúng nav.logout trong locators.yaml"),
 ("LOGIN_013", "Negative", "Mật khẩu 7 ký tự (dưới tối thiểu 8)", "BVA",
  "${REGISTERED_EMAIL}", "Abc@123", "fail",
  "Đăng nhập thất bại, ở lại trang /signin", "Giả định tối thiểu 8 ký tự theo thông báo lỗi của hệ thống"),
]

# (ID, Type, Title, Technique, Name, Email, Password, Expected, Expected Result, Notes)
SIGNUP = [
 ("SIGNUP_001", "Positive", "Đăng ký với dữ liệu hợp lệ", "EP",
  "Test User", "user_{unique}@test.com", PW, "success",
  "Đăng ký thành công, rời khỏi trang /signup", "Tài khoản này được dùng cho các test ở sheet Login"),
 ("SIGNUP_002", "Negative", "Đăng ký với email đã tồn tại", "EP",
  "Test User", "user_{unique}@test.com", PW, "fail",
  "Đăng ký thất bại, báo email đã tồn tại", "Cùng email với SIGNUP_001 trong một lần chạy"),
 ("SIGNUP_003", "Validation", "Để trống tên", "EP",
  "", "blankname_{unique}@test.com", PW, "fail",
  "Báo bắt buộc nhập tên, không đăng ký", "Chỉ áp dụng nếu form có ô tên"),
 ("SIGNUP_004", "Validation", "Để trống email", "EP",
  "Test User", "", PW, "fail", "Báo bắt buộc nhập email, không đăng ký", ""),
 ("SIGNUP_005", "Validation", "Để trống mật khẩu", "EP",
  "Test User", "blankpass_{unique}@test.com", "", "fail",
  "Báo bắt buộc nhập mật khẩu, không đăng ký", ""),
 ("SIGNUP_006", "Validation", "Để trống tất cả các ô", "EP",
  "", "", "", "fail", "Báo bắt buộc nhập thông tin, không đăng ký", ""),
 ("SIGNUP_007", "Validation", "Email thiếu ký tự @", "EP",
  "Test User", "invalidemail.com", PW, "fail", "Báo email sai định dạng, không đăng ký", ""),
 ("SIGNUP_008", "Validation", "Email thiếu tên miền sau @", "EP",
  "Test User", "user@", PW, "fail", "Báo email sai định dạng, không đăng ký", ""),
 ("SIGNUP_009", "Validation", "Email chỉ chứa khoảng trắng", "EP",
  "Test User", "   ", PW, "fail", "Không đăng ký, ở lại trang /signup", ""),
 ("SIGNUP_010", "Validation", "Email có khoảng trắng ở giữa", "EP",
  "Test User", "us er_{unique}@test.com", PW, "fail", "Báo email sai định dạng, không đăng ký", ""),
]

# Them cot Confirm Password ({same} = giong Password) vao moi dong Signup (chen sau cot Password)
SIGNUP = [r[:7] + ("{same}",) + r[7:] for r in SIGNUP]
SIGNUP += [
 ("SIGNUP_011", "Validation", "Mật khẩu xác nhận không khớp", "EP",
  "Test User", "mismatch_{unique}@test.com", PW, "Different@999", "fail",
  "Báo mật khẩu xác nhận không khớp, không đăng ký", ""),
 ("SIGNUP_012", "Validation", "Để trống ô Password Confirm", "EP",
  "Test User", "blankconfirm_{unique}@test.com", PW, "", "fail",
  "Báo bắt buộc nhập ô xác nhận, không đăng ký", ""),
 ("SIGNUP_013", "Negative", "Mật khẩu 7 ký tự (dưới tối thiểu 8)", "BVA",
  "Test User", "bva7_{unique}@test.com", "Abc@123", "{same}", "fail",
  "Báo mật khẩu tối thiểu 8 ký tự, không đăng ký",
  "Giả định tối thiểu 8 ký tự theo thông báo lỗi của hệ thống; cần xác nhận khi chạy"),
 ("SIGNUP_014", "Positive", "Mật khẩu đúng 8 ký tự (biên dưới hợp lệ)", "BVA",
  "Test User", "bva8_{unique}@test.com", "Abc@1234", "{same}", "success",
  "Đăng ký thành công",
  "Giả định tối thiểu 8 ký tự theo thông báo lỗi của hệ thống; cần xác nhận khi chạy"),
]

# Form dang ky thuc te KHONG co o Name: bo test "De trong ten" va cot Name, danh so lai ma
SIGNUP = [r for r in SIGNUP if r[2] != "Để trống tên"]
SIGNUP = [(f"SIGNUP_{i:03d}",) + r[1:4] + r[5:] for i, r in enumerate(SIGNUP, start=1)]

LOGIN_HEAD = ["Test Case ID", "Test Type", "Title", "Technique", "Email", "Password",
              "Expected", "Expected Result", "Notes", "Status", "Actual Result"]
SIGNUP_HEAD = ["Test Case ID", "Test Type", "Title", "Technique", "Email", "Password",
               "Confirm Password", "Expected", "Expected Result", "Notes", "Status", "Actual Result"]
WIDTH = {"Test Case ID": 14, "Test Type": 12, "Title": 36, "Technique": 14, "Name": 14, "Email": 30,
         "Password": 16, "Confirm Password": 16, "Expected": 11, "Expected Result": 46, "Notes": 36, "Status": 11, "Actual Result": 56}


def write_sheet(ws, head, rows):
    for c, h in enumerate(head, start=1):
        cell = ws.cell(1, c, h)
        cell.font = Font(name=FONT, bold=True, color="FFFFFF")
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[cell.column_letter].width = WIDTH[h]
    for r, row in enumerate(rows, start=2):
        values = list(row) + ["Not Run", ""]
        for c, v in enumerate(values, start=1):
            cell = ws.cell(r, c, v)
            cell.font = Font(name=FONT, size=10)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORDER
        ws.row_dimensions[r].height = 32
    ws.freeze_panes = "B2"


wb = Workbook()
ws = wb.active
ws.title = "Login"
write_sheet(ws, LOGIN_HEAD, LOGIN)
write_sheet(wb.create_sheet("Signup"), SIGNUP_HEAD, SIGNUP)

guide = wb.create_sheet("Guide")
rows = [
 ("HƯỚNG DẪN", ""),
 ("Mỗi dòng", "Một test case. Sửa/thêm dòng là thay đổi bộ test, không cần sửa code."),
 ("Expected", "success = hệ thống phải chấp nhận | fail = hệ thống phải từ chối | logout = đăng nhập rồi đăng xuất (sheet Login)"),
 ("{same}", "Cột Confirm Password: giống cột Password. Để trống = bỏ trống ô xác nhận."),
 ("{unique}", "Được thay bằng chuỗi theo thời gian, mỗi lần chạy khác nhau (tránh trùng email với lần chạy trước)."),
 ("${REGISTERED_EMAIL}", "Email vừa đăng ký thành công ở SIGNUP_001 trong lần chạy này (hoặc TEST_EMAIL trong file .env)."),
 ("${REGISTERED_PASS}", "Mật khẩu tương ứng (hoặc TEST_PASS trong file .env)."),
 ("Status / Actual Result", "Do chương trình ghi vào file test-output/reports/results.xlsx sau mỗi lần chạy, không ghi đè file này."),
 ("Status", "Pass | Fail | Blocked (thiếu dữ liệu để chạy) | Error (lỗi khi chạy, ví dụ không tìm thấy phần tử)"),
]
for r, (a, b) in enumerate(rows, start=1):
    guide.cell(r, 1, a).font = Font(name=FONT, bold=True)
    guide.cell(r, 2, b).font = Font(name=FONT)
    guide.cell(r, 2).alignment = Alignment(wrap_text=True, vertical="top")
guide.column_dimensions["A"].width = 24
guide.column_dimensions["B"].width = 110

wb.save(OUT)
print("Da tao", os.path.abspath(OUT), "-", len(LOGIN), "login +", len(SIGNUP), "signup")
