# Binary Search — Find First True

> **規則**：`while lo < hi` · `True→hi=mid` · `False→lo=mid+1` · `return lo`
> **心法**：所有 BS 題都是「找第一個讓 condition 為 True 的位置」
> **典型題**：LC 704 · LC 153 · LC 33 · LC 35 · LC 875

---

## 四條規則（背熟）

```
① while lo < hi              ← 不是 <=
② mid = lo + (hi - lo) // 2  ← 向下取整（往左偏）
③ condition True  → hi = mid ← 答案可能是 mid 或更左
   condition False → lo = mid+1 ← 答案一定在 mid 右邊
④ return lo                  ← lo == hi 就是答案
```

**hi 初始值：**
- 答案一定在陣列裡 → `hi = len(nums) - 1`
- 答案可能是末端之後（insert）→ `hi = len(nums)`
- 答案是數值範圍（answer space）→ `hi = max_possible`

---

## 通用框架

```python
def bs(lo: int, hi: int, condition) -> int:
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if condition(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

---

## 五大題型套法

### 1. 找 exact target（LC 704）
```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    lo = bs(lo, hi, lambda i: nums[i] >= target)
    return lo if nums[lo] == target else -1
```

### 2. 找旋轉陣列最小值（LC 153）
```python
def findMin(nums):
    # condition: nums[mid] <= nums[-1] (在右半段，含最小值)
    return nums[bs(0, len(nums) - 1, lambda i: nums[i] <= nums[-1])]
```

### 3. 旋轉陣列找 target（LC 33）⚠️ 手寫，不套框架
```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target: return mid
        if nums[lo] <= nums[mid]:         # 左半有序
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                              # 右半有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return lo if nums[lo] == target else -1
```

### 4. 插入位置 / left bound（LC 35）
```python
def searchInsert(nums, target):
    # condition: nums[i] >= target
    return bs(0, len(nums), lambda i: i == len(nums) or nums[i] >= target)
```

### 5. Answer Space（LC 875 Koko, LC 1011 Capacity）
```python
def minEatingSpeed(piles, h):
    import math
    def feasible(speed):
        return sum(math.ceil(p / speed) for p in piles) <= h
    return bs(1, max(piles), feasible)
```

---

## 更新記錄
- 2026-05-17：初始版本，採用「Find First True」統一框架
