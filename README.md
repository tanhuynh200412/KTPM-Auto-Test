# Kiểm thử tự động Đăng nhập và Đăng ký (Selenium + Page Object Model)

Website kiểm thử: https://e-commerce-for-testing.onrender.com

## 1. Cấu trúc thư mục

```
KTPM_Auto/
├── main.py                      # Điểm chạy chính
├── config.yaml                  # URL, trình duyệt, thời gian chờ, thứ tự chạy
├── locators.yaml                # Kho định vị phần tử (đổi giao diện chỉ sửa file này)
├── requirements.txt
├── .env.example                 # Mẫu tài khoản dự phòng (tùy chọn)
├── src/
│   ├── base/
│   │   ├── base_setup.py        # Đọc cấu hình, khởi tạo trình duyệt, đánh thức server Render
│   │   └── helper.py            # Thao tác an toàn với phần tử (chờ, nhập, bấm, đọc thông báo)
│   ├── pages/
│   │   ├── base_page.py         # Lớp cha, cách chờ kết quả sau khi gửi form
│   │   ├── home_page.py         # Trang chủ, điều hướng sang đăng nhập / đăng ký
│   │   ├── signin_page.py       # Trang đăng nhập
│   │   └── signup_page.py       # Trang đăng ký
│   ├── testcases/executor.py    # Thực thi test case đọc từ Excel, quyết định Pass/Fail
│   └── report/reporter.py       # Xuất báo cáo HTML và Excel
├── resources/testdata/testcases.xlsx   # Dữ liệu test (sheet Login, Signup, Guide)
├── tools/
│   ├── make_testdata.py         # Tạo lại file testcases.xlsx
│   └── inspect_forms.py         # Đọc form đăng nhập/đăng ký để xác nhận locators
└── test-output/
    ├── reports/                 # report.html, results.xlsx
    └── screenshots/             # Ảnh chụp từng test case
```

<!-- TESTCASES:START -->
## Danh sách Test Case

### Đăng nhập (sheet `Login`)

| ID | Tên test case | Loại | Mô tả ngắn |
|---|---|---|---|
| `LOGIN_001` | Đăng nhập với tài khoản hợp lệ | Positive (EP) | Đăng nhập thành công, rời khỏi trang /signin |
| `LOGIN_002` | Đúng email, sai mật khẩu | Negative (EP) | Đăng nhập thất bại, ở lại trang /signin, có thông báo lỗi |
| `LOGIN_003` | Email chưa đăng ký | Negative (EP) | Đăng nhập thất bại, ở lại trang /signin, có thông báo lỗi |
| `LOGIN_004` | Để trống email | Validation (EP) | Báo bắt buộc nhập email, không đăng nhập |
| `LOGIN_005` | Để trống mật khẩu | Validation (EP) | Báo bắt buộc nhập mật khẩu, không đăng nhập |
| `LOGIN_006` | Để trống cả email và mật khẩu | Validation (EP) | Báo bắt buộc nhập thông tin, không đăng nhập |
| `LOGIN_007` | Email thiếu ký tự @ | Validation (EP) | Báo email sai định dạng, không đăng nhập |
| `LOGIN_008` | Email thiếu tên miền sau @ | Validation (EP) | Báo email sai định dạng, không đăng nhập |
| `LOGIN_009` | Email chỉ chứa khoảng trắng | Validation (EP) | Không đăng nhập, ở lại trang /signin |
| `LOGIN_010` | Email chứa chuỗi SQL injection | Security (Error guessing) | Không đăng nhập, ở lại trang /signin |
| `LOGIN_011` | Mật khẩu sai chữ hoa/thường | Negative (EP) | Đăng nhập thất bại (mật khẩu phân biệt hoa thường) |
| `LOGIN_012` | Đăng xuất sau khi đăng nhập | Session (State) | Đăng xuất thành công, nút Login hiện lại trên header |
| `LOGIN_013` | Mật khẩu 7 ký tự (dưới tối thiểu 8) | Negative (BVA) | Đăng nhập thất bại, ở lại trang /signin |

### Đăng ký (sheet `Signup`)

