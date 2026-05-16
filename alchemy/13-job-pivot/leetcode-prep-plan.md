# LeetCode 復健計畫 — Asher 客製版

> 制定日期：2026-05-14
> 目標：6-8 週內把寫 code 手感拉回 L4 / Senior 面試水準
> 適用對象：Google L4 現職、前 MS Senior、年刷底子、最近 6 個月沒寫 code

## 鎖定設定（2026-05-14 Asher 確認）

- **主力語言**：Python 3
- **LeetCode Premium**：（待確認）
- **AI 協作策略**：見下方「AI 協作 SOP」與「車上口頭模式」

## 為什麼你的計畫跟主流不一樣

| 主流建議 | Asher 客製 | 原因 |
|---|---|---|
| 3-6 個月全程 | **6-8 週** | 你不是新手，是「生疏」不是「歸零」 |
| NeetCode 150 / 250 | **Blind 75** 為主 | 年刷底子在，要的是 pattern 喚醒，不是再學一遍 |
| 一天 4-6 題 | **一天 1-2 題** | 你下班時間幾乎全在 WSLFinLab，量不要爆 |
| 衝 L5 reasoning | **L4 / Senior 水準** | 你不是要升遷，是平移；reasoning 自然會到，不用刻意練 |
| 1-2 個月才開始 mock | **第 4 週就開始 mock** | 你需要的是「重新習慣口語化思考」，不是「學會思考」 |

## 高槓桿 Pattern 清單（10 個）

刷的時候每題先標記 pattern，刷完後檢查自己能不能在「30 秒內看出來」。

- [ ] Two Pointers（兩指針）
- [ ] Sliding Window（滑動視窗）
- [ ] Binary Search（二分搜尋）
- [ ] BFS / DFS（廣度／深度優先）
- [ ] Backtracking（回溯）
- [ ] Dynamic Programming（動態規劃 — 1D / 2D / 區間）
- [ ] Heap / Priority Queue（堆 / 優先佇列）
- [ ] Union-Find（並查集）
- [ ] Monotonic Stack（單調棧）
- [ ] Interval Merge（區間合併）

紅燈訊號：刷到第 3 週還有 pattern 看不出來，回頭把對應主題的 5-10 題集中刷一次。

---

## Phase 0 — 暖身（Week 1，目標：手感回來）

**目標**：確認環境、語言切回主力、寫第一題不卡 IDE。

- [ ] 確認主力語言（Python? Go? C++?）— 5 月底前決定，之後就不換
- [ ] 設好 LC editor + local IDE / Cursor / VS Code 環境
- [ ] 第 1-2 天：3-5 題 LC Easy（不挑題，隨便 Top 100 Easy 點開就刷）
- [ ] 第 3-7 天：每天 1 題 Easy + 1 題 Medium（Blind 75 前 7 題）

**紅燈訊號**：暖身週寫 Easy 還在 30 分鐘以上 — 不要硬上 medium，再給 3-5 天 easy。

---

## Phase 1 — Pattern Refresh（Week 2-4，目標：跑完 Blind 75）

**目標**：把 10 個 pattern 全部過一次，每個 pattern 至少 5 題。

**節奏**：一天 1-2 題（medium 為主），週末 catch up + 重做卡關的題。

- [ ] **Week 2**：Array / Hash / Two Pointers / Sliding Window（Blind 75 約 #1-20）
- [ ] **Week 3**：Binary Search / Stack / Tree BFS-DFS（Blind 75 約 #21-45）
- [ ] **Week 4**：Graph / DP / Heap / Backtracking（Blind 75 約 #46-75）

**每題流程（重要）**：
1. 看題 → 30 秒內標出 pattern guess
2. 寫 brute force（不論多醜，目的是確認懂題目）
3. 想最佳解 → 寫 → run
4. 看 editorial / NeetCode 影片對照
5. **記下哪裡卡到**（這是你的個人錯題本，比題目本身重要）

**紅燈訊號**：跑完 Blind 75 還有超過 3 個 pattern 不熟 — 進 Phase 2 之前用 NeetCode 對應 section 補 5 題。

---

## Phase 2 — Company-tagged Medium（Week 5-6，目標：適應 G / MS 題風）

**目標**：用 LC Premium 篩 Google + Microsoft 過去 6-12 個月的 medium 題，刷 30-50 題。

