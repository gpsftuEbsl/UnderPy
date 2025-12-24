# UnderPy - Dungeon Adventure (v3.0)

這是一款基於 Python 製作的沉浸式文字冒險遊戲。採用 **MVC (Model-View-Controller)** 架構設計，結合了 Tkinter 的全螢幕介面與 Pygame 的戰鬥系統。

## 🛠 系統需求

* **Python 版本**: 3.10+
* **必要套件**:
* `Pillow` (PIL) - 負責圖片處理
* `pygame` - 負責 Boss 戰鬥模組



---

## 🏛 專案架構與職責

遊戲分為三大核心層次，確保程式碼具備良好的擴充性與可維護性：

1. **Model (`Character`)**: 定義實體屬性（HP、ATK）與基礎動作（攻擊、存活判定）。
2. **View (`GameUI`)**: 負責所有視覺呈現、全螢幕控制、打字機特效與物理回饋。
3. **Controller (`GameManager`)**: 遊戲的大腦，負責場景跳轉、劇情判斷、受傷邏輯與密碼驗證。

---

## 📖 模組與方法詳細說明

### 1. GameUI (介面控制器)

負責將遊戲狀態轉化為玩家可見的視覺特效。

| 方法名稱 | 參數 | 具體描述 |
| --- | --- | --- |
| `type_text` | `text`, `speed`, `clear` | **打字機特效核心**。具備「任務鎖定」功能，呼叫時會自動取消上一個未完成的打字任務，防止文字交疊。`clear=True` 用於換場景，`False` 用於追加訊息。 |
| `shake_window` | 無 | **物理回饋**。透過移動 `main_container` 的 `place` 座標，在全螢幕模式下模擬激烈的震動效果。 |
| `flash_red` | 無 | **視覺回饋**。將所有容器背景瞬間轉為血紅色，並在 100 毫秒後恢復，增加受傷的真實感。 |
| `update_image` | `image_path` | 自動縮放圖片至 500x350 並顯示於介面中心。 |
| `set_choices` | `choices`, `handler` | 動態生成選項按鈕，並綁定指定的處理函式（劇情用或戰鬥用）。 |
| `toggle_fullscreen` | `event` | 綁定 `F11`，在全螢幕與視窗模式間切換，並自動重置 UI 佈局。 |

---

### 2. GameManager (遊戲管理器)

負責核心邏輯運算與狀態轉換。

#### 🛡 中央受傷處理系統：`player_take_damage`

這是全遊戲唯一的扣血入口。當呼叫此方法時，系統會自動執行以下流程：

1. 扣除 HP 並確保不為負值。
2. 呼叫 `ui.update_status` 同步狀態。
3. 觸發 `ui.shake_window` 與 `ui.flash_red`。
4. 呼叫 `check_death` 進行生存判定。

#### ⚔️ 戰鬥迴圈：`handle_goblin_combat`

實現了「對話式回合制戰鬥」：

* **攻擊邏輯**：玩家與敵人的傷害訊息會被收集到一個列表，最後透過單次 `type_text` 一併輸出，避免打字機衝突。
* **防禦邏輯**：降低敵方攻擊力，提供策略性玩法。

#### 🔐 密碼驗證：`handle_password_input`

處理 `LEVEL_2_GATE` 的輸入邏輯。包含訊息合併技術，確保在密碼錯誤扣血時，提示訊息與受傷訊息能流暢地排隊打出。

---

## 🎮 遊戲流程圖

1. **START**: 進入地下城，初步探索。
2. **LEVEL 1**: 遭遇史萊姆（伏筆）並進入下一層。
3. **LEVEL 2 (Combat)**: 與哥布林進行對話式戰鬥。玩家可選擇放走（獲取密碼）或殺死。
4. **LEVEL 2 (Puzzle)**: 密碼鎖大門。輸錯會受傷，HP 歸零則 Game Over。
5. **LEVEL 3 (Boss Battle)**: 最終 Boss 戰（切換至 Pygame 模式）。

---

## 📁 資料夾結構

```text
UnderPy/
├── main.py              # 程式進入點，包含 GameManager
├── story/
│   └── script.py        # 遊戲劇本與分歧路徑
├── ui/
│   ├── __init__.py      # 套件宣告
│   └── game_ui.py       # Tkinter 全螢幕美化介面
├── battle/
│   └── battle_game.py   # Pygame Boss 戰戰鬥模組
└── assets/              # 存放遊戲圖片與素材

```

---
