# LeetCode + AI 協作 SOP

> 制定日期：2026-05-14
> 目的：用 Claude Code（桌上）+ 語音 AI（車上）把進步速度極大化，但不踩「AI 替你寫」的反模式
> 配套文件：[leetcode-prep-plan.md](./leetcode-prep-plan.md)

## 🚨 反模式（先講禁忌）

下面這些做了你會「感覺很快」但「實際零成長」，面試時會原形畢露：

1. ❌ **貼題目給 AI 直接要解答** — 你的大腦沒過 pattern recognition 環節
2. ❌ **寫一半卡住直接問 AI 補完** — 卡住的瞬間才是學習發生的地方
3. ❌ **讓 AI auto-complete 你的解** — Copilot/Cursor 在 LC editor 之外開著也算，會稀釋你「自己想」的肌肉
4. ❌ **看了 editorial 就跳下一題** — 沒寫過一遍 = 不會
5. ❌ **跟 AI 討論 30 分鐘但沒打開 LC editor** — 純口頭最後寫出來會驚訝地爛

> **核心原則**：AI 是教練不是代打。教練可以指出你哪邊跑姿不對，不能替你跑。

---

## 🖥️ 桌上模式 — Claude Code SOP

### 建議的 project 結構

我建議在 `/mnt/c/Users/ashershih/sandbox/leetcode-prep/` 開一個獨立目錄（跟 WSLFinLab 分開），用 Claude Code 開啟。建議的結構：

```
leetcode-prep/
├── CLAUDE.md                 # 給 Claude 的常駐指令（最重要）
├── solved/
│   └── 0001-two-sum/
│       ├── problem.md        # 題目（手動 copy 一次也是學習）
│       ├── attempt-1.py      # 你的第一次嘗試（不論對錯）
│       ├── final.py          # 收斂後的版本
│       ├── notes.md          # 我學到了什麼 / 卡在哪
│       └── variants.py       # AI 生成的 2-3 個變體題
├── stuck/                    # 卡關超過 45 分鐘的題目（之後 spaced repetition 用）
├── mistakes-log.md           # 我每次犯的錯誤類型統計
└── weekly-log.md             # 每週進度
```

### CLAUDE.md 內容（複製到該檔案）

```markdown
# LeetCode Prep — Claude 行為守則

## 你的角色：Coding 教練，不是代打

### 絕對禁止
- ❌ 在我請求前，不要寫任何解答 code
- ❌ 不要主動 spoiler 演算法選擇（例如「這題用 DP」）
- ❌ 不要用 Edit 工具改我的 attempt-*.py，那是我的學習軌跡

### 允許並鼓勵
- ✅ 問我釐清題目的問題（模擬面試官）
- ✅ 我寫出 brute force 後，問「複雜度多少？哪邊能優化？」
- ✅ 我提解法時，問「edge case 想到了嗎？」「為什麼是 O(n) 不是 O(nlogn)?」
- ✅ 我完成後，幫我 code review（風格 / clean code / pythonic）
- ✅ 我完成後，生成 2-3 個變體題（同 pattern 不同包裝）放到 variants.py
- ✅ 幫我把這題 tag pattern + 寫進 mistakes-log.md / weekly-log.md

### 觸發指令（我會明確說）
- 「我準備好了」→ 你扮演面試官，給我這題的 clarifying questions
- 「我有想法」→ 聽我講，問針對性問題，**不要給答案**
- 「我寫完了」→ 開始 code review + 變體題生成
- 「我卡 30 分鐘了給個 hint」→ 給「方向性提示」，不給解（例如「想想能不能用 hash map 換空間換時間」，不要說「用 hash map 存 complement」）
- 「給答案」→ 這時才可以給完整解 + 詳細講解
- 「我這次卡的點是 X」→ 寫進 mistakes-log.md，並從歷史記錄找相似的卡點

## 我的背景（你需要知道）
- Google L4 SWE，前 Microsoft Senior
- Python 3 主力
- 年刷 LeetCode 但休息 6 個月
- 目標：6-8 週復健到 L4 / Senior 面試水準
- 不是新手 — 請用 senior 對話水準，不要解釋 hash map 是什麼
```

### 一題的完整流程（範例：Two Sum）

| 階段 | 你做 | Claude Code 做 | 時間 |
|---|---|---|---|
| 1 | 開新題目，手動 copy 題目到 `problem.md` | 等 | 1 分 |
| 2 | 跟 Claude 說「我準備好了」 | 給你 3-5 個 clarifying questions | 2 分 |
| 3 | 在 LC editor 寫 brute force（不要在 IDE）| 等 | 5 分 |
| 4 | 跑過後 paste 到 `attempt-1.py`，跟 Claude 說「brute force 完成」 | 問你複雜度、要不要優化 | 1 分 |
| 5 | 自己想優化方向 → 寫 → run | 等（除非你說卡關） | 10-15 分 |
| 6 | AC 後 paste 到 `final.py`，說「我寫完了」 | code review + 生 2-3 變體題 | 5 分 |
| 7 | 看 NeetCode 影片對照 | 等 | 5-10 分 |
| 8 | 寫 `notes.md`（1-2 句卡點、學到什麼）| 等 | 2 分 |
| **合計** | | | **30-45 分鐘** |

如果第 5 步卡超過 15 分鐘 → 說「給個 hint」，再卡 10 分鐘 → 說「給答案」。**不要硬撐到 60 分鐘**，那是焦慮不是學習。

### Spaced Repetition（防遺忘）

- Claude 每週日問你：「上週 stuck/ 資料夾有 X 題，這週要重做哪 2 題？」
- 你選 2 題 → 不看舊解 → 重寫一次 → 對比
- 這個是 Phase 1-3 都要做的，最強的鞏固方法

