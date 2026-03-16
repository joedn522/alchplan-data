# Happy Coder（slopus/happy）部署到 Windows WSL2 的手冊（含手機連線疑難排解）

> 目標：在 Windows 的 WSL2 裡跑 `happy`（Happy Coder CLI），手機 App 能掃到 QR、也能正常「送出訊息/接管 session」。
>
> Repo: https://github.com/slopus/happy

---

## TL;DR（你現在遇到的症狀最像什麼）
你描述的狀況是：
- `happy` 啟動時手機掃得到 QR、能連上
- 但手機一送訊息就壞掉

這種狀況**很常見於 WSL2 的 inbound network 限制**：
- WSL2 預設是 NAT；**手機在同一個 Wi‑Fi LAN 上，通常「打不到」WSL 的服務 port**
- 掃 QR 成功 ≠ 後續所有連線都通（有些流程可能走不同 host/port/WebSocket）

所以手冊會提供 **3 條部署路徑**（從最少改動到最穩）：
1) **建議**：把 `happy` 跑在 Windows（host）上，但工作目錄對到 WSL repo
2) `happy` 跑在 WSL2，但用 **WSL mirrored networking（Win11）** 或 **portproxy** 打通 inbound
3) 若你其實卡在「Happy Server 不穩/自架」：加上自架 `happy-server`（可選）

---

## 0) 先確認你是在用哪一種模式
請你先在 WSL 裡跑：

```bash
happy --version
which happy || command -v happy
node -v
npm -v
```

以及在手機 Happy App 裡確認：
- 你是登入官方 server（預設）？
- 還是有填自訂 server URL？（Settings 右上角 Database / Server 類似入口）

> 若你沒有自訂 server，理論上不用先搞自架 server，先把 WSL 網路打通通常就能解。

---

## 路徑 A（最推薦）：`happy` 跑在 Windows Host，repo 仍在 WSL
### 為什麼推薦
Windows host 對 LAN inbound 沒有 WSL NAT 那層麻煩：手機打到你的 Windows IP:port 通常就通。

### 步驟
1. 在 **Windows（PowerShell）** 安裝 Node.js（建議 20+）
2. 安裝 Happy CLI：

```powershell
npm install -g happy-coder
happy --help
```

3. 讓 `happy` 在 WSL repo 上工作（兩種做法擇一）

- 作法 A：從 Windows 直接進 WSL 路徑（\\wsl$）
  - 在檔案總管輸入：`\\wsl$\<你的distro>\home\<user>\finlab-v2`
  - 在該資料夾開 Windows Terminal，跑 `happy`

- 作法 B：在 Windows terminal 直接用 `wsl.exe` 切換工作目錄

```powershell
wsl -d <你的distro> -- bash -lc "cd ~/finlab-v2 && pwd"
```

> 注意：Happy 會包一層 wrapper 來啟動 Claude Code/Codex；你要確保實際 agent 執行時看到的是你要的 repo 路徑。

4. 用手機掃 `happy login` / `happy` 產生的 QR code 測試

### 驗收
- 手機接管後送訊息，Windows terminal 有即時反應
- 不會卡在 send / pending

---

## 路徑 B：`happy` 跑在 WSL2，但打通「手機 → WSL」的 inbound

### B1) Windows 11 建議解：WSL mirrored networking
如果你是 Windows 11（新版 WSL），優先用 mirrored networking，體驗最好。

1. 在 Windows 使用者目錄建立/編輯：`%UserProfile%\.wslconfig`
2. 加上：

```ini
[wsl2]
networkingMode=mirrored
# 可選：讓 localhost 更一致
# localhostForwarding=true
```

3. 重新啟動 WSL：

```powershell
wsl --shutdown
```

4. 回到 WSL 重開，跑 `happy` 再用手機測

> mirrored 的核心好處：WSL 的服務更像直接綁在 Windows 網卡上，LAN 裝置比較容易打到。

### B2) 通用解：Windows portproxy 把 Windows port 轉發到 WSL
如果你不方便用 mirrored，或版本不支援，就用 portproxy。

