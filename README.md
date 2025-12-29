# 🏰 UnderPy - 雙引擎地下城冒險遊戲 (Dungeon RPG)

> **結合 MUD 文字冒險的深度與 彈幕射擊(Bullet Hell) 的刺激，一款以 Python 打造的實驗性 RPG。**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green) ![Pygame](https://img.shields.io/badge/Engine-Pygame-red) ![Status](https://img.shields.io/badge/Status-Release-orange)

## 📖 專案簡介 (Introduction)
**UnderPy** 是一個採用 **「雙引擎架構 (Dual-Engine Architecture)」** 開發的 RPG 遊戲。
遊戲本體採用 **Tkinter** 構建經典的文字冒險介面，強調劇本敘事與解謎；而當遭遇強敵時，系統將無縫切換至 **Pygame** 引擎，進入即時動作戰鬥模式。

玩家將扮演一名失去記憶的冒險者，在充滿史萊姆、哥布林與未知的地下城中探索，試圖打破輪迴，尋找「刪除世界」的真相。

## ✨ 核心特色 (Key Features)

### 🎮 遊戲體驗
* **多重結局系統**：包含普通結局、死亡結局與二周目隱藏的「真結局 (True Ending)」。
* **混合戰鬥模式**：
    * 一般戰鬥：策略回合制 (文字描述)。
    * BOSS 戰鬥：Undertale 風格的彈幕閃避 (Pygame)。
* **沉浸式敘事**：實作打字機文字特效與動態震動回饋。
* **完整存檔機制**：支援 JSON 進度保存，重啟遊戲後可延續冒險。

### 🛠️ 技術亮點 (Technical Highlights)
本專案在技術實作上解決了多項 GUI 開發難題：
1.  **異質視窗整合 (Integration)**：實現 Tkinter 主視窗與 Pygame 戰鬥視窗的無縫切換與控制權轉移。
2.  **資料驅動架構 (Data-Driven)**：將劇本邏輯與程式碼分離，透過 `Dictionary` 結構管理龐大的對話與選項。
3.  **非阻塞式延遲 (Non-blocking Delay)**：捨棄 `time.sleep`，全面採用 `root.after` 搭配 `Recursion` 實作動畫，確保介面永不卡死。
4.  **穩健的架構設計**：採用 `GameManager` (邏輯) 與 `GameUI` (顯示) 分離的設計模式，並解決了 Python 常見的循環引用 (Circular Dependency) 問題。

## 📂 專案結構 (Project Structure)

```text
UnderPy/
├── main.py              # 遊戲入口與核心管理器 (GameManager)
├── story/
│   └── script.py        # 劇本資料庫 (所有對話與場景設定)
├── ui/
│   └── game_ui.py       # Tkinter 介面封裝 (負責繪圖與特效)
├── battle/
│   └── battle_game.py   # Pygame 戰鬥系統 (Boss 戰邏輯)
├── assets/              # 遊戲素材 (圖片/音效)
│   └── images/
└── savefile.json        # 自動生成的存檔紀錄
