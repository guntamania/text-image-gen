#!/bin/bash

# uvのインストール確認
if ! command -v uv &> /dev/null; then
    echo "uvがインストールされていません。インストールしてください:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "uvを使用してプロジェクトをセットアップ中..."

# 仮想環境の作成
uv venv

# 仮想環境をアクティベート
source .venv/bin/activate

# 依存関係のインストール
uv pip install -r requirements.txt

echo "セットアップ完了！"
echo ""
echo "仮想環境をアクティベートするには:"
echo "  source .venv/bin/activate"
echo ""
echo "使用方法:"
echo "  # 仮想環境内で実行"
echo "  python image_composer.py -t \"Hello World\" -b background.jpg -o result.png"
echo ""
echo "  # または uv run で実行"
echo "  uv run python image_composer.py -t \"Hello World\" -b background.jpg -o result.png"
echo ""
echo "主要オプション:"
echo "  -t, --text           画像に追加するテキスト"
echo "  -f, --foreground     前景画像のパス"
echo "  -b, --background     背景画像のパス (必須)"
echo "  -o, --output         出力ファイルのパス (必須)"
echo "  -x, --x-position     X座標"
echo "  -y, --y-position     Y座標"
echo "  --font-size          フォントサイズ"
echo "  --font-color         フォントカラー (R,G,B)"
echo ""
echo "例:"
echo "  # テキスト描画"
echo "  python image_composer.py -t \"タイトル\" -b bg.jpg -o out.png --font-size 60"
echo "  python image_composer.py -t \"縁取り\" -b bg.jpg -o out.png --stroke-width 2"
echo ""
echo "  # 画像合成"
echo "  python image_composer.py -f logo.png -b background.jpg -o result.png"
echo "  python image_composer.py -b bg.jpg -o out.png -x 100 -y 50"