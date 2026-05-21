# Stack / Queue — Python 對應

Python 內建沒有專門的 Stack/Queue 類別，但有幾種資料結構可以對應。

---

## 1. list（當 Stack 用）

```python
st = []
st.append(1)   # push
st.pop()       # pop（從尾巴移除）
st[-1]         # top（看最上面）
not st         # empty check
len(st)        # size
```

`append` 和 `pop` 都是 O(1)，面試用 list 當 stack 完全沒問題。

---

## 2. collections.deque（當 Queue 或 Deque 用）

list 當 queue 用很慢（`pop(0)` 是 O(n)），要用 `deque`：

```python
from collections import deque

dq = deque()
dq.append(1)      # 從右邊加（enqueue）
dq.appendleft(1)  # 從左邊加
dq.pop()          # 從右邊移除
dq.popleft()      # 從左邊移除（dequeue），O(1)
dq[0]             # 看最左邊
dq[-1]            # 看最右邊
```

左右兩端操作都是 O(1)，**BFS 幾乎都用這個**。

---

## 3. heapq（當 Priority Queue / Min Heap 用）

```python
import heapq

h = []
heapq.heappush(h, 3)   # push
heapq.heappush(h, 1)
heapq.heappop(h)        # pop 最小值，回傳 1
h[0]                    # 看最小值但不移除
```

Python heapq 預設是 **min heap**。要 max heap 就把值取負號存進去。

---

## C++ vs Python 對照

| C++ | Python |
|-----|--------|
| `stack` | `list` |
| `queue` | `collections.deque` |
| `deque` | `collections.deque` |
| `priority_queue` | `heapq` |
| `set` | `set` |
| `map` | `dict` |
| `unordered_map` | `dict` |

---

## 刷題速記

- **Stack** → `list`
- **Queue / BFS** → `deque`
- **Priority Queue** → `heapq`

這三個記住就夠應付大多數題目。
