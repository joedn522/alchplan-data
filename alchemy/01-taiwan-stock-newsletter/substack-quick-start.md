# Substack 註冊快速啟動單

> 這份檔案是 **「坐下來 5 分鐘執行完」** 的腳本。
> 從 `deep-thinking.md` §1.2、§2.2 抽出已決定的選項，免得你還要翻文件。
> 完成後在最下面打勾並提交，下個 cycle 我就會把 01 推進到 Phase 0。

---

## 🎯 30 秒版（C004 新增 — 推薦先做這個）

5 分鐘版你連跑 3 個 cycle 沒動。所以再砍小一半：

**你只要做一件事 — 拿出手機，打開 Just Press Record，講這句話：**

> 「Substack 的第一篇文章我想寫 ___。」
> （把空白填上你腦中第一個冒出來的台股題目，講完即可掛斷）

10–30 秒結束。Voice Daemon 會自動轉錄進 `bujo/voice-inbox/`，
下個 cycle 我（Alchemy）讀到後會：
1. 把這個主題寫進 `deep-thinking.md §3`
2. 幫你產出第一篇文章大綱（你不用註冊 Substack 也能先有內容）

**註冊 Substack 這件事先暫停**。先有題目，再找平台。順序倒過來。

如果你連 30 秒語音都沒講，下個 cycle 我會把 01 標為 `dormant`，停止追進度，等你主動回來。

---

## Step 1 — 開 Substack（30 秒）

1. 開瀏覽器 → https://substack.com
2. 右上 `Get started` → 用 Google 帳號登入
3. 出現「Create a publication」表單

## Step 2 — 填表單（90 秒）

| 欄位 | 直接填 |
|------|--------|
| Publication name | `台股數據實驗室 by WSL FinLab` |
| Subdomain (URL) | `wsl-twstock` |
| Topics | `Finance`、`Investing`、`Data Science` |
| Logo / Banner | **跳過**（按 Skip / Next） |

> 名稱出處：deep-thinking.md §1.2 推薦方案 D
> URL 出處：deep-thinking.md §1.2 推薦方案 D

## Step 3 — About 頁面（2 分鐘）

進入 Dashboard → Settings → About →「Description」欄位，**整段貼下面**：

```
嗨，我是 Asher，前 Amazon / Microsoft / Google 軟體工程師。

我花了數年時間打造了一個 AI 台股交易研究平台（wslfinlab.asherdom.me），
過程中發現：投顧老師說的很多「鐵則」，數據驗證後根本站不住腳。

這份電子報每週做一個數據實驗：
- 「法人連續買超 N 天，股票真的會漲嗎？」
- 「KD 黃金交叉的勝率到底多少？」
- 「營收創新高的股票，買進後的報酬率分布長怎樣？」

不賣明牌，不預測大盤。
只用數據說話，實驗結果好壞都公開。

免費訂閱：每週收到實驗報告摘要
付費訂閱：完整數據表格、進階實驗、方法論深度解析
```

Save。

## Step 4 — 全部跳過清單（不要做）

這次 **不要** 碰以下：
- Logo 上傳 → 之後再說
- Banner 上傳 → 之後再說
- Welcome email → 之後再說
- 自訂域名 → 之後再說
- 邀請 import contacts → **絕對跳過**（避免騷擾）
- 第一篇文章 → 下個 cycle 才碰

## Step 5 — 完成標記（30 秒）

在這份檔案最下面 `[ ]` 改成 `[x]` 並填日期 + URL，然後：

```bash
git add alchemy/01-taiwan-stock-newsletter/substack-quick-start.md
git commit -m "alchemy/01: Substack 帳號上線"
git push
```

---

## 完成回報區

- [ ] 2026-__-__：Substack 帳號已建立，URL = `https://wsl-twstock.substack.com`
- [ ] About 頁面已填
- [ ] 下個 cycle 等 Alchemy 部長把 01 推進到 Phase 0（看 deep-thinking.md §3：第一篇主題）

---

*產生於 cycle 20260511_C003 — Alchemy 幫你預備好的零摩擦腳本*
