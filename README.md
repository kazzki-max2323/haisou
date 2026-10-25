# haisou

新潟県内のEC店舗（164件）の配送情報を検索・絞り込みする静的ページ。

- `index.html` — 検索ページ（ジャンル／配送業者／出店モール／クール便・メール便／市区町村で絞り込み、関東送料で並べ替え）
- `data/shops.json` — 店舗データ

`fetch` でJSONを読むため、ローカルではHTTPサーバー経由で開く:

```sh
python3 -m http.server
# → http://localhost:8000/
```

GitHub Pages でそのまま公開することもできる。
