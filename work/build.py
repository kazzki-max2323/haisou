import json,re
old={x['id']:x for x in json.load(open('rows4.json'))}
CM={'Y':'ヤマト','S':'佐川','J':'日本郵便','N':'西濃','F':'福山'}
WARDS=['中央区','北区','東区','江南区','秋葉区','南区','西区','西蒲区','区不明']
def ward(a):
    for w in sorted(WARDS,key=len,reverse=True):
        if a.startswith(w): return w
    m=re.search('(中央区|東区|西蒲区|西区|北区|江南区|秋葉区|南区)',a); return m.group(1) if m else ''
def fee(v):
    if v in (None,''): return ''
    v=v.replace('円','').replace(',','')
    return '無料/込' if v=='0' else f'{int(v):,}円'
GEN={}
def g(keys,name):
    for k in keys.split(','): GEN[k]=name
g('okomestore,takizawa,echigo-inahoya,niigata-rice,taueuta,oec-hoko,echigoyonezo,niigata1rice.base.shop,magokoromura.thebase.in,komekobo.base.shop,takaiag.thebase.in,akatsukashuraku.stores.jp,komenoya,niigatanosho.base.shop','米・農産物')
g('niigata,takano-shuzo,yokogoshi,shihukunosake,niigatameisyuoukoku,takarayama-brewery,mokku-seikatsu,osaka-saketen,tamasakete,watago.buyshop.jp,oguroshuzo-sake.shop-pro.jp','酒')
g('auc-niigatatakeuchi,kobari,moto7mita,niigatatakeuchi,arurunnoumi.shop-pro.jp,sakana-bandai.shop-pro.jp,souzaburou.shop-pro.jp','水産')
g('apron-niigata,popponopan,omochi,warabimochi-kamakura,minatoseika.shop-pro.jp,45cheesecake.base.shop,muffin7bell.base.shop,petitpas5500.stores.jp,huskygelato.stores.jp,dabcoffee.thebase.in,sakaiwacoffe.thebase.in,luxuoso.thebase.in,pureoolong.base.shop','菓子・飲料')
g('momokawamiso,anacpngt,niigata025,niigata-shop,kgtomioka,niigata-furusatowari,irisawa-seimen.shop-pro.jp,an-foods.shop-pro.jp,tsubasan.shop-pro.jp,seihyo.shop-pro.jp,murayamakennzi.shop-pro.jp,horishu.raku-uru.jp,kokonoyasai.official.ec,hshoney.base.shop,iwasakishoku.base.shop,eyamaga.thebase.in,nobutakurami.thebase.in,akasyachi1.thebase.in,fkblackbird.base.shop,giftsquare-hakusin,toyano,bean.shop-pro.jp','食品・ギフト')
g('kagayakifarm,yamayokajyuen,grapegarden.base.shop,fruitdome.shop-pro.jp,satonashien.stores.jp,edamame02.base.shop,daigoya,yamabiko-engei,green-very,leafs-hojuen,hokuetsu-noji,k8783.thebase.in,arbre,eguchi-ya.shop-pro.jp','農園・花・園芸')
g('chubonotakumi,emono-s,kyorituall,westwebstore,e-steps,adachiseisakusyo,three-s-s-s,kiri-pro,fshinbo.thebase.in,livewell,all-zakka,finchandec.shop-pro.jp,storeroom.shop-pro.jp','キッチン・家具・生活')
g('dissolve,hon-waka,firstmarket,threec-web,foottown,mittrom,laviris,cottonhouse-39,urbene,riverus.thebase.in,atticofalice.theshop.jp,piiiiece.thebase.in,tity.ocnk.net,embellir.shop-pro.jp,kojiseika.shop-pro.jp,vintagecolor.base.shop,kamedajima.theshop.jp,ntb.shop-pro.jp,rental-kimonomarket,persona0312.base.shop,dorainavanti.base.shop,erieballoon.stores.jp,letablier.stores.jp,kohiru.shop-pro.jp,h03tr.shop-pro.jp','衣料・服飾')
g('kyuzo-outdoor,smart-factory,paintlucky,bathking,valere,sonicpluscenterniigata,ysd01,keiyo3,ryoei-inc.shop-pro.jp,kitanoyasp-bb.stores.jp,fishon.theshop.jp,whiteleaf-mart,wish-shop,blackburn','工具・車・スポーツ')
g('tc-books,topculture,hakushindo-store,honoto.thebase.in,cinewind.thebase.in,npwonline.thebase.in,tniigata.thebase.in,lifemag.thebase.in,g-zero.shop-pro.jp,sasabun,minatoinari.thebase.in','本・趣味・文具')
def genre(id,shop):
    id2=re.sub('^(y-|b-)','',id)
    if id2 in GEN: return GEN[id2]
    if id in GEN: return GEN[id]
    if id in old and old[id].get('genre'):
        o=old[id]['genre']; return {'米':'米・農産物','菓子・米菓':'菓子・飲料','キッチン・金物':'キッチン・家具・生活'}.get(o,o)
    s=shop
    for k,v in [('米','米・農産物'),('酒','酒'),('鮭|海鮮|魚','水産'),('菓子|団子|パン','菓子・飲料')]:
        if re.search(k,s): return v
    return '雑貨・その他'
