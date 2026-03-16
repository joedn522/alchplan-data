# 10 - 工作情境 Scenario 盤點

目標：把「軟體工程師日常」拆成可被 AI 介入的具體情境，後面所有 prompt / workflow 都會對應到這些情境，而不是抽象的「幫我寫 code」。

## 粗列情境（先當草稿，之後可補充）

- **Debug / Issue Investigation**
  - 讀錯誤訊息、log trace
  - 從大量 log / trace ID 裡定位問題根因
  - 針對 flaky test / race condition 的排查

- **Code Comprehension / Code Review**
  - 快速理解 legacy code 的架構與責任切分
  - 在 CR 前先用 AI 做 pre-review，找出明顯問題
  - 幫忙產生 review comment 草稿

- **Spec / Design / Doc**
  - 從 chat / 雜記整理出設計文件
  - 把設計文件轉成 task / ticket
  - 產生 API doc / usage example

- **Validation / Testing**
  - 產生 test cases（unit / integration / property-based）
  - 用自然語言描述行為，請 AI 轉成測試碼
  - 幫忙檢查 edge cases / failure modes

- **Dashboard / Monitoring / Oncall**
  - 解讀 dashboard 上的異常 pattern
  - 從多個 metric / log source 整合成 incident 敘事
  - 根據 runbook 提供下一步建議

- **溝通 / 協作**
  - 把技術細節轉成 PM / non-tech 聽得懂的版本
  - 產生 meeting note / summary / action items
  - 撰寫 RFC / 設計提案的初稿

- **個人學習 / 技術雷達**
  - 跟進新工具 / framework，產生「對我有什麼影響？」的摘要
  - 把散落的閱讀筆記整理成知識結構

## 待補充
- [ ] 把你實際一天的活動（從 calendar / log）對應到這份列表，補全遺漏的情境。
- [ ] 標記哪些情境在 Google 內部已有現成工具（例如特定 dashboard / internal bot）。