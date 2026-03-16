# Prompts — Dashboard / Monitoring / Oncall

## 1) 讀 dashboard 異常 pattern → 假說與下一步
**Prompt**
```
你是 oncall lead。以下是 dashboard/指標摘要：
{{paste_metrics_summary}}

事件背景：{{context}}

請輸出：
- 你注意到的異常訊號（與基線比較）
- 3 個根因假說（每個都列：支持/反駁要看什麼）
- 立刻要做的 5 個檢查（按優先順序）
- 可能的緩解手段（低風險先）
```

## 2) 多來源（metric/log/trace）整合成 incident 敘事
**Prompt**
```
請把以下資料整合成一份 incident timeline + summary。

資料：
- Metrics：{{paste_metrics}}
- Logs：{{paste_logs}}
- Traces：{{paste_traces}}
- 變更/部署：{{deploy_info}}

輸出：
1) Timeline（含時間、觀察、推論）
2) Customer impact（量化）
3) Root cause（若未定則列 top suspects）
4) Mitigation steps taken
5) Follow-ups（prevent recurrence）
```

## 3) 根據 runbook 推下一步（但要先檢查前提）
**Prompt**
```
你是 runbook executor。請根據 runbook 給出下一步，但務必先列出必要前提與風險。

Runbook：
{{paste_runbook}}

現況：
{{paste_current_state}}

輸出：
- Preconditions（我需要先確認什麼）
- Next steps（每一步：指令/操作、預期結果、失敗怎麼辦）
- Stop conditions（什麼情況要升級/停止）
```