---

## 🚗 車上模式 — 語音 AI 對話

### 為什麼這招特別猛

你在車上做不了的事：寫 code、看螢幕、查資料。
你在車上能做的事：**講話、思考、被質疑**。

這正好是 **mock interview 在練的東西** — think aloud + 被打斷不亂 + 把演算法用人話說清楚。所以車上 30 分鐘的價值，可能比你在桌前安靜寫 30 分鐘還高（對 mock interview 來說）。

### 工具選擇

| 工具 | 適合 | 不適合 |
|---|---|---|
| **Claude 手機 App 語音模式** | 即時雙向對話、被打斷追問 | 沒法回放、沒留 transcript |
| **Just Press Record + Voice Daemon**（你已有）| 留 transcript、結構化記錄 | 是 monologue 不是對話 |
| **Telegram Bot**（你已有）| 可以打字確認、有歷史 | 開車時打字危險 |

**推薦組合**：
- **主要**：Claude App 語音模式（雙向真對話）
- **輔助**：Just Press Record 錄你的 final summary（會自動進 voice-inbox → 你晚上回家可以看 transcript 整理）

### 三種車上練法（從易到難）

#### 練法 1：題目「口頭白板」（最基本）

**場景**：上班通勤 30 分鐘，提前看過題目（紅綠燈時瞄一眼 phone）

**對話開場白**（直接複製給 Claude App）：
> 「我在開車，我要用口頭講解一題 LeetCode 給你聽。題目是 [題號 + 題名]。你扮演面試官，我講的時候你只能：(1) 問釐清問題 (2) 質疑我的 approach (3) 提醒我漏想的 edge case。**不要給答案，不要說 pattern 名稱**。準備好了嗎？」

**你做**：
1. 用口頭講出 brute force（「我可以兩層 loop...」）
2. 講複雜度（「這是 O(n²)」）
3. 講優化方向（「能不能用空間換時間...」）
4. 講最終 approach + 邊界條件

**Claude 做**：
- 中途打斷追問「為什麼？」「O(n²) 怎麼算的？」「空 input 怎麼辦？」

**回家後**：
打開 leetcode-prep，跟 Claude Code 說「我今天車上講過 [題號]，現在我要寫」→ 直接進桌上模式第 3 步開始寫。

#### 練法 2：「綜合題」拆解（你問的這種）

**綜合題**指那種「LRU Cache / Design Twitter / Word Search II」這類混合多 pattern + 資料結構設計題。這種題在車上練特別有效，因為**主要工作是 architecture 不是 syntax**。

**對話開場白**：
> 「車上模式 — 我要拆解一題綜合題：[題目]。你的工作是逼我講清楚 (1) 我要用哪些資料結構 (2) 每個 operation 的複雜度 (3) 為什麼選這個資料結構而不是另一個。我講不清楚就追問，不要替我想。」

**你做**：
- 講 high-level architecture（「我會用一個 hash map + doubly linked list」）
- 講每個 API 的步驟（「get(key) 我先...然後...」）
- 講為什麼選 doubly 而不是 singly

**Claude 做**：
- 「為什麼不能用 single linked list？」
- 「如果 capacity 是 0 你的 code 會怎樣？」
- 「remove 操作怎麼做到 O(1)？」

**這正是 senior bar 的訊號** — 能講清楚 trade-off 比能寫出 code 更值錢。

#### 練法 3：Mock 預演（Phase 3 用）

**場景**：明天有真 mock，今天通勤先模擬

**對話開場白**：
> 「Mock 預演模式 — 你是 Google L4 面試官，我要跑完整流程：(1) 你出一題 medium，題目就講題不要講 pattern (2) 我做 clarifying questions (3) 我講 approach (4) 你質疑 (5) 我口頭講 code（一行一行講）(6) 你問複雜度 (7) 我講 edge cases。全程 25 分鐘，模擬時間壓力。」

**為什麼這比真 mock 還好用**：
- 通勤時間天天有，真 mock 一週 1-2 次
- Claude 不會手下留情，會盯細節
- 口頭講 code 是真實面試的硬技能（共享編輯器沒 autocomplete）

### 車上專屬注意事項

1. **安全第一**：不要看 phone，全程語音。複雜題目提前在家先看 5 分鐘。
2. **環境噪音**：開車時 Whisper 可能誤聽，重要結論用 Just Press Record 重講一次。
3. **不要寫 code**：抗拒「我跟你講 syntax」的衝動，講 logic 就好。Syntax 回家寫。
4. **時間 box**：一趟通勤一題，不要貪多。一週 5 趟車程 = 5 題口頭預演 = 約等於 2 次完整 mock 的訓練量。

---

## 📊 每週 AI 協作健診（給 Career 部長用）

每週日 Claude Code 自動跑這份檢查（你跟 Claude 說「跑 weekly AI 健診」）：

- [ ] 本週用「給答案」指令幾次？（>3 次是紅燈）
- [ ] 本週車上練幾題？（<3 題沒在用車上時間）
- [ ] mistakes-log.md 重複出現的 pattern 是哪個？
- [ ] 哪幾題卡 30 分鐘以上？要不要列入下週重做？

---

## 🔧 快速啟動 checklist

我跑完這 5 步你就能開始：

- [ ] 建立 `/mnt/c/Users/ashershih/sandbox/leetcode-prep/` 目錄
- [ ] 把上方 CLAUDE.md 範本寫入該目錄
- [ ] 在 Claude 手機 App 設一個 prompt 模板（車上模式的開場白）
- [ ] 第一題：選 Blind 75 #1 Two Sum 跑完整流程一遍（試水溫）
- [ ] 之後一週後評估：流程順不順、Claude 有沒有踩線、要不要調整 CLAUDE.md
