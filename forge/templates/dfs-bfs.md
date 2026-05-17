# DFS / BFS

> **DFS 規則**：base case → 遞迴左右 → combine（後序框架最萬用）
> **BFS 規則**：`deque` + `popleft` · level 用 `len(queue)` snapshot
> **典型題**：LC 104 · LC 543 · LC 124 · LC 102 · LC 127 · LC 200

---

## DFS — 二叉樹（後序框架）

```python
def dfs(node):
    # 1. base case
    if not node:
        return BASE_VALUE          # 0 / False / float('-inf') 視題目

    # 2. 遞迴
    left  = dfs(node.left)
    right = dfs(node.right)

    # 3. combine（用 left、right、node.val 計算結果）
    return COMBINE(left, right, node.val)
```

**前/中/後序選哪個？**
- **後序（最常用）**：需要子樹結果才能算自己（LC 124 Path Sum, LC 543 Diameter）
- **前序**：需要把父節點資訊傳給子節點（LC 257 路徑字串）
- **中序**：BST 相關（中序 = 升序）

---

## DFS — 圖（有向 / 無向，防 cycle）

```python
def dfs_graph(node, visited: set):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_graph(neighbor, visited)
```

---

## BFS — Level Order（LC 102）

```python
from collections import deque

def bfs_level(root):
    if not root: return []
    queue = deque([root])
    result = []

    while queue:
        level_size = len(queue)        # ← snapshot 當層大小，重要！
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)

    return result
```

---

## BFS — 最短路徑（LC 127 Word Ladder, LC 200 Island）

```python
def bfs_shortest(start, end, graph: dict) -> int:
    queue = deque([(start, 0)])        # (node, distance)
    visited = {start}

    while queue:
        node, dist = queue.popleft()
        if node == end: return dist
        for nbr in graph.get(node, []):
            if nbr not in visited:
                visited.add(nbr)
                queue.append((nbr, dist + 1))

    return -1
```

---

## DFS vs BFS 選哪個？

| 場景 | 選擇 |
|---|---|
| 找最短路徑 | BFS（層數 = 距離）|
| 需要路徑本身 / 所有解 | DFS（+ backtracking）|
| 樹的遍歷、計算子樹結果 | DFS |
| Level-order / 按層處理 | BFS |

---

## 更新記錄
- 2026-05-17：初始版本，DFS 後序 + BFS level/shortest
