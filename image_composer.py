#!/usr/bin/env python3
"""
Image Composer CLI Tool
画像と背景を合成するコマンドラインツール
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

def wrap_text(text, max_chars=18):
    """
    テキストを指定文字数で折り返す関数
    
    Args:
        text: 折り返すテキスト
        max_chars: 1行の最大文字数
        
    Returns:
        折り返されたテキストの行のリスト
    """
    if not text:
        return []
    
    lines = []
    current_line = ""
    
    for char in text:
        if char == '\n':
            lines.append(current_line)
            current_line = ""
        elif len(current_line) >= max_chars:
            lines.append(current_line)
            current_line = char
        else:
            current_line += char
    
    if current_line:
        lines.append(current_line)
    
    return lines

def add_text_to_image(image_path, output_path, text, x=None, y=None, font_size=50, 
                     font_color=(0, 0, 0), font_path=None, 
                     stroke_width=0, stroke_color=(0, 0, 0)):
    """
    画像にテキストを描画する関数
    
    Args:
        image_path: 背景画像のパス
        output_path: 出力ファイルのパス
        text: 描画するテキスト
        x: テキストのX座標
        y: テキストのY座標
        font_size: フォントサイズ
        font_color: フォントカラー (R, G, B)
        font_path: フォントファイルのパス
        stroke_width: 縁取りの太さ
        stroke_color: 縁取りの色 (R, G, B)
    """
    try:
        # 画像を読み込み
        image = Image.open(image_path)
        
        # 画像をRGBAに変換
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # 描画オブジェクトを作成
        draw = ImageDraw.Draw(image)
        
        # フォントを設定
        try:
            if font_path and Path(font_path).exists():
                font = ImageFont.truetype(font_path, font_size)
            else:
                # 日本語フォントを試す（macOSのフォントパス）
                japanese_fonts = [
                    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
                    "/System/Library/Fonts/ヒラギノ明朝 ProN W6.ttc",
                    "/System/Library/Fonts/Hiragino Sans W6.ttc",
                    "/System/Library/Fonts/Hiragino Mincho ProN W6.ttc",
                    "/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
                    "/Library/Fonts/Arial Unicode MS.ttf"
                ]
                
                font = None
                for font_name in japanese_fonts:
                    try:
                        font = ImageFont.truetype(font_name, font_size)
                        break
                    except:
                        continue
                
                if font is None:
                    # デフォルトフォントを使用（サイズ指定）
                    try:
                        font = ImageFont.load_default(size=font_size)
                    except TypeError:
                        # 古いPillowバージョンの場合
                        font = ImageFont.load_default()
        except:
            try:
                font = ImageFont.load_default(size=font_size)
            except TypeError:
                font = ImageFont.load_default()
        
        # テキストを18文字で折り返し
        text_lines = wrap_text(text, 18)
        
        # 各行の高さとサイズを計算
        line_heights = []
        line_widths = []
        for line in text_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_widths.append(bbox[2] - bbox[0])
            line_heights.append(bbox[3] - bbox[1])
        
        # 行間のスペース
        line_spacing = max(line_heights) * 0.2 if line_heights else 0
        total_text_height = sum(line_heights) + line_spacing * (len(text_lines) - 1)
        max_text_width = max(line_widths) if line_widths else 0
        
        # 画像のサイズを取得
        img_width, img_height = image.size
        
        # 複数行テキストのセンタリング位置を計算
        if x is None:
            x = (img_width - max_text_width) // 2
        if y is None:
            y = (img_height - total_text_height) // 2
        
        # 各行を描画
        current_y = y
        for i, line in enumerate(text_lines):
            # 各行を水平センタリング
            line_x = x
            if x is None or (len(text_lines) > 1):  # 複数行の場合は各行をセンタリング
                line_x = (img_width - line_widths[i]) // 2
            
            # テキストを描画
            if stroke_width > 0:
                # 縁取り付きテキスト
                draw.text((line_x, current_y), line, font=font, fill=font_color, 
                         stroke_width=stroke_width, stroke_fill=stroke_color)
            else:
                # 通常のテキスト
                draw.text((line_x, current_y), line, font=font, fill=font_color)
            
            # 次の行の位置を計算
            current_y += line_heights[i] + line_spacing
        
        # 結果を保存
        image.save(output_path, format='PNG')
        print(f"テキスト追加完了: {output_path}")
        
    except FileNotFoundError as e:
        print(f"エラー: ファイルが見つかりません - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

def compose_images(foreground_path, background_path, output_path, x=0, y=0, 
                  resize_width=None, resize_height=None, opacity=1.0, blend_mode='normal'):
    """
    画像を合成する関数
    
    Args:
        foreground_path: 前景画像のパス
        background_path: 背景画像のパス
        output_path: 出力ファイルのパス
        x: 前景画像のX座標
        y: 前景画像のY座標
        resize_width: 前景画像のリサイズ幅
        resize_height: 前景画像のリサイズ高さ
        opacity: 前景画像の不透明度 (0.0-1.0)
        blend_mode: ブレンドモード
    """
    try:
        # 画像を読み込み
        foreground = Image.open(foreground_path)
        background = Image.open(background_path)
        
        # 前景画像をRGBAに変換（透明度対応）
        if foreground.mode != 'RGBA':
            foreground = foreground.convert('RGBA')
        
        # 背景画像をRGBAに変換
        if background.mode != 'RGBA':
            background = background.convert('RGBA')
        
        # 前景画像のリサイズ
        if resize_width or resize_height:
            original_width, original_height = foreground.size
            
            if resize_width and resize_height:
                new_size = (resize_width, resize_height)
            elif resize_width:
                aspect_ratio = original_height / original_width
                new_size = (resize_width, int(resize_width * aspect_ratio))
            else:
                aspect_ratio = original_width / original_height
                new_size = (int(resize_height * aspect_ratio), resize_height)
            
            foreground = foreground.resize(new_size, Image.Resampling.LANCZOS)
        
        # 不透明度を適用
        if opacity < 1.0:
            alpha = foreground.split()[-1]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            foreground.putalpha(alpha)
        
        # 合成位置の調整
        fg_width, fg_height = foreground.size
        bg_width, bg_height = background.size
        
        # 座標が負の場合の処理
        if x < 0:
            x = max(0, bg_width + x - fg_width)
        if y < 0:
            y = max(0, bg_height + y - fg_height)
        
        # 画像が背景からはみ出さないように調整
        x = min(x, bg_width - fg_width) if x + fg_width > bg_width else x
        y = min(y, bg_height - fg_height) if y + fg_height > bg_height else y
        
        # 画像を合成
        result = background.copy()
        result.paste(foreground, (x, y), foreground)
        
        # 結果を保存
        result.save(output_path, format='PNG')
        print(f"画像合成完了: {output_path}")
        
    except FileNotFoundError as e:
        print(f"エラー: ファイルが見つかりません - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='画像と背景を合成、またはテキストを画像に追加するコマンドラインツール',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 画像合成
  python image_composer.py -b background.jpg -o result.png
  python image_composer.py -f logo.png -b bg.jpg -o out.png -x 100 -y 50
  
  # テキスト追加
  python image_composer.py -t "Hello World" -b bg.jpg -o out.png
  python image_composer.py -t "タイトル" -b bg.jpg -o out.png --font-size 60 --font-color 255,0,0
  python image_composer.py -t "縁取り文字" -b bg.jpg -o out.png --stroke-width 2 --stroke-color 0,0,0
        """
    )
    
    # モード選択
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('-f', '--foreground', default='images/header.png',
                           help='前景画像のパス（合成する画像）（デフォルト: images/header.png）')
    mode_group.add_argument('-t', '--text',
                           help='画像に追加するテキスト')
    
    # 背景画像オプション
    parser.add_argument('-b', '--background',
                       help='背景画像のパス（省略時はimages/内の画像を使用）')
    parser.add_argument('-o', '--output', required=True,
                       help='出力ファイルのパス')
    
    # 位置オプション
    parser.add_argument('-x', '--x-position', type=int,
                       help='X座標 (省略時は水平センタリング)')
    parser.add_argument('-y', '--y-position', type=int,
                       help='Y座標 (省略時は垂直センタリング)')
    
    # 画像合成オプション
    parser.add_argument('--resize-width', type=int,
                       help='前景画像のリサイズ幅')
    parser.add_argument('--resize-height', type=int,
                       help='前景画像のリサイズ高さ')
    parser.add_argument('--opacity', type=float, default=1.0,
                       help='前景画像の不透明度 (0.0-1.0, デフォルト: 1.0)')
    
    # テキスト描画オプション
    parser.add_argument('--font-size', type=int, default=50,
                       help='フォントサイズ (デフォルト: 50)')
    parser.add_argument('--font-color', default='0,0,0',
                       help='フォントカラー R,G,B (デフォルト: 0,0,0)')
    parser.add_argument('--font-path',
                       help='フォントファイルのパス')
    parser.add_argument('--stroke-width', type=int, default=0,
                       help='縁取りの太さ (デフォルト: 0)')
    parser.add_argument('--stroke-color', default='0,0,0',
                       help='縁取りの色 R,G,B (デフォルト: 0,0,0)')
    
    args = parser.parse_args()
    
    # 背景画像の設定
    if not args.background:
        # images/ディレクトリから画像を選択
        images_dir = Path('images')
        if not images_dir.exists():
            print("エラー: images/ディレクトリが見つかりません")
            sys.exit(1)
        
        # 画像ファイルを検索
        image_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif']:
            image_files.extend(images_dir.glob(ext))
            image_files.extend(images_dir.glob(ext.upper()))
        
        if not image_files:
            print("エラー: images/ディレクトリに画像ファイルが見つかりません")
            sys.exit(1)
        elif len(image_files) == 1:
            args.background = str(image_files[0])
            print(f"背景画像として使用: {args.background}")
        else:
            # 複数ある場合はプロンプトで選択
            print("複数の画像が見つかりました。使用する背景画像を選択してください:")
            for i, img_file in enumerate(image_files, 1):
                print(f"  {i}: {img_file.name}")
            
            while True:
                try:
                    choice = int(input("番号を入力してください: ")) - 1
                    if 0 <= choice < len(image_files):
                        args.background = str(image_files[choice])
                        print(f"背景画像として使用: {args.background}")
                        break
                    else:
                        print("無効な番号です。")
                except (ValueError, KeyboardInterrupt):
                    print("\nキャンセルされました。")
                    sys.exit(1)
    
    # 背景画像の存在確認
    if not Path(args.background).exists():
        print(f"エラー: 背景画像が見つかりません - {args.background}")
        sys.exit(1)
    
    # 出力ディレクトリの作成
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.text:
        # テキスト描画モード
        try:
            # カラーの解析
            font_color = tuple(map(int, args.font_color.split(',')))
            stroke_color = tuple(map(int, args.stroke_color.split(',')))
            
            if len(font_color) != 3 or len(stroke_color) != 3:
                raise ValueError("色は R,G,B 形式で指定してください")
            
            add_text_to_image(
                args.background,
                args.output,
                args.text,
                args.x_position,
                args.y_position,
                args.font_size,
                font_color,
                args.font_path,
                args.stroke_width,
                stroke_color
            )
            
        except ValueError as e:
            print(f"エラー: {e}")
            sys.exit(1)
    else:
        # 画像合成モード
        if not Path(args.foreground).exists():
            print(f"エラー: 前景画像が見つかりません - {args.foreground}")
            sys.exit(1)
        
        # 不透明度の範囲チェック
        if not 0.0 <= args.opacity <= 1.0:
            print("エラー: 不透明度は0.0から1.0の範囲で指定してください")
            sys.exit(1)
        
        compose_images(
            args.foreground,
            args.background,
            args.output,
            args.x_position,
            args.y_position,
            args.resize_width,
            args.resize_height,
            args.opacity
        )

if __name__ == '__main__':
    main()