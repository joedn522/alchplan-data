# wslfinlab-ideas（Finbot 草稿）

> 位置：Obsidian vault sync
> 
> 用途：作為 wslfinlab / finlab_v2 策略研究的「單一事實來源」草稿區。後續所有 Iter 011+ 的實驗設計、驗收標準、結果摘要都先落在這裡，再請 Claude 產出最終 HTML report 丟到 wslfinlab 的 strategy_reports。

---

## Floor Stock Burst（搶地板股）V10 → Iter 011+ Roadmap

來源報告：Iter 010 Full Report
- https://wslfinlab.asherdom.me/reports/topics/78e2b1_floor_stock_burst/rule/iter_010_full_report.html

### 現況（V10 Portfolio）摘要
- Portfolio 模型：5 槽位 FCFS，每槽 20% 固定比重（避免 sim() 再平衡陷阱）
- 近 3 年（2023–2025）：PF 高、平均單筆報酬佳
- 全期（2015–2025）：PF ~1.98，年均交易 ~29.1
- 已知失效 regime：2021（純多頭、無真恐慌）PF 極差
- 明星發現：Rev3m 濾網（B6）PF 很高，但交易量過低（~15.9/yr）

---

## 迭代原則（先穩健、再放量、最後才微調加碼/出場）

1) **先解決最大已知失效模式（Regime filter）**
2) **再做放量（dynamic BB threshold / Rev3m bucket）**
3) **最後才做加碼/出場進階（容易 overfit）**
4) 所有結論需附：年別切片（特別是 2021）、交易量、PF、平均單筆、MDD

---

## Iter 011（優先）：Market State Filter（regime robustness）

### Hypothesis B：只在「市場情緒崩」時啟動地板股

**動機**：Iter 010 明確指出 2021 類型市場會讓策略失效。

**最小可落地規則（不引入外部資料）**
- 以 0050 或加權指數 proxy：
  - 方案 B1：Market BB 位階 < 0 才允許進場
  - 方案 B2：Market MA20 slope < 0 才允許進場

**驗收（AC）**
- 2021 年 PF 明顯改善（至少不再災難）
- 不應大幅削弱 2018 / 2020 / 2023–2025 的有效表現
- 年均交易量仍維持可實戰水準（>= 20–30/yr，或由你指定）

**要產出的 artefacts**
- 年別績效表（2015–2025）
- 2021 的交易列表與失敗歸因（為何被 filter 擋下 / 為何仍進場）

---

## Iter 012：Rev3m 放量（Dynamic BB Threshold）

### Hypothesis A：基本面越強，恐慌門檻可放寬

**動機**：B6（Rev3m）PF 高但量太少。

**建議規則（bucket，不要一開始就連續函數）**
- Rev3m > 0.1：BB 位階 < -5
- 0 < Rev3m <= 0.1：BB 位階 < -7
- Rev3m <= 0：BB 位階 < -10（維持 V10）

**驗收（AC）**
- trades/yr 回到 >= 25–35/yr（或你指定）
- PF 仍維持 > 1.6–2.0（或你指定）

---

## Iter 013：加碼/出場進階（風控與右尾）

### Hypothesis C：ATR 波動度決定加碼間隔
- 目的：讓加碼以風險單位一致，而不是固定條件

### Hypothesis D：強彈日啟動 trailing stop
- 目的：把「少數大反彈」的右尾抓更久

**驗收（AC）**
- 右尾增厚（max trade / top decile return 提升）
- MDD 或尾部風險不惡化（或需有清楚 trade-off）

---

## Iter 014：資金閒置 → 互補策略（Portfolio Complementarity）

### Hypothesis E：填補地板股空窗期
- 先做量化：5 槽位下的資金使用率分布（<40% 的時間占比）
- 再設計互補策略（例如「強勢股回檔」）

---

## 工程/驗證規範（避免 tools 卡住 & 指標出現 0%/空值）

### 固定 preflight
- 確認：pytest / python / git 就緒（healthcheck_l1.sh）

### 指標一致性 guardrails
- avg_return_per_trade 必須以 CSV mean 為準（避免 JSON stale 值）
- stock_id 一律 str + zfill(4)
- Portfolio 模式固定比重 + FCFS（避免 sim() 再平衡陷阱）

### Debug log（env-gated）
- `DASHBOARD_DEBUG=1` 才印
- 每次 request 僅印一次 summary（策略數、含 sparkline 數、關鍵 metric 是否存在）

---

## 下一步待辦（Finbot）

1) 明確定義 Iter 011 的回測比較表格式（baseline V10 vs B1 vs B2）
2) 產出 Iter 011 proposal 的最終版（給 Claude 生成 HTML report）
3) 把 HTML report 掛到 `/strategy_reports`（Floor Stock Burst 卡片下新增一條「Iter 011 提案」連結）