- [ ] 開 LC Premium（如果還沒有）
- [ ] 篩選：Google + Microsoft，Medium，Past 6 months
- [ ] 一天 2 題，按公司各刷一半
- [ ] 對每題額外做：**寫一個 1-2 句的 trade-off 註解**（時間 vs 空間 / 可讀性 vs 效率）— 這是 senior bar 的訊號

**紅燈訊號**：超過 40% 題在 25 分鐘內寫不完 — 退回 Phase 1 補弱項 pattern。

---

## Phase 3 — Mock + 維持（Week 7-8，目標：口語化）

**目標**：5 次以上 mock，確認你能 think aloud + 在被打斷時不亂。

- [ ] Mock 平台選一個：[Pramp](https://www.pramp.com)（免費，peer-to-peer）/ [Hello Interview](https://www.hellointerview.com)（付費，有 ex-FAANG）/ [interviewing.io](https://interviewing.io)（匿名 + 真實 FAANG）
- [ ] 至少 **5 次 mock**，4 次 coding + 1 次 system design（給 MS Senior 用）
- [ ] 平常維持：一天 1 題 medium（不挑，保持手感）
- [ ] 每週 1 次：回頭重做 2 題以前卡關的題目（spaced repetition）

**Mock 自我檢查表**：
- [ ] 30 秒內提出 clarifying questions
- [ ] 1 分鐘內 verbalize approach（不直接寫 code）
- [ ] 寫到一半被問「為什麼這樣」能 1 句答完
- [ ] complexity analysis 不用被催就主動講
- [ ] edge cases 自己找出 2-3 個

---

## 每日 / 每週 Routine

**Weekday（適合下班後 45-60 分鐘）**：
- 1 題 medium（25-40 分鐘）
- 看 editorial（5-10 分鐘）
- 寫 pattern + 卡點到錯題本（5 分鐘）

**Weekend（適合 2-3 小時 block）**：
- 重做本週卡關的 2-3 題
- Mock 1 次（Week 4 開始）
- 看 1-2 個系統設計影片（給 MS Senior）

## 紅燈訊號總表（什麼時候要調整計畫）

1. **Week 2 結束還在卡 Easy** → 多給 1 週 Phase 0
2. **Week 4 結束 Blind 75 沒跑完** → 不要硬衝 Phase 2，把 Blind 75 收尾
3. **Phase 2 medium 通過率 < 50%** → 退回補 pattern，不要繼續往前衝
4. **Mock 5 次 ≥ 3 次卡在「不知道從哪開始」** → 多刷 30 題 medium，再開 mock

## 資源連結

- [Blind 75（NeetCode 整理版）](https://neetcode.io/practice/practice/blind75)
- [NeetCode 150 — 影片講解](https://neetcode.io/practice/practice/neetcode150)
- [Sean Prashad LeetCode Patterns](https://seanprashad.com/leetcode-patterns/)
- [Hello Interview — Google L4 Guide](https://www.hellointerview.com/guides/google/l4)
- [Pramp 免費 mock](https://www.pramp.com)

## 進度追蹤（每週填）

| Week | Phase | 目標題數 | 實際 | Mock 次數 | 卡關 pattern | 備註 |
|---|---|---|---|---|---|---|
| 1 | 暖身 | 10 | | 0 | | |
| 2 | Pattern | 10-12 | | 0 | | |
| 3 | Pattern | 10-12 | | 0 | | |
| 4 | Pattern | 10-12 | | 1 | | |
| 5 | Company | 12-14 | | 1 | | |
| 6 | Company | 12-14 | | 1 | | |
| 7 | Mock + 維持 | 7 | | 2 | | |
| 8 | Mock + 維持 | 7 | | 2 | | |

---

## 給 Career 部長的 handoff note

- 本計畫由 Session PM + Asher 於 2026-05-14 共同制定
- Asher 路徑策略：Tier 1 Google 內轉（內轉 coding bar 可能更輕，但完整跑 Blind 75 不浪費）/ Tier 2 Microsoft Senior（需完整面試 loop）
- 如果 Tier 1 內轉啟動快、6 週內就要面，可以壓縮 Phase 2 → 1 週、直接進 mock
- Career 部長每 cycle 確認 Asher 上週進度（題數、mock 次數、卡點），不催不 nudge，只記錄
