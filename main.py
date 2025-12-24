import tkinter as tk
from functools import partial
from story.script import SCENE_SCRIPT  # 確保你的 story/script.py 裡面有 "type": "INPUT"
from PIL import Image, ImageTk

# 嘗試匯入戰鬥模組，如果沒有則定義一個假的 (避免報錯)
try:
    from battle.battle_game import boss_battle
except ImportError:
    def boss_battle():
        print("【測試模式】未找到 battle_game，模擬戰鬥勝利")
        return "WIN"

# --- 1. Model 層: 角色類別 ---
class Character:
    def __init__(self, name, hp, atk):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        damage = self.atk  # 簡化：不計算亂數
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0
        return f"{self.name} 攻擊了 {target.name}，造成 {damage} 點傷害！"
    
    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

# --- 2. Controller 層: 遊戲管理器 (修正邏輯) ---
class GameManager:
    def __init__(self, ui):
        self.ui = ui
        self.player = Character("勇者", 100, 15)
        self.current_enemy = None
        self.game_state = "SCENE"
        self.script_data = SCENE_SCRIPT
        self.current_scene_id = "START"
        
        # 劇情變數：是否知道密碼
        self.known_password = None 

    def start_game(self, *args):
        """遊戲啟動和重置點"""
        self.player.hp = self.player.max_hp
        self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp}")
        self.load_scene("START")
    
    def load_scene(self, scene_id):
        self.current_scene_id = scene_id
        scene = self.script_data.get(scene_id)
        
        if not scene:
            self.ui.update_text(f"錯誤：找不到場景 ID: {scene_id}")
            self.ui.set_choices([], None)
            self.ui.update_image(None)
            return

        self.game_state = "SCENE"
        self.ui.update_text(scene["text"])
        
        # 設定圖片
        image_path = scene.get("image")
        self.ui.update_image(image_path)
        
        # ==========================================
        # ★★★ 關鍵修正處：檢查場景類型 ★★★
        # ==========================================
        # 如果劇本裡寫了 "type": "INPUT"，就顯示輸入框，隱藏按鈕
        if scene.get("type") == "INPUT":
            self.ui.show_input_field()      # 呼叫 UI 顯示輸入框
            self.ui.set_choices([], None)   # 清除所有按鈕
        else:
            self.ui.hide_input_field()      # 呼叫 UI 隱藏輸入框 (一般場景要藏起來)
            
            # 正常載入按鈕
            choices = list(scene["choices"].keys())
            self.ui.set_choices(choices, self.handle_scene_choice)

    def handle_scene_choice(self, choice):
        current_scene = self.script_data[self.current_scene_id]
        next_action = current_scene["choices"].get(choice)

        if not next_action:
            self.ui.append_text("無效的選項。")
            return
            
        # --- 特殊邏輯：Pygame 戰鬥 ---
        if next_action == "BATTLE_SLIME":
            self.ui.master.withdraw() # 隱藏主視窗
            
            # 呼叫戰鬥
            result = boss_battle() 
            
            self.ui.master.deiconify() # 顯示主視窗
            
            if result == "WIN":
                self.load_scene("WIN_SLIME")
            elif result == "LOSE":
                self.ui.update_text("你戰敗了... (Game Over)")
                self.ui.set_choices([], None)
            else:
                self.ui.update_text("你逃離了戰場。")
            return
        
        # --- 特殊邏輯：哥布林劇情 ---
        if next_action == "LEVEL_2_GOBLIN":
            self.player.hp -= 10
            self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp} (心理受創)")
        
        if next_action == "GOBLIN_SPARED":
            self.known_password = "9527" # 玩家獲得密碼
        
        # --- 結局處理 ---
        if next_action.startswith("END"):
            self.load_scene(next_action)
            self.ui.set_choices([], None)
            self.ui.hide_input_field()
            return
            
        # 一般跳轉
        self.load_scene(next_action)

    # --- 戰鬥 (純文字版) ---
    def enter_battle(self, enemy_name, hp, atk):
        self.game_state = "BATTLE"
        self.current_enemy = Character(enemy_name, hp, atk)
        self.ui.update_text(f"進入戰鬥！面對 {self.current_enemy.name}")
        self.ui.set_choices(["攻擊", "防禦", "逃跑"], self.handle_battle_choice)
        self.ui.hide_input_field()

    def handle_battle_choice(self, action):
        if action == "攻擊":
            message = self.player.attack(self.current_enemy)
            self.ui.append_text(message)
        
        if not self.current_enemy.is_alive():
            self.ui.append_text(f"你贏了！{self.current_enemy.name} 倒下了。")
            self.game_state = "SCENE"
            self.load_scene("WIN_SLIME")
            return

        enemy_message = self.current_enemy.attack(self.player)
        self.ui.append_text(enemy_message)
        self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp}")

        if not self.player.is_alive():
            self.ui.append_text("你戰敗了！Game Over。")
            self.ui.set_choices([], None)
            return

        self.ui.set_choices(["攻擊", "防禦", "逃跑"], self.handle_battle_choice)

    # --- 密碼輸入處理器 ---
    def handle_password_input(self, input_val):
        """處理 UI 傳回來的密碼"""
        self.ui.append_text(f"你輸入了：{input_val}")

        if input_val == "9527":
            self.ui.append_text("【系統】密碼正確！大門緩緩打開...")
            self.ui.hide_input_field()   # ★ 成功後隱藏輸入框
            self.load_scene("LEVEL_3_START")
        else:
            self.player.hp -= 5
            self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp} (錯誤懲罰)")
            self.ui.append_text("密碼錯誤！門發出了嘲笑的聲音。")
            
            if self.known_password:
                self.ui.append_text(f"提示：你記得哥布林說過密碼是 {self.known_password}")
            else:
                self.ui.append_text("提示：你根本不知道密碼... 早知道就不殺哥布林了。")

