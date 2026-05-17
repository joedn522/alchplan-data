# Sliding Window

> **規則**：`for right` 擴張 · `while 違反` 縮左 · window 用 `dict`
> **心法**：right 是外層 for，left 是內層 while — 不要反過來
> **典型題**：LC 3 · LC 76 · LC 424 · LC 239 · LC 643

---

## 兩種 Window

| 類型 | 場景 | 框架 |
|---|---|---|
| **可變長度** | 最長 / 最短 / 滿足條件的 subarray | `for right` + `while left` |
| **固定長度** | 大小為 k 的 window | 單 `for`，進一出一 |

---

## 可變長度框架（最常用）

```python
def sliding_window(s: str) -> int:
    window = {}          # 用 dict，不用 Counter（少一個 import）
    left = 0
    result = 0

    for right in range(len(s)):
        # 1. 擴張：把 s[right] 加進 window
        c = s[right]
        window[c] = window.get(c, 0) + 1

        # 2. 縮小：違反條件時從左收縮
        while [window 違反條件]:
            d = s[left]
            window[d] -= 1
            if window[d] == 0:
                del window[d]
            left += 1

        # 3. 更新結果（縮完之後才更新）
        result = max(result, right - left + 1)

    return result
```

**違反條件怎麼寫：**
- LC 3（無重複）：`while window[c] > 1`
- LC 76（最小包含視窗）：`while formed == required`（條件滿足時縮，找更小的）
- LC 424（最長替換後無重複）：`while (right - left + 1) - max(window.values()) > k`

---

## 固定長度框架

```python
def fixed_window(nums: list, k: int) -> int:
    window_sum = sum(nums[:k])
    result = window_sum

    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]   # 進一出一
        result = max(result, window_sum)

    return result
```

---

## 常見坑

1. **`while` 還是 `if` 縮小？** 可變長度永遠用 `while`，因為可能要縮多次
2. **結果更新時機** 找「最長」→ 每次 for 都更新；找「最短」→ 只在 while 裡更新
3. **window 清空策略** `del window[d]` 要在 `window[d] == 0` 才刪，否則 `get` 會出問題

---

## 更新記錄
- 2026-05-17：初始版本
