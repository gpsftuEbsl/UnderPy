# story/script.py

# 劇情數據模組，使用字典儲存所有對話腳本

# --- 遊戲初始介紹 ---
INTRO_SCENE = {
    "id": "INTRO_01",
    "text": "歡迎來到 UnderPy 的世界。你醒來時，發現自己被困在一個未知的洞穴裡。",
    "speaker": "旁白",
    "next": "NPC_MEET"  # 指向下一個劇情段落
}

# --- 遇到 NPC 的對話 ---
NPC_MEET = {
    "id": "NPC_02",
    "text": "一位看起來很友善的 NPC 站在前方。 '嗨！陌生人，你還好嗎？'",
    "speaker": "NPC A",
    "next": "CHOICE_1"  # 指向一個選項
}

# --- 戰鬥前的對話 ---
PRE_BATTLE = {
    "id": "BATTLE_01",
    "text": "NPC 突然變臉：'抱歉，這是規定！準備好戰鬥吧！'",
    "speaker": "NPC A",
    "next_action": "START_BATTLE"  # 特殊指令，告訴 manager.py 啟動 Pygame
}

# 使用字典儲存選項與分支 (Choices and Branches)

CHOICE_1 = {
    "id": "CHOICE_01",
    "text": "你要如何回應這位友善的 NPC？",
    "speaker": "旁白",
    "options": [
        {
            "text": "1. 友好地打招呼。",
            "target": "BATTLE_01"  # 選項 1 導向戰鬥
        },
        {
            "text": "2. 保持沉默。",
            "target": "ENDING_PACIFIST" # 選項 2 導向和平結局（如果選擇製作）
        }
    ]
}

# 儲存結局文本 (Ending Text)

