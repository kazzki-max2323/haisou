# rows5.json を ../niigata-shops.html に埋め込む（work/ で実行: python3 build.py && python3 inject.py）
import json
rows=json.load(open('rows5.json',encoding='utf-8'))
for r in rows:
    for k in ('fn','fk','fo'): r.pop(k,None)
p='../niigata-shops.html'
h=open(p,encoding='utf-8').read()
a=h.index('const ROWS = ')+len('const ROWS = '); b=h.index(';\nconst WARDS')
open(p,'w',encoding='utf-8').write(h[:a]+json.dumps(rows,ensure_ascii=False)+h[b:])
print(len(rows),'rows injected')
