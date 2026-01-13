@echo off
cd /d %~dp0
setlocal

:: icon.pngがあるか確認
if not exist "icon.png" (
    echo [エラー] icon.png が見つかりません。
    echo このバッチファイルと同じ場所に icon.png を置いてください。
    pause
    exit /b
)

echo 画像変換ライブラリ(Pillow)を確認中...
pip install Pillow >nul 2>&1

echo.
echo icon.png を icon.ico に変換しています...

:: Pythonを使って変換を実行 (高画質のまま変換)
python -c "from PIL import Image; img = Image.open('icon.png'); img.save('icon.ico', format='ICO', sizes=[(256, 256)])"

if exist "icon.ico" (
    echo.
    echo [成功] icon.ico を作成しました！
    echo.
) else (
    echo.
    echo [失敗] 変換に失敗しました。
)

pause