CORP=re.compile('株式会社|有限会社|合同会社|法人|組合|商店|酒店|商會|酒造|醸造|工業|製作所')
FULL={
'daikokuyaniigata':'中央区鳥屋野2-15-9','creimastudio':'東区紫竹2-1-6 メゾンフローラA-101','naka-store':'東区藤見町1-19-21',
'qurious':'西区坂井砂山3-6-50 Kハウス1F','emono-s':'西区寺尾上4-4-15-206','cyastore':'西区坂井砂山1-19-8','mittrom':'西区新通南1-1-9',
'kcshop000':'西区大野町889-3','yamabiko-engei':'秋葉区新津本町3-19-2','green-very':'秋葉区西島40-4','yamayokajyuen':'南区大郷2460-子',
'atechigo':'中央区女池上山3-13-10 Lily-be千歳','eurpmask-directshop':'中央区天神1-1 プラーカ3 HUB STATION KENTO内',
'y-hellodolly':'西区山田2580-3','y-riftencom':'江南区木津4-2-5','y-footmassage':'西区西小針台2-4-28','y-world-green-aquarium':'東区河渡新町1丁目丁58-1',
'y-sugaisyoukai77':'東区新石山3-16-3','y-oobikiyaking':'中央区万代1-2-3 コープ野村万代303',
'b-riverus.thebase.in':'中央区古町通7-943 プレミオビル1F','b-persona0312.base.shop':'中央区古町通5番町630-2','b-piiiiece.thebase.in':'中央区古町通2番町665-8',
'b-dabcoffee.thebase.in':'中央区水島町3-23 八千代マンション1F','b-pureoolong.base.shop':'中央区本町通6 本町中央市場商店街内','b-fishon.theshop.jp':'中央区蒲原町1-23',
'b-dorainavanti.base.shop':'中央区女池南3-5-8 SHS鳥屋野店1F','b-nobutakurami.thebase.in':'中央区古町通八番町1437-6 2F','b-sewinniigata.base.shop':'東区東明5-1-1 東明プラザ103',
'b-tniigata.thebase.in':'中央区沼垂西1-4-2 竹石ビルII 2階','b-nroom.thebase.in':'東区太平3-21-7 2F','b-takaiag.thebase.in':'西区金巻2463',
'b-honoto.thebase.in':'西区寺尾東2-24-8','b-sakaiwacoffe.thebase.in':'西区寺尾東2-23-19','b-tentkids.thebase.in':'西区小針2-42-10 佐山第二ビル2号',
'b-kamedajima.theshop.jp':'中央区東堀通4-452','b-luxuoso.thebase.in':'中央区東堀通11番町1754 リバティープラザ2','b-lifemag.thebase.in':'西蒲区和納2-48-17',
'b-rucoto.base.shop':'東区松島3-1-3','b-magokoromura.thebase.in':'西蒲区馬堀4692','b-vintagecolor.base.shop':'秋葉区小須戸360-1','b-erieballoon.stores.jp':'中央区西堀通3-258-48',
'b-petitpas5500.stores.jp':'東区東中島2-6-1','b-letablier.stores.jp':'江南区天野2-14-13','b-satonashien.stores.jp':'江南区二本木2-10-1','b-fruitdome.shop-pro.jp':'南区清水8791-2',
'b-watago.buyshop.jp':'江南区亀田四ツ興野2-3-3','b-cinewind.thebase.in':'中央区八千代2-1-1 万代シテイ第二駐車場ビル1階','b-fukushinomise.shop-pro.jp':'中央区上所2-2-2 新潟ユニゾンプラザ1階',
'o-blackburn':'中央区姥ヶ山4-19-1','o-arbre':'中央区笹口2-9-10','o-suzumasa':'西区五十嵐3の町10946-1','o-koyanagi':'南区大郷689','o-lepoelon':'南区白根1245-1',
'a-A12JZ3R8VBQ32M':'江南区手代山1-2-14','a-A6NGNDLZRD0UP':'中央区女池上山2-19-14','a-A19TN1Y1AU1W0B':'東区太平3-27-5','a-A2DMSA1ST9K47D':'西区五十嵐二の町8648-2',
'u-3':'西蒲区福井1833','b-sakana-bandai.shop-pro.jp':'中央区万代島2-2 にぎわい市場ピアBandai内','b-arurunnoumi.shop-pro.jp':'中央区万代島2-2 にぎわい市場ピアBandai内','u-4':'西蒲区曽根251-2',
}
rows=[];byid={}
def add(r):
    rows.append(r); byid[r['id']]=r; return r
