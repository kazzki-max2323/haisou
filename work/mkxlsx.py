import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter as L

h = open('niigata-shops.html', encoding='utf-8').read()
a = h.index('const ROWS = ') + len('const ROWS = ')
b = h.index(';\nconst WARDS')
rows = json.loads(h[a:b])
WARDS = ['中央区', '北区', '東区', '江南区', '秋葉区', '南区', '西区', '西蒲区']
CARS = ['ヤマト', '日本郵便', '佐川', '西濃', '福山']
F = 'Arial'

wb = Workbook()
ws = wb.active
ws.title = '一覧'
head = ['区', '住所', 'ショップ', '会社', 'ジャンル', '出店先', '配送会社', 'クール便', '電話', 'URL'] + CARS + ['配送会社わかる']
ws.append(head)
for r in rows:
    url = list(r['links'].values())[0]
    ws.append(['新潟市' + r['ward'], '新潟市' + r['addr'], r['shop'], r['company'], r['genre'], '・'.join(r['ch']),
               '・'.join(r['carriers']) if r['carriers'] else (r['cnote'] or '記載なし'),
               '○' if r['cool'] else '', r['tel'], url])
n = len(rows) + 1
for i in range(2, n + 1):
    for j, c in enumerate(CARS):
        ws.cell(i, 11 + j, f'=IF(ISNUMBER(SEARCH("{c}",$G{i})),1,0)')
    ws.cell(i, 16, f'=IF(SUM(K{i}:O{i})>0,1,0)')
    ws.cell(i, 10).hyperlink = ws.cell(i, 10).value
tab = Table(displayName='EC一覧', ref=f'A1:{L(len(head))}{n}')
tab.tableStyleInfo = TableStyleInfo(name='TableStyleLight9', showRowStripes=True)
ws.add_table(tab)
W = [11, 30, 26, 24, 14, 16, 20, 8, 14, 34] + [6] * 5 + [8]
for j, w in enumerate(W, 1):
    ws.column_dimensions[L(j)].width = w
for j in range(11, 17):
    ws.column_dimensions[L(j)].hidden = True
for row in ws.iter_rows(min_row=1, max_row=n):
    for c in row:
        link = c.column == 10 and c.row > 1
        c.font = Font(name=F, size=11, bold=c.row == 1,
                      color='FFFFFF' if c.row == 1 else ('0563C1' if link else '000000'),
                      underline='single' if link else None)
        c.alignment = Alignment(vertical='top', wrap_text=c.column in (2, 3, 4, 6, 7))
ws.freeze_panes = 'C2'

s = wb.create_sheet('集計')
s.column_dimensions['A'].width = 18
s.column_dimensions['B'].width = 10
s.column_dimensions['C'].width = 10
nf = Font(name=F, size=11)
bold = Font(name=F, size=11, bold=True)
mut = Font(name=F, size=10, color='666666')
R = 2000
cells = {
    'A1': '新潟市EC事業者リスト 集計',
    'A2': '「一覧」で絞り込むと、ここの数字とグラフが表示中の行だけで計算し直されます。',
    'A4': '表示中の件数', 'B4': f'=SUBTOTAL(103,一覧!C2:C{R})',
    'A5': '配送会社がわかった', 'B5': f'=SUBTOTAL(109,一覧!P2:P{R})',
    'A6': '記載なし・非公開', 'B6': '=B4-B5',
    'A7': 'クール便あり',
    'B7': f'=SUMPRODUCT(SUBTOTAL(103,OFFSET(一覧!H2,ROW(一覧!H2:H{R})-ROW(一覧!H2),0)),--(一覧!H2:H{R}="○"))',
    'A9': '配送会社', 'B9': '件数', 'C9': '割合',
    'A15': '※割合は「配送会社がわかった」件数に対して。1店で複数書いていることがあるので合計は100%を超えます。',
    'A17': '区', 'B17': '件数',
    'A27': '出典：各ショップの特定商取引法表記・会社概要（2026年10月25日調べ）。',
    'A28': '会社を追加するときは「一覧」の表の一番下に入力すると、表と集計が自動で広がります。',
}
for k, v in cells.items():
    s[k] = v
for i, c in enumerate(CARS):
    r = 10 + i
    col = L(11 + i)
    s.cell(r, 1, c)
    s.cell(r, 2, f'=SUBTOTAL(109,一覧!{col}2:{col}{R})')
    s.cell(r, 3, f'=IFERROR(B{r}/$B$5,0)').number_format = '0%'
for i, w in enumerate(WARDS):
    r = 18 + i
    s.cell(r, 1, '新潟市' + w)
    s.cell(r, 2, f'=SUMPRODUCT(SUBTOTAL(103,OFFSET(一覧!A2,ROW(一覧!A2:A{R})-ROW(一覧!A2),0)),--(一覧!A2:A{R}="新潟市{w}"))')
for row in s.iter_rows(min_row=1, max_row=28, max_col=3):
    for c in row:
        if c.value is None:
            continue
        if c.row == 1:
            c.font = Font(name=F, size=14, bold=True)
        elif c.row in (2, 15, 27, 28):
            c.font = mut
        elif c.row in (9, 17):
            c.font = bold
            c.fill = PatternFill('solid', fgColor='DCEFEE')
        elif c.row in (4, 5, 6, 7) and c.column == 2:
            c.font = Font(name=F, size=12, bold=True)
        else:
            c.font = nf

ch = BarChart()
ch.type = 'bar'
ch.title = '配送会社（表示中）'
ch.add_data(Reference(s, min_col=2, min_row=9, max_row=14), titles_from_data=True)
ch.set_categories(Reference(s, min_col=1, min_row=10, max_row=14))
ch.legend = None
ch.y_axis.majorGridlines = None
ch.x_axis.scaling.orientation = 'maxMin'
ch.dataLabels = DataLabelList()
ch.dataLabels.showVal = True
ch.series[0].graphicalProperties.solidFill = 'C98A00'
ch.height = 7
ch.width = 12
s.add_chart(ch, 'A30')
wb.active = 0
wb.save('niigata-shops.xlsx')
print(n)
