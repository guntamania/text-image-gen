# Text Image Generator

画像と背景を合成、またはテキストを画像に追加するコマンドラインツール

## 機能

### 画像合成
- 前景画像と背景画像を合成
- 位置調整（X、Y座標指定）
- 前景画像のリサイズ
- 透明度調整

### テキスト描画
- 画像上にテキストを描画
- 18文字での自動折り返し（複数行表示対応）
- フォントサイズ・色の指定
- 縁取り文字の作成
- カスタムフォントのサポート
- 位置調整（X、Y座標指定）

### 共通機能
- 自動的な画像フォーマット変換
- エラーハンドリング

## セットアップ

### uvを使用した方法（推奨）

```bash
# uvのインストール（まだインストールしていない場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# プロジェクトのセットアップ
./setup.sh

# または手動で
uv sync
```

### 従来の方法

```bash
pip3 install -r requirements.txt
```

## 使用方法

### 基本的な使用方法

```bash
# uvを使用した場合（推奨）
# テキストを画像に追加
uv run python image_composer.py -t "Hello World" -b background.jpg -o result.png

# 画像合成
uv run python image_composer.py -f logo.png -b background.jpg -o result.png

# 従来の方法
# テキストを画像に追加
python3 image_composer.py -t "Hello World" -b background.jpg -o result.png

# 画像合成
python3 image_composer.py -f logo.png -b background.jpg -o result.png
```

### オプション

#### 必須オプション
- `-b, --background`: 背景画像のパス（必須）
- `-o, --output`: 出力ファイルのパス（必須）

#### モード選択（どちらか一つ）
- `-f, --foreground`: 前景画像のパス（デフォルト: images/header.png）
- `-t, --text`: 画像に追加するテキスト

#### 位置調整
- `-x, --x-position`: X座標（デフォルト: 0）
- `-y, --y-position`: Y座標（デフォルト: 0）

#### 画像合成オプション
- `--resize-width`: 前景画像のリサイズ幅
- `--resize-height`: 前景画像のリサイズ高さ
- `--opacity`: 前景画像の不透明度（0.0-1.0、デフォルト: 1.0）

#### テキスト描画オプション
- `--font-size`: フォントサイズ（デフォルト: 50）
- `--font-color`: フォントカラー R,G,B（デフォルト: 255,255,255）
- `--font-path`: フォントファイルのパス
- `--stroke-width`: 縁取りの太さ（デフォルト: 0）
- `--stroke-color`: 縁取りの色 R,G,B（デフォルト: 0,0,0）

### 使用例

#### テキスト描画

##### uvを使用（推奨）
```bash
# 基本的なテキスト追加
uv run python image_composer.py -t "Hello World" -b background.jpg -o result.png

# 位置を指定してテキスト追加
uv run python image_composer.py -t "タイトル" -b bg.jpg -o out.png -x 100 -y 50

# フォントサイズと色を指定
uv run python image_composer.py -t "大きな赤い文字" -b bg.jpg -o out.png --font-size 80 --font-color 255,0,0

# 縁取り文字
uv run python image_composer.py -t "縁取り文字" -b bg.jpg -o out.png --stroke-width 2 --stroke-color 0,0,0

# カスタムフォント使用
uv run python image_composer.py -t "カスタムフォント" -b bg.jpg -o out.png --font-path /path/to/font.ttf
```

##### 従来の方法
```bash
# 基本的なテキスト追加
python3 image_composer.py -t "Hello World" -b background.jpg -o result.png

# 位置を指定してテキスト追加
python3 image_composer.py -t "タイトル" -b bg.jpg -o out.png -x 100 -y 50

# フォントサイズと色を指定
python3 image_composer.py -t "大きな赤い文字" -b bg.jpg -o out.png --font-size 80 --font-color 255,0,0

# 縁取り文字
python3 image_composer.py -t "縁取り文字" -b bg.jpg -o out.png --stroke-width 2 --stroke-color 0,0,0

# カスタムフォント使用
python3 image_composer.py -t "カスタムフォント" -b bg.jpg -o out.png --font-path /path/to/font.ttf
```

#### 画像合成

##### uvを使用（推奨）
```bash
# 基本的な合成（デフォルト前景画像を使用）
uv run python image_composer.py -b background.jpg -o result.png

# 特定の前景画像を使用
uv run python image_composer.py -f logo.png -b background.jpg -o result.png

# 位置を指定して合成
uv run python image_composer.py -f logo.png -b bg.jpg -o out.png -x 100 -y 50

# 前景画像をリサイズして合成
uv run python image_composer.py -f logo.png -b bg.jpg -o out.png --resize-width 200

# 透明度を調整して合成
uv run python image_composer.py -f logo.png -b bg.jpg -o out.png --opacity 0.7
```

##### 従来の方法
```bash
# 基本的な合成（デフォルト前景画像を使用）
python3 image_composer.py -b background.jpg -o result.png

# 特定の前景画像を使用
python3 image_composer.py -f logo.png -b background.jpg -o result.png

# 位置を指定して合成
python3 image_composer.py -f logo.png -b bg.jpg -o out.png -x 100 -y 50

# 前景画像をリサイズして合成
python3 image_composer.py -f logo.png -b bg.jpg -o out.png --resize-width 200

# 透明度を調整して合成
python3 image_composer.py -f logo.png -b bg.jpg -o out.png --opacity 0.7
```

## 対応フォーマット

- 入力: PNG, JPEG, GIF, BMP, TIFF等（Pillowがサポートする形式）
- 出力: PNG（透明度保持）

## 注意事項

- 前景画像が背景画像よりも大きい場合、自動的に調整されます
- 負の座標を指定すると、右下からの相対位置として扱われます
- 出力ディレクトリが存在しない場合、自動的に作成されます