def mk(id,shop,company,addr,tel,car,fees,cool,ch,url):
    indiv = company in ('個人','') and True
    comp = '個人事業主' if company in ('個人',) else (company or '—')
    a=addr
    a=FULL.get(id,addr)
    return {'id':id,'shop':shop,'company':comp,'ward':ward(addr),'addr':a,'tel':tel if (CORP.search(comp) and tel) else '',
            'carriers':car,'fn':fees[0],'fk':fees[1],'fo':fees[2],'cool':cool,'genre':genre(id,shop),'links':{ch:url},'cnote':''}
# rakuten
for ln in open('rnew.txt',encoding='utf-8'):
    p=ln.rstrip('\n').split('|')
    if len(p)<9: continue
    id,shop,comp,addr,tel,car,fs,cool,yid=p[:9]
    f=fs.split('/') if fs else ['','','']
    r=mk(id,shop,comp,addr,tel,[CM[c] for c in car],[fee(x) for x in f],bool(cool),'楽天',f'https://www.rakuten.co.jp/{id}/')
    if yid: r['links']['Yahoo!']=f'https://store.shopping.yahoo.co.jp/{yid}/'
    add(r)
ymerged={r['links']['Yahoo!'].split('/')[3] for r in rows if 'Yahoo!' in r['links']}
for ln in open('ynew.txt',encoding='utf-8'):
    p=ln.rstrip('\n').split('|')
    if len(p)<9: continue
    id,shop,comp,addr,car,fn,fk,fo,cool=p[:9]
    if id in ymerged: continue
    add(mk('y-'+id,shop,comp or '個人',addr,'',[CM[c] for c in car],[fee(fn),fee(fk),fee(fo)],bool(cool),'Yahoo!',f'https://store.shopping.yahoo.co.jp/{id}/'))
def chname(h):
    if re.search('base\\.shop|thebase\\.in|theshop\\.jp|official\\.ec|buyshop\\.jp',h): return 'BASE'
    if 'stores.jp' in h: return 'STORES'
    if 'shop-pro.jp' in h: return 'カラーミー'
    if 'ocnk.net' in h: return 'おちゃのこ'
    if 'raku-uru' in h: return '楽楽うる'
    return '自社サイト'
for ln in open('bnew.txt',encoding='utf-8'):
    p=ln.rstrip('\n').split('|')
    if len(p)<4: continue
    h,shop,comp,addr=p[:4]; rest=p[4:]
    car=''; cool=False; merge=None
    for x in rest:
        if x.startswith('='): merge=x[1:]
        elif x=='C': cool=True
        else: car=x
    ch=chname(h); url='https://'+h+'/'
    if merge and merge in byid:
        byid[merge]['links'][ch]=url; continue
    add(mk('b-'+h,shop,comp,addr,'',[CM[c] for c in car],['','',''],cool,ch,url))
