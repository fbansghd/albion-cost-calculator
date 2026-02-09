# Albion Cost Calculator

Albion Onlineのアイテム製作における利益率を分析するツールです。Albion Online Data Project APIから市場データを取得し、製作原価と市場価格を比較して利益率を計算します。

## 機能

- 🔍 **市場データ取得**: Albion Online Data Project APIから最新の価格データを取得
- 💰 **原価計算**: 素材価格とレシピから製作原価を自動計算
- 📊 **利益率分析**: 取引量で重み付けした平均価格から利益率を算出
- 📁 **CSV出力**: 分析結果をCSVファイルに出力して管理
- 🚀 **API制限対策**: レート制限(429エラー)に対する自動リトライ機能
- 🌍 **Windows対応**: 文字エンコーディング問題を解決

## プロジェクト構成

```
albion-cost-calculator/
├── config.py              # 設定ファイル（素材価格、レシピ、API設定）
├── calculator.py          # 計算関数（レシピ生成、原価計算）
├── item_lists.py          # アイテムリスト定義
├── profit_analyzer.py     # メインスクリプト
├── requirements.txt       # 依存パッケージ
└── README.md             # このファイル
```

### 各ファイルの役割

| ファイル | 説明 |
|---------|------|
| `config.py` | 素材価格、レシピデータ、API設定などの設定を管理 |
| `calculator.py` | レシピ生成、原価計算、アイテムリスト生成などの関数を提供 |
| `item_lists.py` | 分析対象のアイテム名リストとデフォルト設定を定義 |
| `profit_analyzer.py` | APIからデータを取得し、利益分析を実行するメインスクリプト |
| `requirements.txt` | 依存パッケージのリスト（aiohttp, pandas） |

## インストール

### 必要要件

- Python 3.7以上
- pip（Pythonパッケージマネージャー）

### 依存パッケージのインストール

requirements.txtを使用してインストール（推奨）：

```bash
pip install -r requirements.txt
```

または、個別にインストール：

```bash
pip install aiohttp pandas
```

## 使用方法

### 基本的な使い方

1. **アイテムリストの設定**

   `item_lists.py` を開き、分析したいアイテムのコメントアウトを解除します：

   ```python
   ALL_ITEM_NAMES = [
       "OFF_SHIELD",
       "OFF_BOOK",
       "OFF_TORCH",
       # "CAPE",          # ← コメントアウトを外すと分析対象に追加
       # "BAG",
       # "MAIN_SWORD",
       # ...
   ]
   ```

2. **スクリプトの実行**

   ```bash
   python profit_analyzer.py
   ```

3. **結果の確認**

   - コンソールに分析結果が表示されます
   - `item_profit_analysis_7days.csv` ファイルが生成されます

### 出力例

```
📊 データ取得結果:
   取得データ総数: 71件
   7日以内フィルタ後: 46件
   除外されたデータ: 25件

        item_id tier enchant       cost     avg_price        profit  profit_pct  trade_count       latest_update
  T5_OFF_SHIELD   T5           7018.048  16376.320755   9358.272755  133.345807          106 2026-02-08 12:00:00
   T5_OFF_TORCH   T5           7146.944  12366.000000   5219.056000   73.025002          210 2026-02-04 00:00:00
```

## 設定のカスタマイズ

### 素材価格の更新

`config.py` の `material_prices` 辞書を編集します：

```python
material_prices = {
    "T5_PLANK": 1006,      # ← 価格を更新
    "T5_PLANK@1": 1591,
    "T5_PLANK@2": 5873,
    # ...
}
```

### レシピの追加・変更

`config.py` の `base_recipes` 辞書を編集します：

```python
base_recipes = {
    "MAIN_SWORD": {"BAR": 16, "LEATHER": 8},
    "OFF_SHIELD": {"PLANK": 4, "BAR": 4},
    # 新しいアイテムを追加
    "YOUR_ITEM": {"PLANK": 8, "CLOTH": 8},
}
```