| ID | Tên test case | Loại | Mô tả ngắn |
|---|---|---|---|
| `SIGNUP_001` | Đăng ký với dữ liệu hợp lệ | Positive (EP) | Đăng ký thành công, rời khỏi trang /signup |
| `SIGNUP_002` | Đăng ký với email đã tồn tại | Negative (EP) | Đăng ký thất bại, báo email đã tồn tại |
| `SIGNUP_003` | Để trống email | Validation (EP) | Báo bắt buộc nhập email, không đăng ký |
| `SIGNUP_004` | Để trống mật khẩu | Validation (EP) | Báo bắt buộc nhập mật khẩu, không đăng ký |
| `SIGNUP_005` | Để trống tất cả các ô | Validation (EP) | Báo bắt buộc nhập thông tin, không đăng ký |
| `SIGNUP_006` | Email thiếu ký tự @ | Validation (EP) | Báo email sai định dạng, không đăng ký |
| `SIGNUP_007` | Email thiếu tên miền sau @ | Validation (EP) | Báo email sai định dạng, không đăng ký |
| `SIGNUP_008` | Email chỉ chứa khoảng trắng | Validation (EP) | Không đăng ký, ở lại trang /signup |
| `SIGNUP_009` | Email có khoảng trắng ở giữa | Validation (EP) | Báo email sai định dạng, không đăng ký |
| `SIGNUP_010` | Mật khẩu xác nhận không khớp | Validation (EP) | Báo mật khẩu xác nhận không khớp, không đăng ký |
| `SIGNUP_011` | Để trống ô Password Confirm | Validation (EP) | Báo bắt buộc nhập ô xác nhận, không đăng ký |
| `SIGNUP_012` | Mật khẩu 7 ký tự (dưới tối thiểu 8) | Negative (BVA) | Báo mật khẩu tối thiểu 8 ký tự, không đăng ký |
| `SIGNUP_013` | Mật khẩu đúng 8 ký tự (biên dưới hợp lệ) | Positive (BVA) | Đăng ký thành công |

> **Lưu ý:** các test giá trị biên (BVA) dùng giả định mật khẩu tối thiểu **8 ký tự**, theo thông báo lỗi của hệ thống.
> Nếu kết quả chạy thật khác, sửa dữ liệu trong file Excel (không cần sửa code).
<!-- TESTCASES:END -->

## 2. Cài đặt

```
pip install -r requirements.txt
```
Cần cài Google Chrome (hoặc Edge/Firefox). Selenium tự tải driver phù hợp, không cần tải chromedriver thủ công.
**Không đặt dự án trong C:\Windows\System32.**

## 3. Chạy

```
python main.py                              # chạy tất cả (Signup rồi Login)
python main.py --sheet Login                # chỉ chạy đăng nhập
python main.py --only SIGNUP_001,LOGIN_001  # chạy test case chỉ định
python main.py --headless                   # ẩn trình duyệt
python main.py --browser edge               # chrome | edge | firefox
```

Lần chạy đầu có thể chậm 30 đến 90 giây vì server Render (gói miễn phí) phải khởi động.

## 4. Cách hoạt động

- Mỗi dòng trong `testcases.xlsx` là một test case. Thêm/sửa dòng là thay đổi bộ test, không cần sửa code.
- Cột `Expected`: `success` (hệ thống phải chấp nhận), `fail` (hệ thống phải từ chối), `logout` (đăng nhập rồi đăng xuất).
- `{unique}` được thay bằng chuỗi theo thời gian để mỗi lần chạy tạo email mới.
- `${REGISTERED_EMAIL}` / `${REGISTERED_PASS}` là tài khoản vừa đăng ký thành công ở `SIGNUP_001`, dùng lại cho các test đăng nhập. Nếu không đăng ký được, điền `TEST_EMAIL` / `TEST_PASS` vào file `.env`.
- Trạng thái: **Pass**, **Fail**, **Blocked** (thiếu dữ liệu để chạy), **Error** (lỗi khi chạy, ví dụ không tìm thấy phần tử).
- "Thành công" được xác định khi trình duyệt rời khỏi trang `/signin` hoặc `/signup`, hoặc hiện thông báo thành công. "Thất bại" là vẫn ở lại trang.

## 5. Xác nhận locators trước khi chạy lần đầu

Form đăng ký thật gồm 3 ô: **E-mail, Password, Password Confirm** và nút **Sign Up** (không có ô Name). Locators của trang đăng nhập đã xác nhận; locators của ô Password Confirm (ô mật khẩu thứ 2) và nút Logout là **dự đoán hợp lý**, nên kiểm tra lại. Chạy:

```
python tools/inspect_forms.py
```
rồi đối chiếu `form_info.txt` với `locators.yaml` (các mục `signup.*`, `nav.logout`) và sửa nếu khác.

## 6. Kết quả

- `test-output/reports/report.html`: báo cáo trực quan, có link xem ảnh từng test case.
- `test-output/reports/results.xlsx`: dữ liệu test kèm Status, Actual Result và sheet Summary thống kê.
- `test-output/screenshots/`: ảnh chụp màn hình sau mỗi test case.
