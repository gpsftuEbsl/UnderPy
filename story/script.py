# --- 新增的劇本資料 (可放在 GameManager 外部，讓流程負責人單獨維護) ---
SCENE_SCRIPT = {
    "START": {
        "text": "你進入了一個地下城。前方出現一隻史萊姆！",
        "choices": {
            "調查": "SLIME_INFO",
            "戰鬥": "BATTLE_SLIME", # 特殊動作代號
            "逃跑": "END_RUN"
        }
    },
    "SLIME_INFO": {
        "text": "史萊姆看起來很飢餓。你確認了，這確實是一隻史萊姆。",
        "choices": {
            "準備戰鬥": "BATTLE_SLIME",
            "偷偷溜走": "END_RUN"
        }
    },
    "WIN_SLIME": {
        "text": "你贏了！史萊姆倒下了。你發現了一把生鏽的鑰匙。",
        "choices": {
            "繼續探索": "SCENE_2_ROOM"
        }
    },
    "SCENE_2_ROOM": {
        "text": "你來到了一扇古老的門前，這似乎是地下城的第二層入口。",
        "choices": {
            "用鑰匙開門": "END_WIN",
            "返回": "START" # 範例: 回到起點
        }
    },
    "END_RUN": {
        "text": "你成功逃跑了！遊戲結束。",
        "choices": {}
    },
    "END_WIN": {
        "text": "你打開了門，通往更深處的光芒籠罩了你。恭喜你完成了第一階段的探索！",
        "choices": {}
    },
}
# 戰鬥相關的場景 ID (例如 BATTLE_SLIME) 是特殊動作，由 GameManager 判斷處理。