### API設定の調整

`config.py` で以下のパラメータを調整できます：

```python
# 同時リクエスト数（高いほど速いが、API制限に引っかかりやすい）
concurrent_requests = 7

# チャンクサイズ（一度に処理するアイテム数）
chunk_size = 7

# リトライ回数
retries = 5

# タイムアウト（秒）
timeout = 10

# 待機時間の設定
normal_wait_min = 0.4      # 通常の最小待機時間
normal_wait_max = 0.8      # 通常の最大待機時間
throttle_wait_base = 30    # 429エラー時のベース待機時間
throttle_wait_max = 60     # 429エラー時の最大待機時間
```

### ティアとエンチャントの変更

`item_lists.py` でデフォルト設定を変更できます：

```python
# ティア設定（例：T4～T8まで分析）
DEFAULT_TIERS = ["T4", "T5", "T6", "T7", "T8"]

# エンチャント設定（例：エンチャント無しとレベル1のみ）
DEFAULT_ENCHANTS = ["", "@1"]
```

## CSV出力フォーマット

生成されるCSVファイル（`item_profit_analysis_7days.csv`）の列：

| 列名 | 説明 |
|-----|------|
| `item_id` | アイテムID（例：T5_OFF_SHIELD@1） |
| `tier` | ティア（例：T5） |
| `enchant` | エンチャントレベル（例：@1） |
| `cost` | 製作原価（素材費 × リターン率考慮後） |
| `avg_price` | 取引量による重み付け平均価格 |
| `profit` | 利益額（avg_price - cost） |
| `profit_pct` | 利益率（%） |
| `trade_count` | 総取引数 |
| `latest_update` | 最新データの更新日時 |

## トラブルシューティング

### UnicodeEncodeError が発生する

Windowsで絵文字や日本語が表示できない場合、`profit_analyzer.py` に以下が含まれているか確認してください：

```python
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

### 429エラーが頻発する

API制限に引っかかっている場合：

1. `config.py` で `concurrent_requests` を減らす（例：7 → 3）
2. `chunk_size` を減らす（例：7 → 3）
3. `throttle_wait_base` を増やす（例：30 → 60）

### データが取得できない

1. インターネット接続を確認
2. Albion Online Data Project APIが稼働しているか確認
3. アイテムIDが正しいか確認（`item_lists.py`）

### ImportError が発生する

すべてのファイルが同じディレクトリにあることを確認してください：
- `config.py`
- `calculator.py`
- `item_lists.py`
- `profit_analyzer.py`

## 技術仕様

### データソース
- **API**: Albion Online Data Project (https://east.albion-online-data.com)
- **対象市場**: Black Market
- **データ期間**: 過去7日間

### 計算ロジック

#### 原価計算
```
原価 = Σ(素材価格 × 必要数) × (1 - リターン率)
```

#### 重み付け平均価格
```
重み付け平均 = Σ(価格 × 取引数) / Σ(取引数)
```

#### 利益率
```
利益率(%) = (平均価格 - 原価) / 原価 × 100
```

### リターン率
デフォルトのリターン率は **15.2%** （`return_rate = 0.152`）です。これは製作時に戻ってくる素材の割合を示します。

## ライセンス

このプロジェクトは個人使用・学習目的で作成されています。

## 貢献

バグ報告や機能追加の提案は、GitHubのIssuesでお願いします。

## 免責事項

- このツールはAlbion Onlineの公式ツールではありません
- 市場価格は常に変動するため、実際の利益を保証するものではありません
- APIの利用制限を遵守してください

## 更新履歴

### v2.0.0 (2026-02-09)
- コードベースを完全リファクタリング
- モジュール構造に分離（config, calculator, item_lists, profit_analyzer）
- 重複コードを削除
- ドキュメント（docstring）を追加
- Windows UTF-8エンコーディング対応

### v1.0.0
- 初回リリース
- 基本的な市場データ取得と利益分析機能
