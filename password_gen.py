import tkinter as tk
from tkinter import ttk
import secrets
import string
import os
import sys
import ctypes

def resource_path(relative_path):
    """ PyInstallerでEXE化した際のリソースパス解決用関数 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PW 生成")
        self.root.geometry("400x450") # 高さを少し調整
        self.root.resizable(False, False)

        # Windowsタスクバーアイコン設定
        try:
            myappid = 'mycompany.myproduct.subproduct.version'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        # アイコン設定
        try:
            icon_path = resource_path("icon.png")
            self.icon_img = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, self.icon_img)
        except Exception as e:
            print(f"Icon not found: {e}")

        # デフォルト変数
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=False)
        self.password_length = tk.IntVar(value=20)
        self.mode = tk.StringVar(value="random")

        self.setup_ui()
        self.generate_password()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TButton", font=("Meiryo UI", 10))
        style.configure("TLabel", font=("Meiryo UI", 10))
        
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # --- モード選択 ---
        mode_frame = ttk.LabelFrame(main_frame, text="パスワードの種類を選択", padding=10)
        mode_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="ランダム", variable=self.mode, 
                        value="random", command=self.toggle_options).pack(side="left", padx=10)
        ttk.Radiobutton(mode_frame, text="# PIN", variable=self.mode, 
                        value="pin", command=self.toggle_options).pack(side="left", padx=10)

        # --- カスタマイズ ---
        setting_frame = ttk.LabelFrame(main_frame, text="新しいパスワードをカスタマイズ", padding=10)
        setting_frame.pack(fill="x", pady=5)

        # 文字数スライダー
        length_frame = ttk.Frame(setting_frame)
        length_frame.pack(fill="x", pady=5)
        ttk.Label(length_frame, text="文字数").pack(side="left")
        self.length_label = ttk.Label(length_frame, text=str(self.password_length.get()))
        self.length_label.pack(side="right")
        
        self.slider = ttk.Scale(setting_frame, from_=4, to=64, orient="horizontal", 
                                variable=self.password_length, command=self.update_length_label)
        self.slider.pack(fill="x", pady=5)

        # オプション（数字・記号）
        self.options_frame = ttk.Frame(setting_frame)
        self.options_frame.pack(fill="x", pady=5)
        self.check_digits = ttk.Checkbutton(self.options_frame, text="数字", variable=self.include_digits)
        self.check_digits.pack(side="left", padx=(0, 15))
        self.check_symbols = ttk.Checkbutton(self.options_frame, text="記号", variable=self.include_symbols)
        self.check_symbols.pack(side="left")

        # --- 結果表示 ---
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill="x", pady=20)
        ttk.Label(result_frame, text="生成されたパスワード").pack(anchor="w", pady=(0, 5))
        
        self.entry_password = tk.Entry(result_frame, font=("Consolas", 16), justify="center", bd=2, relief="solid")
        self.entry_password.pack(fill="x", ipady=8)

        # --- ボタンエリア（修正箇所：横並び） ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)

        # コピーボタン (左側)
        self.btn_copy = tk.Button(btn_frame, text="パスワードをコピー", bg="#0066cc", fg="white", 
                             font=("Meiryo UI", 10, "bold"), relief="flat", cursor="hand2",
                             command=self.copy_to_clipboard)
        self.btn_copy.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)

        # 更新ボタン (右側)
        btn_refresh = tk.Button(btn_frame, text="パスワードを更新", bg="white", fg="#0066cc", 
                                font=("Meiryo UI", 10), relief="solid", bd=1, cursor="hand2",
                                command=self.generate_password)
        btn_refresh.pack(side="right", fill="x", expand=True, padx=(5, 0), ipady=5)

        # --- 通知用ラベル ---
        self.notify_label = tk.Label(self.root, text="コピーしました", bg="#333333", fg="white", 
                                     font=("Meiryo UI", 9), padx=10, pady=5)

    def update_length_label(self, event=None):
        self.length_label.config(text=f"{int(self.slider.get())}")

    def toggle_options(self):
        if self.mode.get() == "pin":
            self.check_digits.configure(state="disabled")
            self.include_digits.set(True)
            self.check_symbols.configure(state="disabled")
            self.include_symbols.set(False)
        else:
            self.check_digits.configure(state="normal")
            self.check_symbols.configure(state="normal")
        self.generate_password()

    def generate_password(self):
        length = self.password_length.get()
        mode = self.mode.get()
        chars = ""
        
        if mode == "pin":
            chars = string.digits
        else:
            chars += string.ascii_letters
            if self.include_digits.get():
                chars += string.digits
            if self.include_symbols.get():
                chars += string.punctuation

        if not chars: chars = string.ascii_letters

        generated = ''.join(secrets.choice(chars) for _ in range(length))
        
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, generated)

    def copy_to_clipboard(self):
        password = self.entry_password.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            self.show_notification("コピーしました")

    def show_notification(self, message):
        self.notify_label.config(text=message)
        self.notify_label.place(relx=0.5, rely=0.9, anchor="center")
        self.root.after(2000, self.hide_notification)

    def hide_notification(self):
        self.notify_label.place_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()