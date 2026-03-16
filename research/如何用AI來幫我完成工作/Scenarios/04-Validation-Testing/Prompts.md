# Prompts — Validation / Testing

## 1) 產生測試案例清單（unit/integration）
**Prompt**
```
你是測試工程師。根據以下需求/函式行為，產生測試案例。

需求/行為：
{{paste_spec_or_behavior}}

請輸出：
- Unit tests（至少 10 個，含 edge cases）
- Integration tests（至少 5 個，含失敗路徑）
- 每個 case：前置條件、輸入、期望輸出、為什麼重要
```

## 2) 自然語言 → 測試碼
**Prompt**
```
請把以下自然語言測試案例轉成可直接執行的測試碼。

語言/框架：{{language_and_framework}}（例如 Python+pytest / TS+jest）
系統介面：{{api_or_function_signatures}}
測試案例：
{{paste_cases}}

請輸出：
- 完整測試檔（含 setup/fixtures/mocks）
- 如需 mock 外部依賴，請明確指出 mock 行為
```

## 3) Edge cases / failure modes 掃描
**Prompt**
```
你是 adversarial tester。請針對以下功能做 failure-mode 分析。

功能描述：{{feature}}
輸入限制：{{constraints}}
程式碼（可選）：
{{paste_code}}

請輸出：
- 可能失敗模式清單（安全性、資料一致性、資源、並發、時間）
- 每個失敗模式對應的測試建議
- 需要新增的 observability（log/metric）
```