# own sites from snippet / old rows
own=[('o-kashimaya','加島屋','株式会社加島屋','中央区東堀前通8番町1367','https://www.kashimaya.jp/','水産'),
     ('o-blackburn','ミリタリーギア BLACKBURN','ミリタリーギアBLACKBURN','中央区','https://blackburn.jp/','工具・車・スポーツ'),
     ('o-arbre','arbre-flower','fleur','中央区','http://arbre-flower.com/','農園・花・園芸'),
     ('o-suzumasa','すずまさ農園','株式会社すずまさ農園','西区','https://www.suzumasa-farm.jp/','米・農産物'),
     ('o-koyanagi','小柳農園','小柳農園','南区','https://koyanagi-noen.com/','米・農産物'),
     ('o-lepoelon','ル・ポワロン・ビス','ル・ポワロン・ビス','南区（旧白根市）','https://le-poelon-bis.com/','菓子・飲料')]
for id,shop,comp,addr,url,gn in own:
    CAR={'o-blackburn':['ヤマト'],'o-arbre':['ヤマト'],'o-koyanagi':['ヤマト','日本郵便'],'o-lepoelon':['ヤマト']}
    r=add(mk(id,shop,comp,addr,'',CAR.get(id,[]),['','',''],id in('o-koyanagi','o-suzumasa'),'自社サイト',url)); r['genre']=gn
for oid in ['a-A12JZ3R8VBQ32M','a-A6NGNDLZRD0UP','a-A19TN1Y1AU1W0B','a-A2DMSA1ST9K47D','w-5895091','s-0','s-4','s-8','s-14','u-3','u-4']:
    o=old[oid]
    addr=o['addr'].replace('新潟県新潟市','')
    if oid=='s-8':
        byid['takarayama-brewery']['links']['自社サイト']=o['url']; continue
    ch={'Amazon':'Amazon','au PAY':'au PAY','自社サイト':'自社サイト'}[o['src']]
    comp=o['company'] if o['company'] not in ('個人事業主',) else '個人'
    r=add(mk(oid,o['shop'],comp,addr,o.get('tel',''),o['carriers'],['',fee(o['kanto'].replace('〜','')) if o['kanto'] else '',''],o['cool'],ch,o['url']))
    if o['src']=='Amazon': r['cnote']='Amazonは配送会社非公開（'+o['amz']+'）'
    if o['kanto'].endswith('〜'): r['fk']+='〜'
    r['genre']=genre(oid,o['shop'])

