# haisou

新潟市内のネットショップの配送会社・送料をまとめた静的ページ（`data/shops.json` のうち所在地が新潟市内の会社を住所順に表示）。

公開URL: https://kazzki-max2323.github.io/haisou/

- `index.html` — 調査ページ（概要の数字・配送会社の記載状況グラフ・一覧表）
- `data/shops.json` — 店舗データ

`fetch` でJSONを読むため、ローカルではHTTPサーバー経由で開く:

```sh
python3 -m http.server
# → http://localhost:8000/
```

GitHub Pages でそのまま公開することもできる。

- `niigata-shops.html` — 新潟市8区のEC事業者リスト（350件・住所／配送会社／送料／出店先）。1ファイルで完結
