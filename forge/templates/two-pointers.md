# Two Pointers

> **規則**：`while left < right` · 移動「不可能讓答案更好的那個」
> **心法**：對撞指針從兩端夾；同向指針一快一慢
> **典型題**：LC 11 · LC 15 · LC 42 · LC 26 · LC 125

---

## 兩種模式

| 模式 | 初始 | 場景 |
|---|---|---|
| **對撞（Opposite）** | `left=0, right=n-1` | 有序陣列、容器問題 |
| **同向（Fast-Slow）** | `slow=0, fast=0/1` | 移除重複、cycle 偵測 |

---

## 對撞指針框架

```python
def two_pointers(nums: list):
    left, right = 0, len(nums) - 1
    result = 0

    while left < right:           # 不是 <=
        current = compute(left, right)
        result = max(result, current)

        # greedy：移動「不可能讓答案更大」的那邊
        if nums[left] < nums[right]:
            left += 1
        else:
            right -= 1            # 相等時移哪邊都可以

    return result
```

**為什麼移較小的？（LC 11 的 greedy proof）**
容積 = min(height[L], height[R]) × (R-L)。寬度每次縮 1，唯一可能增加容積的方式是換一個更高的柱子。移較高的那邊只會讓 min 更小或持平，一定不更好；移較小的才有機會找到更高的替代。

---

## 同向指針框架（去重 / 條件過濾）

```python
def remove_duplicates(nums: list) -> int:
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != nums[slow]:    # 條件：值不同才保留
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

---

## 3Sum 特殊處理（LC 15）— duplicate 跳法

```python
def threeSum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]: continue   # 外層跳重複
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]: left += 1   # 內層跳重複
                while left < right and nums[right] == nums[right-1]: right -= 1
                left += 1; right -= 1
            elif s < 0: left += 1
            else: right -= 1
    return result
```

---

## 更新記錄
- 2026-05-17：初始版本