#### 1) 先找 WSL IP
在 WSL：

```bash
ip addr | grep -n "inet "
# 通常會看到 eth0 的 172.x.x.x
```

假設 WSL IP = `172.25.10.55`

#### 2) 找出 happy 需要被手機打到的 port
這步最關鍵：你要先知道 `happy`（或它啟動的 daemon）實際聽在哪個 port。

做法：
- 先跑 `happy`，讓它顯示 QR
- 觀察 QR/連線資訊（通常會包含 host:port）
- 或在 WSL 開另一個 shell 查 listening ports：

```bash
# 需要的話先安裝：sudo apt-get update && sudo apt-get install -y net-tools
sudo netstat -tulpn | head
sudo netstat -tulpn | grep LISTEN
```

> 在 repo 裡可以看到一些預設 port：
> - Claude/Gemini OAuth callback default `54545`
> - Codex auth default `1455`
> 但「手機接管」不一定只靠這些 port，所以要以你實際 listen 為準。

#### 3) 用 portproxy 轉發
在 Windows（系統管理員 PowerShell）：

```powershell
# 例：把 Windows 的 54545 轉發到 WSL 的 54545
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=54545 connectaddress=172.25.10.55 connectport=54545

# 查看
netsh interface portproxy show all
```

#### 4) 開防火牆
Windows 防火牆要放行你 listen 的 port（例：54545）。

#### 5) 再用手機測

---

## 路徑 C（可選）：自架 Happy Server（解「官方 server 不穩/或你想全自管」）
> 你目前描述比較像 WSL inbound 問題；但如果你想自架，我也把最短路徑放這。

Happy 官方 server 預設是 `happy-api.slopus.com`；自架可以用 repo 內的 `packages/happy-server`。

### C1) 在 WSL 用 Docker 跑 happy-server（standalone）
1. 在 Windows 安裝 Docker Desktop，並啟用 WSL integration
2. 在 WSL clone repo（或用你已經有的 checkout）
3. build image（在 monorepo root）：

```bash
docker build -t happy-server -f packages/happy-server/Dockerfile .
```

4. 跑起來：

```bash
docker run -p 3005:3005 \
  -e HANDY_MASTER_SECRET=<your-secret> \
  -e PUBLIC_URL=http://<YOUR_WINDOWS_IP>:3005 \
  -v happy-data:/data \
  happy-server
```

> iOS 可能會擋純 HTTP（取決於 App 設定/ATS）；最穩是搭配 **Tailscale Serve** 或反向代理上 HTTPS。

### C2) iOS 建議：Tailscale Serve 提供 HTTPS（超省事）
參考（外部文章）：Tony Dehnke 2026-01-04（happy-server-light + tailscale serve）。

概念：
- Windows 裝 Tailscale
- 讓 Tailscale Serve 把 `http://localhost:3005` 變成 `https://<machine>.<tailnet>.ts.net`

---

## Troubleshooting Checklist（你現在「送訊息就壞」最該檢查）
1) 手機跟 Windows 是否在同一個網段？（同 Wi‑Fi）
2) QR code 裡的 host 是什麼？是 `172.x`（WSL NAT）還是 `192.168.x`（LAN）？
   - 若是 `172.x`：手機大機率打不到 → 走路徑 A 或 B
3) 你是否使用公司 Wi‑Fi / AP isolation？（同網段設備互相不可見）
4) Windows 防火牆是否擋住 inbound port？
5) `happy` 有沒有顯示 WebSocket 連線錯誤？（如果有，把錯誤貼我，我可以對症）

---

## 我需要你提供 3 個資訊，我可以把這份手冊「完全對準你的環境」
1) 你 Windows 版本（10/11）與 WSL 版本（`wsl --version`）
2) 你跑 `happy` 的那一刻，WSL 裡 `netstat -tulpn | grep LISTEN` 的結果（或至少跟 happy 相關的 port）
3) 手機掃 QR 後送訊息，終端機/手機畫面上的錯誤訊息（截圖或文字）
