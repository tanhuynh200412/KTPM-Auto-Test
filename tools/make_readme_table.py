"""Cap nhat muc 'Danh sach Test Case' trong README.md tu file resources/testdata/testcases.xlsx."""
import os

from openpyxl import load_workbook

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
START, END = "<!-- TESTCASES:START -->", "<!-- TESTCASES:END -->"


def table(ws) -> str:
    head = {str(c.value).strip(): c.column for c in ws[1]}
    lines = ["| ID | Tên test case | Loại | Mô tả ngắn |", "|---|---|---|---|"]
    for row in range(2, ws.max_row + 1):
        tc = ws.cell(row, head["Test Case ID"]).value
        if not tc:
            continue
        kind = f"{ws.cell(row, head['Test Type']).value} ({ws.cell(row, head['Technique']).value})"
        lines.append(f"| `{tc}` | {ws.cell(row, head['Title']).value} | {kind} | "
                     f"{ws.cell(row, head['Expected Result']).value} |")
    return "\n".join(lines)


wb = load_workbook(os.path.join(ROOT, "resources", "testdata", "testcases.xlsx"))
block = f"""{START}
## Danh sách Test Case

### Đăng nhập (sheet `Login`)

{table(wb['Login'])}

### Đăng ký (sheet `Signup`)

{table(wb['Signup'])}

> **Lưu ý:** các test giá trị biên (BVA) dùng giả định mật khẩu tối thiểu **8 ký tự**, theo thông báo lỗi của hệ thống.
> Nếu kết quả chạy thật khác, sửa dữ liệu trong file Excel (không cần sửa code).
{END}"""

path = os.path.join(ROOT, "README.md")
text = open(path, encoding="utf-8").read()
if START in text:
    pre, rest = text.split(START, 1)
    post = rest.split(END, 1)[1]
    text = pre + block + post
else:
    text = text.replace("## 2. Cài đặt", block + "\n\n## 2. Cài đặt", 1)
open(path, "w", encoding="utf-8").write(text)
print("Da cap nhat bang test case trong README.md")
