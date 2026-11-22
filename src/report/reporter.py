"""Xuat bao cao ket qua: Excel (results.xlsx) va HTML (report.html)."""
import html
import os
from collections import Counter

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill

FONT = "Arial"
FILLS = {
    "Pass": PatternFill("solid", fgColor="C6EFCE"),
    "Fail": PatternFill("solid", fgColor="FFC7CE"),
    "Blocked": PatternFill("solid", fgColor="FFEB9C"),
    "Error": PatternFill("solid", fgColor="F8CBAD"),
}
STATUSES = ["Pass", "Fail", "Blocked", "Error"]


def load_cases(testdata_path: str, sheet: str) -> list:
    """Doc cac test case cua mot sheet thanh list dict (khoa = ten cot viet thuong, '_' thay khoang trang)."""
    wb = load_workbook(testdata_path)
    ws = wb[sheet]
    headers = [str(c.value or "").strip().lower().replace(" ", "_") for c in ws[1]]
    cases = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[0]:
            continue
        case = dict(zip(headers, row))
        case["id"] = str(case["test_case_id"]).strip()
        cases.append(case)
    return cases


def write_excel(testdata_path: str, out_path: str, results: list, meta: dict) -> None:
    wb = load_workbook(testdata_path)
    by_sheet = {}
    for r in results:
        by_sheet.setdefault(r.sheet, {})[r.id] = r

    ranges = {}
    for sheet, by_id in by_sheet.items():
        ws = wb[sheet]
        header = {str(c.value or "").strip(): c.column for c in ws[1]}
        id_col, st_col, ac_col = header["Test Case ID"], header["Status"], header["Actual Result"]
        for row in range(2, ws.max_row + 1):
            tc_id = str(ws.cell(row, id_col).value or "").strip()
            if tc_id in by_id:
                res = by_id[tc_id]
                st = ws.cell(row, st_col, res.status)
                st.font = Font(name=FONT, bold=True, size=10)
                st.alignment = Alignment(horizontal="center", vertical="top")
                if res.status in FILLS:
                    st.fill = FILLS[res.status]
                ws.cell(row, ac_col, res.actual).alignment = Alignment(wrap_text=True, vertical="top")
        col = ws.cell(1, st_col).column_letter
        ranges[sheet] = f"'{sheet}'!${col}$2:${col}${ws.max_row}"

    # Sheet Summary dung cong thuc dem theo cot Status cua tung sheet
    sm = wb.create_sheet("Summary", 0)
    sm["A1"] = "TỔNG HỢP KẾT QUẢ KIỂM THỬ TỰ ĐỘNG"
    sm["A1"].font = Font(name=FONT, size=14, bold=True)
    for r, (k, v) in enumerate([("Thời gian chạy", meta.get("time", "")), ("Website", meta.get("base_url", "")),
                                ("Trình duyệt", meta.get("browser", ""))], start=2):
        sm.cell(r, 1, k).font = Font(name=FONT, bold=True)
        sm.cell(r, 2, v).font = Font(name=FONT)
    head = ["Chức năng", "Tổng", "Pass", "Fail", "Blocked", "Error", "Not Run", "Tỷ lệ Pass"]
    for c, h in enumerate(head, start=1):
        cell = sm.cell(6, c, h)
        cell.font = Font(name=FONT, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(horizontal="center")
    r = 7
    for sheet, rng in ranges.items():
        sm.cell(r, 1, sheet)
        sm.cell(r, 2, f"=COUNTA({rng})")
        for c, s in enumerate(["Pass", "Fail", "Blocked", "Error", "Not Run"], start=3):
            sm.cell(r, c, f'=COUNTIF({rng},"{s}")')
        sm.cell(r, 8, f"=IFERROR(C{r}/B{r},0)").number_format = "0.0%"
        r += 1
    if ranges:
        sm.cell(r, 1, "Tổng cộng").font = Font(name=FONT, bold=True)
        for c in range(2, 8):
            col = sm.cell(6, c).column_letter
            sm.cell(r, c, f"=SUM({col}7:{col}{r - 1})").font = Font(name=FONT, bold=True)
        sm.cell(r, 8, f"=IFERROR(C{r}/B{r},0)").number_format = "0.0%"
    for row in sm.iter_rows(min_row=7, max_row=r):
        for cell in row:
            if cell.font.name != FONT:
                cell.font = Font(name=FONT, size=10, bold=cell.font.bold)
    for col, w in zip("ABCDEFGH", [26, 24, 8, 8, 10, 8, 10, 12]):
        sm.column_dimensions[col].width = w
    sm.column_dimensions["B"].width = 40

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb.save(out_path)


def write_html(out_path: str, results: list, meta: dict) -> None:
    count = Counter(r.status for r in results)
    total = len(results)
    rate = f"{count['Pass'] * 100 / total:.1f}%" if total else "0%"
    rows = []
    for r in results:
        shot = (f'<a href="{html.escape(r.screenshot)}" target="_blank">Xem ảnh</a>' if r.screenshot else "")
        rows.append(
            f"<tr><td>{html.escape(r.sheet)}</td><td>{html.escape(r.id)}</td><td>{html.escape(r.title)}</td>"
            f"<td>{html.escape(r.expected)}</td><td><span class='b {r.status}'>{r.status}</span></td>"
            f"<td>{html.escape(r.actual)}</td><td>{shot}</td></tr>"
        )
    page = f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8"><title>Báo cáo kiểm thử tự động</title>
<style>
body{{font-family:Arial,sans-serif;margin:24px;color:#222}}
h1{{margin-bottom:4px}} .meta{{color:#555;margin-bottom:16px}}
.cards{{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap}}
.card{{border:1px solid #ccc;border-radius:8px;padding:12px 20px;min-width:90px;text-align:center}}
.card b{{display:block;font-size:26px}}
table{{border-collapse:collapse;width:100%;font-size:14px}}
th{{background:#1F4E78;color:#fff}} th,td{{border:1px solid #bbb;padding:6px 8px;text-align:left;vertical-align:top}}
.b{{padding:2px 8px;border-radius:10px;font-weight:bold}}
.Pass{{background:#C6EFCE}} .Fail{{background:#FFC7CE}} .Blocked{{background:#FFEB9C}} .Error{{background:#F8CBAD}}
</style></head><body>
<h1>Báo cáo kiểm thử tự động: Đăng nhập và Đăng ký</h1>
<div class="meta">Thời gian: {html.escape(meta.get('time',''))} | Website: {html.escape(meta.get('base_url',''))} | Trình duyệt: {html.escape(meta.get('browser',''))}</div>
<div class="cards">
<div class="card"><b>{total}</b>Tổng</div>
<div class="card Pass"><b>{count['Pass']}</b>Pass</div>
<div class="card Fail"><b>{count['Fail']}</b>Fail</div>
<div class="card Blocked"><b>{count['Blocked']}</b>Blocked</div>
<div class="card Error"><b>{count['Error']}</b>Error</div>
<div class="card"><b>{rate}</b>Tỷ lệ Pass</div>
</div>
<table><tr><th>Chức năng</th><th>Mã TC</th><th>Mô tả</th><th>Kỳ vọng</th><th>Trạng thái</th><th>Kết quả thực tế</th><th>Ảnh</th></tr>
{''.join(rows)}
</table></body></html>"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