# --- 3. View 層: 介面類別 ---
class GameUI:
    def __init__(self, master, game_manager):
        self.master = master
        self.game = game_manager
        self.master.title("UnderPy")
        self.master.geometry("600x600")

        # 狀態顯示區
        self.status_label = tk.Label(master, text="HP:", anchor="w", fg="red")
        self.status_label.pack(pady=(10, 5), padx=20, fill="x")

        # 圖片顯示區
        self.image_label = tk.Label(master)
        self.image_label.pack(pady=5)
        self.current_image = None

        # 劇情文字區
        self.text_area = tk.Text(master, height=12, state='disabled')
        self.text_area.pack(pady=10, padx=20, fill="x")

        # --- 密碼輸入區 (平時隱藏) ---
        # 這裡不需要 pack，等 show_input_field 被呼叫時才 pack
        self.input_frame = tk.Frame(master)
        self.entry_field = tk.Entry(self.input_frame)
        self.entry_field.pack(side="left", padx=5)
        self.confirm_btn = tk.Button(self.input_frame, text="輸入", command=self.submit_password)
        self.confirm_btn.pack(side="left")

        # 按鈕區
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

    def update_status(self, text):
        self.status_label.config(text=text)

    def update_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.config(state='disabled')

    def append_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def set_choices(self, choices, handler_function):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        if choices and handler_function:
            for choice in choices:
                command = partial(handler_function, choice)
                btn = tk.Button(self.button_frame, text=choice, command=command, width=15)
                btn.pack(side="left", padx=10)

    def update_image(self, image_path=None):
        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((400, 300), Image.Resampling.LANCZOS)
                self.current_image = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.current_image)
            except Exception as e:
                print(f"載入圖片失敗: {e}")
                self.image_label.config(image="")
        else:
            self.image_label.config(image="")

    # --- 輸入框控制 ---
    def show_input_field(self):
        """顯示密碼輸入框"""
        # 這裡會把 frame 放到畫面上
        self.input_frame.pack(pady=10, after=self.text_area) 
        self.entry_field.delete(0, tk.END)
        self.entry_field.focus()

    def hide_input_field(self):
        """隱藏密碼輸入框"""
        self.input_frame.pack_forget()

    def submit_password(self):
        password = self.entry_field.get()
        self.game.handle_password_input(password)

# --- 4. 程式啟動 ---
if __name__ == '__main__':
    root = tk.Tk()
    
    # 1. 建立 Manager (還沒有 UI)
    game_manager = GameManager(None)
    
    # 2. 建立 UI (傳入 Manager)
    game_ui = GameUI(root, game_manager)
    
    # 3. 連接 UI 回 Manager
    game_manager.ui = game_ui

    # 4. 開始遊戲
    game_manager.start_game()
    
    root.mainloop()