GEN2={'ec.the-niigata.jp':'食品・ギフト','www.niigata-ogawaya.co.jp':'食品・ギフト','gataichi.com':'食品・ギフト','www.lutecia.jp':'菓子・飲料','sakenomatsuzawa.com':'酒',
'shop.niigata-miyage.com':'食品・ギフト','mattomento.com':'衣料・服飾','www.ichimasa-eshop.com':'水産','maruyahonten.shop':'菓子・飲料','www.honeymustard-shop.com':'雑貨・その他',
'dress-mitamasaki-lab.com':'衣料・服飾','rato.co.jp':'衣料・服飾','sanpou-g.net':'食品・ギフト','aoki-farm.shop':'米・農産物','terufuku.com':'食品・ギフト','n-kagayaki.sanchoku-prime.com':'米・農産物',
'www.fruitstomato.com':'農園・花・園芸','www.e-misoya.com':'食品・ギフト','sakurakoubou.jp':'雑貨・その他','www.niigata-osakaya.com':'菓子・飲料','www.dangoya.com':'菓子・飲料','e-kome-miso.com':'食品・ギフト',
'www.kojimaya-sake.co.jp':'酒','www.marutakekoizumi.com':'菓子・飲料','www.kato-s.co.jp':'工具・車・スポーツ','okashi-hanyu.com':'菓子・飲料','n-kome.jp':'米・農産物','sakekadoya.shop':'酒',
'kaikuukan.com':'キッチン・家具・生活','beau-decor.com':'キッチン・家具・生活','y-sake.com':'酒','ozawa-brand.com':'衣料・服飾','www.tecraft.co.jp':'工具・車・スポーツ','www.sakubei.com':'水産',
'solano-store.com':'米・農産物','mamiyafarm.com':'米・農産物','www.shop-kishimoto.com':'酒',
'mizunoflower.base.shop':'農園・花・園芸','sidemilitia.com':'衣料・服飾','time.official.ec':'衣料・服飾','okubosake.shop-pro.jp':'酒','sake-ikenori.com':'酒','www.yamazaki-saketen.com':'酒',
'suzuki-sengyo.com':'水産','kaisenya.umisanmi.co.jp':'水産','watanabe-sengyo.shop':'水産','bellmate.com':'菓子・飲料','www.ichiba-coffee.com':'菓子・飲料','nagaifarm.com':'米・農産物','kihei.shop-pro.jp':'菓子・飲料',
'shiiya-coffee.com':'菓子・飲料','konasnow.base.shop':'菓子・飲料','namifuku.buyshop.jp':'食品・ギフト','ramen-walker.shop-pro.jp':'食品・ギフト','unnmeemon.com':'食品・ギフト','www.moubouquet.com':'農園・花・園芸',
'sogafarm.jp':'米・農産物','www.okashi-kikuya.jp':'菓子・飲料','www.takaguchi-m.com':'食品・ギフト','niigatatokimeki.net':'米・農産物','takatsuka-farm.shop-pro.jp':'米・農産物','honmashuho.com':'酒',
'finepet-pet.com':'雑貨・その他','www.niigata-ffs.co.jp':'農園・花・園芸','katannu.jp':'キッチン・家具・生活','www.chez-ti.com':'菓子・飲料','sake-ones.com':'酒','nouen-sasaki.com':'米・農産物',
'www.syutujin.com':'菓子・飲料','www.dansirou.com':'食品・ギフト','maruko-foods.co.jp':'食品・ギフト','mirainouen.shop-pro.jp':'米・農産物','www.akaichi-budougu.com':'工具・車・スポーツ','regaroflower.com':'農園・花・園芸'}
for ln in open('onew.txt',encoding='utf-8'):
    p=ln.rstrip('\n').split('|')
    if len(p)<2: continue
    h=p[0]; url='https://'+h+'/'
    if p[1].startswith('='):
        t=p[1][1:]
        if t in byid: byid[t]['links']['自社サイト']=url
        else: print('MISSING merge',t)
        continue
    shop,comp,addr=p[1],p[2],p[3]; car=p[4] if len(p)>4 else ''; cool=len(p)>5 and p[5]=='C'
    r=add(mk('o2-'+h,shop,comp,addr,'',[CM[c] for c in car],['','',''],cool,'自社サイト',url)); r['genre']=GEN2.get(h,'雑貨・その他')


FS={};car_raw={}
_CN={'ヤマト':'ヤマト','クロネコ':'ヤマト','佐川':'佐川','ゆうパ':'日本郵便','日本郵便':'日本郵便','西濃':'西濃'}
for ln in open('fsite.txt',encoding='utf-8'):
    p=ln.rstrip('\n').split('|')
    if p[0]=='NEW' or len(p)<6: continue
    k,h,L,addr,car,cart=p[:6]
    cs=[]
    for c in car.split(','):
        if c in _CN and _CN[c] not in cs: cs.append(_CN[c])
    car_raw[k]=car
    FS[k]=(h,re.sub(r'\s','',addr.translate(str.maketrans('０１２３４５６７８９－−','0123456789--'))),cs,cart=='CART')
# extra addresses from web search (company registry / official pages)
for k,a in {'31':'秋葉区七日町2424','50':'西区黒鳥4877','51':'西区赤塚5586','54':'東区松島3丁目1-3','63':'西蒲区仁箇2674-6','2':'中央区白山浦2-23','60':'秋葉区新津本町4丁目25-2'}.items():
    if k in FS: FS[k]=(FS[k][0],a,FS[k][2],FS[k][3])
    else: FS[k]=('',a,[],False)
