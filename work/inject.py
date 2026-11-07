# rows5.json を ../niigata-shops.html に埋め込む（work/ で実行: python3 build.py && python3 inject.py）
# geo.json（id -> [緯度, 経度, 国土地理院の住所検索で一致した住所]）があれば ll として入れる
import json, os
rows=json.load(open('rows5.json',encoding='utf-8'))
geo=json.load(open('geo.json',encoding='utf-8')) if os.path.exists('geo.json') else {}
for r in rows:
    for k in ('fn','fk','fo'): r.pop(k,None)
    g=geo.get(r['id'])
    a=r['addr'].replace(r['ward'],'').strip()
    # 区名だけ・番地非公開の住所は区の真ん中に落ちるので地図に出さない
    if g and r['ward']!='区不明' and a and not a.startswith('（'):
        r['ll']=[round(g[0],6),round(g[1],6)]
        if g[2]!='full': r['llq']=1  # 町名までしか合わなかった（位置はおおよそ）
p='../niigata-shops.html'
h=open(p,encoding='utf-8').read()
a=h.index('const ROWS = ')+len('const ROWS = '); b=h.index(';\nconst WARDS')
open(p,'w',encoding='utf-8').write(h[:a]+json.dumps(rows,ensure_ascii=False)+h[b:])
print(len(rows),'rows injected,',sum('ll' in r for r in rows),'with location')
