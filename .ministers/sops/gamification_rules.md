# 遊戲化規則 — RPG 升級型

> 系統：6 條技能樹 + 總 Level（= 各 tree level 加總）。
> Display：每個 cycle 的 Knowledge Circle Report 上方加「🎮 狀態表」section。
> State：`.ministers/state/gamification.json`

## Level 曲線

每個 skill tree 各自升級。**升到 Lv N 需要累積 `N × 100` XP**（triangular）。

- Lv 1 → 100 XP
- Lv 5 → 1500 XP（累積）
- Lv 10 → 5500 XP
- Lv 20 → 21000 XP

簡單、可預測，不需要 exponential 爆炸。

## XP 規則（v1，可調）

### 🧠 Engineering
| 動作 | XP |
|------|----|
| LeetCode Easy | +10 |
| LeetCode Medium | +25 |
| LeetCode Hard | +50 |
| System Design 案例（看完 1 個） | +20 |
| System Design 練題 | +30 |
| 技術 blog 寫 1 篇 | +40 |
| AlchPlan / 自動化系統 commit（自動偵測 git log） | +5 |

### 🚀 Career Move
| 動作 | XP |
|------|----|
| 認真讀 1 個 JD + 1 頁筆記 | +15 |
| 連絡 1 位前同事 / 認識的人 | +20 |
| 投 1 個職缺 | +30 |
| 完成 1 輪模擬面試 | +40 |
| 接到 recruiter call | +50 |
| 進到 onsite | +200 |
| 拿到 offer | +500 |
| 連 4 週推進（streak bonus） | +100 |

### 💰 Quant（observed only）
| 訊號 | XP |
|------|----|
| WSLFinLab sandbox 任一 git commit（每日封頂 +30） | +10/commit |
| dashboard 上新增 1 檔策略 | +50 |
| 達成週 P&L 正報酬 | +30 |
| **Asher 主動回報重要進展（語音 / Telegram）** | +50 |

### 🎵 Music（observed only）
| 訊號 | XP |
|------|----|
| Bobo's FM 上新影片（YT API 接入後自動偵測） | +50 |
| 完成一首音樂作品（即使未上架） | +30 |
| **Asher 主動回報重要進展** | +30 |

### 🧘 Mind
| 動作 | XP |
|------|----|
| 日記新規則「1 格就算」達標 | +10 |
| 日記寫完整（≥3 個 section 有內容） | +25 |
| 語音 inbox 處理（轉錄成功） | +5 |
| 連 7 天有寫日記 streak | +30（bonus） |

### 💪 Body（待啟用）
> LifeCoach 下 cycle 提運動 / 飲食追蹤後啟用。可能規則：
> - 1 次運動 +15、1 週運動 3 次 +50、7 天睡足 6h +30 等

## 已預先解鎖（pre-seeded）

兩條既有副業給予初始 level，避免 Asher 被系統視為 0 XP 新手：

| Tree | 初始 Lv | XP | 理由 |
|------|--------|----|----|
| 💰 Quant | **Lv 10** | 5500 lifetime | WSLFinLab 已部署、200+ trades、ML 策略多檔 |
| 🎵 Music | **Lv 8** | 3600 lifetime | Bobo's FM 已上線、有作品、品牌定位完成 |
| 🧠 Engineering | **Lv 5** | 1500 lifetime | AlchPlan 系統 + WSLFinLab 之外的工程底子 |

預期未來這個系統會自然繼續累積，不會卡住。

## 成就（Achievements）

獨立於 level，是「重大里程碑」。已有 5 個解鎖（含預先承認的兩條副業既有成就）。預覽中有 8 個待解鎖，多數跟 13 跳槽計畫掛鉤。

## 如何更新

### 自動（cycle 中 Alchemy / LifeCoach 處理）
- 部長讀對應檔案（`leetcode.md`、`weekly-log.md`、`bujo/daily/`）變動，比對 last_circle 後 +XP
- WSLFinLab / Bobo's FM 從 git log / 外部 API 觀察（之後加）
- 寫進 `gamification.json` 的 `recent_xp_log`

### 手動（Asher 在對話中講）
- Session PM（Claude Code 對話）聽到 Asher 講「我刷了 ___」「我投了 ___」直接 +XP 並 commit

### Display 在哪
- Knowledge Circle Report 第一個 section：
  ```
  ## 🎮 Asher 狀態

  Total Lv 24 · 1,500 XP

  🧠 Engineering Lv 5 ▓▓░░ 200/500
  🚀 Career Move Lv 1 ░░░░ 0/100
  💰 Quant Lv 10 (observed)
  🎵 Music Lv 8 (observed)
  🧘 Mind Lv 0 ░░░░ 0/100
  💪 Body Lv 0 (尚未啟用)

  本 cycle +0 XP · 最近解鎖：🤖 自建 AI Agent 系統
  ```

## 反模式守則

- **不**用 XP 數字騙人 — 系統不會為了好看的進度條偽造紀錄
- **不**懲罰退步 — 沒做就是 0 XP，不扣分（避免 streak 焦慮）
- **不**強迫每個 tree 都要練 — 你可以一整個月只動 1 條，是你的選擇
- 預先解鎖 = 認可既有事實，不是免費贈送