for i,ln in enumerate(open('fnew.txt',encoding='utf-8')):
    p=ln.rstrip('\n').split('|')
    if len(p)<4: continue
    r=add(mk('f-%d'%i,p[0],p[1],p[2],'',[],['','',''],False,'ふるさと納税','https://www.rakuten.co.jp/f151009-niigata/')); r['genre']=p[3]; r['cnote']='通販ページ未確認（ふるさと納税で発送）'
    if str(i) in FS:
        h,addr,car,cart=FS[str(i)]
        if addr:
            a=re.sub('^新潟市','',addr)
            if not r['addr'].startswith(a): r['addr']=a; r['ward']=ward(a)
        if car: r['carriers']=car; r['cool']='クール' in car_raw.get(str(i),'')
        if cart:
            r['links'][chname(h)]='https://'+h+'/'; r['cnote']=''
        elif h:
            r['links']['会社HP']='https://'+h+'/'; r['cnote']='会社HPに通販なし（ふるさと納税で発送）'
byid['westwebstore']['links']['自社サイト']='https://www.west-shop.co.jp/'
byid['westwebstore']['fk']=byid['westwebstore']['fk'] or '480円'

_raw=open('furu_raw.txt',encoding='utf-8').read()
def _n(x): return re.sub(r'(株式会社|有限会社|合同会社|\(株\)|\(有\)|（.*?）|\s|　|【.*?】)','',x)
_F={_n(re.sub(r'\(\d+\)$','',x.strip())) for x in _raw.split('¶')}
_F.discard('')
for r in rows:
    if 'ふるさと納税' in r['links']: continue
    k=_n(r['company'])
    if len(k)>=2 and k in _F: r['links']['ふるさと納税']='https://www.rakuten.co.jp/f151009-niigata/'
# 食べチョク・ポケマル producers
for ln in open('pnew.txt',encoding='utf-8'):
    if ln.startswith('#') or not ln.strip(): continue
    id,shop,comp,addr,car,cool,gn,tid,pid,merge=ln.rstrip('\n').split('|')
    links={}
    if tid: links['食べチョク']=f'https://www.tabechoku.com/producers/{tid}'
    if pid: links['ポケマル']=f'https://poke-m.com/producers/{pid}'
    if id=='m':
        r=byid[merge]; r['links'].update(links)
        if car and not r['carriers']: r['carriers']=[CM[c] for c in car]; r['cnote']=''
        continue
    r=add(mk(id,shop,comp or '—',addr,'',[CM[c] for c in car],['','',''],bool(cool),'食べチョク' if tid else 'ポケマル',''))
    r['links']=links; r['genre']=gn
    if addr=='区不明':
        r['ward']='区不明'; r['addr']='区不明'
    if not car: r['cnote']='記載なし（配送は商品ごと）' if tid else '記載なし（ポケマル経由）'
# carriers found on shipping/item pages (2nd pass)
_CR={}
for ln in open('carres.txt',encoding='utf-8'):
    p=ln.strip().split('|')
    if len(p)==2 and p[1]: _CR[p[0]]=p[1]
for r in rows:
    if r['carriers']: continue
    for u in r['links'].values():
        h=re.sub(r'^https?://','',u).split('/')[0]
        if h in _CR:
            r['carriers']=[CM[c] for c in _CR[h]]
            if r['cnote'].startswith('通販ページ未確認') or r['cnote']=='記載なし': r['cnote']=''
            break
# 日本郵便の内訳（P=ゆうパック, M=ゆうパケット等）
_JP=dict(l.strip().split('|') for l in open('jp.txt',encoding='utf-8') if l.strip())
for r in rows:
    if '日本郵便' in r['carriers']: r['jp']=_JP.get(r['id'],'')
# fix: atechigo address (女池上山 is 中央区)
for r in rows:
    if r['id']=='u-3': r['company']='峰乃白梅酒造株式会社'
    if r['id']=='u-4': r['company']='朝妻酒造株式会社'
    if not r['ward']: print('NOWARD',r['id'],r['addr'])
    if not r['carriers'] and not r['cnote']: r['cnote']='記載なし'
    r['ch']=list(r['links'].keys())
wo={w:i for i,w in enumerate(WARDS)}
rows.sort(key=lambda r:(wo.get(r['ward'],9),r['addr']))
json.dump(rows,open('rows5.json','w'),ensure_ascii=False)
from collections import Counter
print(len(rows),Counter(r['ward'] for r in rows))
print('carrier known',sum(1 for r in rows if r['carriers']),'fees',sum(1 for r in rows if r['fk']))
print(Counter(r['genre'] for r in rows))
