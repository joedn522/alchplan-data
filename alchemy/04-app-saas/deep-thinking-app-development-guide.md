# iPhone App 開發與上架完整指南 + App 賺錢策略

> 最後更新：2026-03-15（v2：新增後端架構、API key 管理、OpenClaw 策略轉向）
> 目標讀者：有豐富軟體工程經驗、但從未上架過 iOS App 的開發者
> 第一個 App 目標：語音子彈筆記（Voice Bullet Journal）

---

## 目錄

1. [iOS App 上架完整流程](#1-ios-app-上架完整流程)
2. [技術選型建議](#2-技術選型建議)
3. [App 營利模式完整分析](#3-app-營利模式完整分析)
4. [金流與法律](#4-金流與法律)
5. [語音子彈筆記 App 的具體規劃](#5-語音子彈筆記-app-的具體規劃)
6. [App 推廣策略](#6-app-推廣策略)
7. [其他 App 點子的評估框架](#7-其他-app-點子的評估框架)
8. [時程規劃](#8-時程規劃)
9. [後端架構與 API Key 管理](#9-後端架構與-api-key-管理)
10. [OpenClaw Skill 的定位（行銷工具，非產品）](#10-openclaw-skill-的定位)
11. [市場分析：為什麼 App Store 還沒被 AI App 攻佔](#11-市場分析為什麼-app-store-還沒被-ai-app-攻佔)
12. [防濫用機制](#12-防濫用機制)
13. [平滑服務用戶的完整體驗設計](#13-平滑服務用戶的完整體驗設計)

---

## 1. iOS App 上架完整流程

### 1.1 前置準備

| 項目 | 說明 |
|------|------|
| Mac 電腦 | 必須。Xcode 只能在 macOS 上執行。你有 macOS 設備，OK |
| Apple ID | 用個人 Apple ID 即可，之後升級為開發者帳號 |
| iPhone/iPad | 用於真機測試。模擬器可以跑大部分功能，但語音相關功能必須真機 |

### 1.2 Apple Developer Program 註冊

**Step 1：確認 Apple ID 已啟用雙重認證**
- 設定 → Apple ID → 密碼與安全性 → 雙重認證：開啟

**Step 2：前往 [developer.apple.com/programs](https://developer.apple.com/programs)**
- 點選「Enroll」
- 選擇身份類型：

| 類型 | 年費 | 適用情境 | 需要 D-U-N-S 嗎？ |
|------|------|----------|-------------------|
| **Individual（個人）** | USD $99/年 | 個人開發者、side project | 不需要 |
| **Organization（組織）** | USD $99/年 | 有公司/團隊 | 需要 D-U-N-S Number |

> **建議：先用 Individual 開始。** 之後要改成公司很容易，不需要重新申請。

**Step 3：完成付款**
- 信用卡或 Apple ID 餘額皆可
- 付款後約 24-48 小時內審核通過（個人帳號通常很快）

**Step 4：審核通過後**
- 你會收到 email 確認
- 登入 [developer.apple.com](https://developer.apple.com) 確認 Membership 狀態為 Active
- 現在可以存取：App Store Connect、Certificates、Provisioning Profiles

### 1.3 Xcode 專案設定（從零開始）

**Step 1：安裝 Xcode**
```
# 從 Mac App Store 安裝，或用 xcode-select
xcode-select --install
```
- Xcode 檔案很大（約 12GB），下載需要時間
- 安裝後第一次開啟會要求安裝額外 components，全部同意

**Step 2：建立新專案**
1. 開啟 Xcode → File → New → Project
2. 選擇 iOS → App
3. 填寫：
   - **Product Name**：`VoiceBulletJournal`（或你的 App 名稱）
   - **Team**：選擇你的 Apple Developer 帳號
   - **Organization Identifier**：`com.yourname`（例如 `com.ashershih`）
   - **Bundle Identifier**：會自動組合成 `com.ashershih.VoiceBulletJournal`
   - **Interface**：選 SwiftUI
   - **Language**：Swift
   - **Storage**：None（之後再加）
4. 選擇存放位置，Create

**Step 3：設定 Signing & Capabilities**
1. 點選專案 Navigator 中的專案名稱
2. 選 Targets → 你的 App
3. Signing & Capabilities：
   - ✅ Automatically manage signing
   - Team：選你的 Developer 帳號
   - Bundle Identifier：確認正確
4. Xcode 會自動建立 Provisioning Profile 和 Signing Certificate

**Step 4：加入必要的 Capabilities**
- 在 Signing & Capabilities 中點 「+ Capability」
- 語音子彈筆記需要的：
  - **Speech Recognition**（語音辨識）
  - **Microphone**（麥克風）
  - **Push Notifications**（如果要推播）
  - **iCloud**（如果要雲端同步，選 CloudKit）

**Step 5：設定 Info.plist 權限說明**
```xml
<!-- 麥克風權限 -->
<key>NSMicrophoneUsageDescription</key>
<string>需要麥克風來錄製你的語音筆記</string>

<!-- 語音辨識權限 -->
<key>NSSpeechRecognitionUsageDescription</key>
<string>需要語音辨識來將你的語音轉換為文字</string>
```
> **注意：** 權限說明必須用「使用者能理解的語言」，不能寫技術術語。審核會因為這個被拒。

**Step 6：真機測試**
1. 用 USB 線連接 iPhone
2. iPhone 上信任此電腦
3. Xcode 左上角選擇你的 iPhone 作為目標裝置
4. 按 ▶️ Run
5. 第一次在 iPhone 上需要：設定 → 一般 → VPN與裝置管理 → 信任開發者

### 1.4 App Store Connect 設定

**Step 1：登入 [appstoreconnect.apple.com](https://appstoreconnect.apple.com)**

**Step 2：建立新 App**
1. 我的 App → ＋ → 新 App
2. 填寫：

| 欄位 | 說明 | 範例 |
|------|------|------|
| 平台 | 勾選 iOS | ✅ iOS |
| 名稱 | App Store 上顯示的名稱（30 字元內，全球唯一） | Voice Bullet Journal |
| 主要語言 | App 的主要語言 | 繁體中文 或 English |
| Bundle ID | 必須與 Xcode 中的一致 | com.ashershih.VoiceBulletJournal |
| SKU | 內部管理用，不會公開 | voicebulletjournal001 |
| 使用者存取權限 | 完整存取 | 完整存取 |

**Step 3：填寫 App 資訊**

必填項目 checklist：
- [ ] **App 預覽和截圖**（最重要！）
  - 需要：6.7 吋（iPhone 15 Pro Max）、6.5 吋（iPhone 14 Plus）、5.5 吋截圖
  - iPad 如果支援也要提供
  - 每個尺寸最少 1 張，最多 10 張
  - 建議用 Figma 做精美的行銷截圖，不要直接用 raw screenshot
  - 尺寸：6.7" = 1290 x 2796 px
- [ ] **描述**：4000 字元以內，前三行最重要（使用者看到的折疊前文字）
- [ ] **關鍵字**：100 字元以內，用逗號分隔，不要重複 App 名稱中已有的字
- [ ] **支援 URL**：必須提供一個網頁（可以是 GitHub Pages 的簡單頁面）
- [ ] **隱私權政策 URL**：**必填**，見第 4 章
- [ ] **年齡分級**：填寫問卷後自動產生
- [ ] **版權**：例如 `2026 Your Name`
- [ ] **App 圖示**：1024 x 1024 px，PNG，無透明度，無圓角（系統會自動加）
- [ ] **Build**：上傳的 binary（見下方）
- [ ] **定價**：在「定價和供應狀況」中設定

**Step 4：上傳 Build**

方法 A：從 Xcode 直接上傳
1. Xcode → Product → Archive
2. Archive 成功後，Organizer 視窗會自動開啟
3. 選擇剛建立的 Archive → Distribute App
4. 選擇 App Store Connect → Upload
5. 跟著步驟走（通常全部用預設值）
6. 上傳完成後，等待 15-30 分鐘的自動處理
7. 處理完成後，在 App Store Connect 的「Build」區段就能看到

方法 B：用 Command Line
```bash
# 先 Archive
xcodebuild -scheme VoiceBulletJournal -configuration Release archive -archivePath build/VoiceBulletJournal.xcarchive

# 再 Export
xcodebuild -exportArchive -archivePath build/VoiceBulletJournal.xcarchive -exportPath build/export -exportOptionsPlist ExportOptions.plist

# 上傳
xcrun altool --upload-app -f build/export/VoiceBulletJournal.ipa -u your@email.com -p app-specific-password
```

### 1.5 提交審核

**提交前 Checklist：**
- [ ] 所有必填欄位都已填寫
- [ ] 截圖已上傳（所有要求的尺寸）
- [ ] Build 已上傳且處理完畢（狀態顯示為可選擇）
- [ ] 已選擇 Build
- [ ] 定價已設定
- [ ] 隱私權政策 URL 可正常存取
- [ ] 如果有登入功能：提供 Demo 帳號密碼給審核人員
- [ ] App 不能有明顯 crash 或 placeholder 內容

**提交步驟：**
1. 在版本頁面點選「提交以供審核」
2. 回答幾個問題：
   - 是否使用 IDFA（廣告追蹤）？→ 通常選「否」
   - 是否使用加密？→ 如果用 HTTPS（幾乎都會），選「是」，但符合豁免條件
   - 內容版權？→ 確認擁有所有內容的版權

**審核時間：**
- 通常 24-48 小時（2026 年的經驗）
- 第一次送審可能會比較慢
- 快的時候 6 小時內就通過

### 1.6 常見被拒原因與解法

| 拒絕原因 | 說明 | 解法 |
|----------|------|------|
| **Guideline 2.1 - Performance: App Completeness** | App 有 crash、有 placeholder 內容、功能不完整 | 確保所有功能可用，移除所有 TODO/placeholder |
| **Guideline 2.3.3 - Accurate Metadata** | 截圖與實際 App 不符 | 用真實 App 截圖 |
| **Guideline 3.1.1 - IAP Required** | 數位內容未使用 IAP 購買 | 數位內容必須走 IAP（見第 4 章） |
| **Guideline 4.0 - Design** | UI 太簡陋、使用者體驗差 | 確保基本的 UI 品質 |
| **Guideline 5.1.1 - Privacy** | 隱私權政策缺失或不完整 | 提供完整的隱私權政策 |
| **Guideline 5.1.2 - Data Use and Sharing** | 未正確宣告資料使用 | 在 App Store Connect 填寫完整的隱私權營養標籤 |
| **Login Required without Demo Account** | 需要登入但沒給審核帳號 | 在「App Review Information」中提供測試帳號 |

> **Pro Tip：** 如果被拒，不要慌。在 Resolution Center 回覆，說明你的修正方案。語氣禮貌、具體說明改了什麼。通常修正後重新提交 24 小時內會再審。

### 1.7 上架後的更新流程

1. 在 App Store Connect 中，點選已上架的 App
2. 左側選擇「+ 版本或平台」→ iOS
3. 輸入新的版本號（例如 1.1.0）
4. 填寫「此版本的新功能」（What's New）
5. 在 Xcode 中更新版本號和 Build 號
   - Version：1.1.0（給使用者看的）
   - Build：2（每次上傳遞增，給 Apple 看的）
6. 重新 Archive → Upload
7. 在 App Store Connect 選擇新 Build
8. 提交審核
9. 更新版本的審核通常比第一次快

---

## 2. 技術選型建議

### 2.1 三大選項比較

| | SwiftUI (Native) | React Native | Flutter |
|---|---|---|---|
| **語言** | Swift | JavaScript/TypeScript | Dart |
| **跨平台** | 僅 Apple 生態系（iOS/iPadOS/macOS/watchOS） | iOS + Android + Web | iOS + Android + Web + Desktop |
| **效能** | 最佳 | 好（有 bridge 開銷） | 很好（自己繪製 UI） |
| **語音 API 存取** | 原生支援，API 直接呼叫 | 需要 Native Module 或第三方套件 | 需要 Plugin |
| **開發速度** | 中（需學 Swift，但 SwiftUI 生產力高） | 快（如果已熟悉 React） | 中 |
| **App 大小** | 最小（~10MB） | 中（~30MB） | 中（~20MB） |
| **在 Windows 上開發** | ❌ 不行 | ✅ 可以（但 iOS build 仍需 Mac） | ✅ 可以（但 iOS build 仍需 Mac） |
| **Apple 審核** | 沒問題 | 沒問題（已被廣泛接受） | 沒問題 |
| **長期維護** | Apple 官方框架，最穩定 | Meta 維護，社群大 | Google 維護，成長快 |

### 2.2 具體建議

**對你的情況，推薦的策略是：Web App 先行 + 之後加 iOS Native**

理由：

**Phase 1：先做 Web App（PWA）**
- 可以在 Windows 上開發
- 不需要付 $99/年
- 可以快速驗證市場
- 技術棧：Next.js + Vercel
- 語音功能：Web Speech API（Chrome 支援最好）或串 OpenAI Whisper API
- 2 天可以做出 MVP

**Phase 2：如果驗證成功，做 iOS Native App**
- 用 SwiftUI（你是有經驗的工程師，學習成本不高）
- 原因：
  - 語音子彈筆記是「個人工具類」App，使用者期待原生體驗
  - 語音辨識用 Apple 內建的 Speech framework 品質最好、最省成本（免費、離線可用）
  - 背景錄音、Siri Shortcuts 整合、Widget 等功能只有 Native 能做好
  - 如果要做訂閱制，Native App 使用者付費意願更高

**不推薦 React Native / Flutter 的原因：**
- 你的 App 重度依賴語音 API，跨平台框架在這塊常有坑
- 你的主要市場應該先聚焦 iOS（iPhone 使用者付費意願遠高於 Android）
- 跨平台「省」下來的時間，會花在除 Native Module 的 bug 上
- 如果之後真的要 Android，那時候再評估（可能市場已經告訴你不需要）

### 2.3 後端架構

**極簡架構（推薦先用這個）：**

```
使用者 iPhone
    ↓
Apple Speech Framework（語音→文字，免費、離線）
    ↓
OpenAI API / Claude API（文字→結構化筆記）
    ↓
本地儲存（Core Data / SwiftData）
    ↓
（可選）iCloud 同步（免費、Apple 內建）
```

**優點：**
- 不需要自己架後端伺服器
- 不需要管理使用者帳號（用 Apple ID 的 iCloud 即可）
- 成本極低（只有 AI API 呼叫費用）
- 隱私友善（資料在使用者自己的 iCloud）

**成本估算：**
- OpenAI GPT-4o-mini：~$0.15 / 1M input tokens → 每次語音筆記大約 500 tokens → **每次約 $0.0001**
- 每天用 10 次 → 一個月 $0.03 / 使用者
- 1000 個活躍使用者 → **$30/月**

**如果需要更多後端功能（使用者帳號、跨裝置同步、分析等）：**

```
使用者 iPhone
    ↓
Supabase（PostgreSQL + Auth + Storage + Realtime）
    ↓
Edge Functions（或 Vercel Serverless）
    ↓
OpenAI / Claude API
```

| 後端選項 | 免費額度 | 優點 | 缺點 |
|----------|---------|------|------|
| **Supabase** | 50K MAU, 500MB DB | PostgreSQL、開源、功能全 | 要學 Supabase SDK |
| **Firebase** | 很慷慨 | Google 生態系、文件多 | NoSQL 不適合複雜查詢 |
| **自架 (AWS/GCP)** | 有 free tier | 完全控制 | 維護成本高 |

> **建議：** 先用 Local + iCloud 開始。等到需要社群功能、分析後台時才加後端。YAGNI（You Aren't Gonna Need It）。

### 2.4 開發工具推薦

| 工具 | 用途 | 說明 |
|------|------|------|
| **Xcode** | iOS 開發 | 必備 |
| **SF Symbols** | 圖示 | Apple 免費圖示庫，4000+ 圖示 |
| **Figma** | UI 設計、App Store 截圖 | 免費方案夠用 |
| **TestFlight** | Beta 測試 | Apple 官方，免費，最多 10000 測試者 |
| **RevenueCat** | 訂閱管理 | 簡化 IAP，免費到 $2500 MRR |
| **Cursor / Claude Code** | AI 輔助開發 | 加速開發 |

---

## 3. App 營利模式完整分析

### 3.1 三大模式比較

#### 模式 A：付費下載（Paid Upfront）

```
使用者付一次錢 → 永久使用
```

| 項目 | 說明 |
|------|------|
| 典型定價 | $0.99 ~ $9.99 |
| Apple 抽成 | 30%（Small Business Program 為 15%） |
| 優點 | 簡單、使用者預期清楚、不需要持續提供新功能的壓力 |
| 缺點 | 收入一次性、下載門檻高、很難累積、需要持續獲取新使用者 |
| 適合 | 工具類（計算機、相機濾鏡）、遊戲 |
| 不適合 | 有持續成本的服務（語音子彈筆記有 AI API 成本，不適合） |

#### 模式 B：免費 + 內購（Freemium + IAP）

```
免費下載 → 部分功能免費 → 進階功能付費解鎖
```

| 項目 | 說明 |
|------|------|
| 典型定價 | 免費 + $4.99~$29.99 一次性解鎖 |
| Apple 抽成 | 30%（Small Business Program 為 15%） |
| 優點 | 下載門檻低、使用者可以先體驗再決定 |
| 缺點 | 轉換率通常只有 2-5%、收入仍是一次性 |
| 適合 | 功能明確可分層的工具 |

#### 模式 C：訂閱制（Subscription）⭐ 推薦

```
免費下載 → 試用期（7天/1個月）→ 月繳或年繳
```

| 項目 | 說明 |
|------|------|
| 典型定價 | $2.99~$9.99/月 或 $19.99~$49.99/年 |
| Apple 抽成 | 第一年 30%（Small Business 15%）→ 續訂第二年起 15% |
| 優點 | **持續性收入（MRR）**、可覆蓋持續成本（AI API）、估值高 |
| 缺點 | 使用者對訂閱疲勞、需要持續提供價值、退訂率需管理 |
| 適合 | **有持續成本的服務、AI 功能的 App（你的情況）** |

### 3.2 Apple Small Business Program

**重要！一定要申請。**

| | 標準 | Small Business Program |
|---|---|---|
| 資格 | 所有開發者 | 前一年 App Store 營收 < $1M |
| 抽成 | 30% | **15%** |
| 訂閱續訂（>1年） | 15% | 15% |

**申請方式：**
1. 前往 [developer.apple.com/programs/small-business-program](https://developer.apple.com/programs/small-business-program)
2. 登入 Developer 帳號
3. 確認營收資格
4. 送出申請
5. 通常幾天內生效

> 以你的情況，第一年營收幾乎不可能超過 $1M，一定要申請。差別是 30% vs 15%，很大。

### 3.3 收入實際計算範例

以語音子彈筆記 App 為例，假設訂閱制：

| 方案 | 月費 | 年費 |
|------|------|------|
| Free | $0 | $0 |
| Pro | $3.99/月 | $29.99/年 |

**情境：上架 6 個月後有 500 付費使用者**

| | 月訂閱（假設 200 人） | 年訂閱（假設 300 人） |
|---|---|---|
| 月營收 | 200 × $3.99 = $798 | 300 × $29.99 / 12 = $750 |
| 合計月營收 | **$1,548** | |
| Apple 抽成（15%） | -$232 | |
| AI API 成本 | -$15（500 人 × $0.03） | |
| **淨月收入** | **~$1,300** | |

> 這是保守估計。如果 App 品質好、定位精準，500 付費使用者在 6 個月內是可以達到的。

### 3.4 台灣開發者的稅務注意事項

**Apple 端：**
- Apple 會代扣美國 withholding tax（預扣稅）
- **務必在 App Store Connect 中填寫 W-8BEN 表格**（非美國個人）
- 台灣與美國沒有稅務協定，預扣稅率為 30%
  - 但如果你是台灣稅務居民，App Store 收入屬於「權利金」，適用的稅率可能不同
  - **強烈建議諮詢台灣的會計師**，確認是否有方式降低預扣稅
- Apple 每月結算，付款到你指定的銀行帳戶（可以是台灣的銀行）

**台灣端：**
- App Store 收入屬於「海外所得」
- 個人：併入綜合所得稅申報
- 如果年營收超過一定金額，需要開立統一發票 → 這時可能需要設立公司或行號
- 營業稅：如果是 B2C 數位服務，Apple 已經在各國處理了 VAT/消費稅
- **小規模初期：以個人身份開始，不需要急著開公司**（見第 4 章）

**建議的報稅準備：**
1. 從第一天起記錄所有收入和支出
2. 保留 Apple 的付款報表（App Store Connect → 付款和財務報告）
3. 記錄 AI API 費用、Apple Developer 年費等可扣除支出
4. 年收入到一定程度（例如年營收 > 50 萬台幣）再考慮設立公司

---

## 4. 金流與法律

### 4.1 App Store 內購（IAP）運作機制

**什麼是 IAP？**
- In-App Purchase，使用者在 App 內付費
- Apple 處理所有金流：信用卡、Apple Pay、電信帳單代付
- 你不需要碰任何金流 → **不用串信用卡、不用擔心 PCI DSS、不會有金流相關官司**

**IAP 類型：**

| 類型 | 說明 | 範例 | 適用場景 |
|------|------|------|----------|
| **Consumable（消耗型）** | 用完就沒了，可重複購買 | AI 使用次數、代幣 | 按量計費 |
| **Non-Consumable（非消耗型）** | 永久解鎖 | Pro 版本解鎖 | 一次性付費 |
| **Auto-Renewable Subscription（自動續訂）** | 定期自動扣款 | 月訂閱、年訂閱 | 訂閱制（推薦） |
| **Non-Renewing Subscription** | 不自動續訂 | 季節通行證 | 較少用 |

**實作流程（概述）：**

1. **App Store Connect 設定：**
   - App → 內購項目與訂閱 → 新增
   - 設定產品 ID（例如 `com.ashershih.vbj.pro.monthly`）
   - 設定價格（Apple 提供價格等級表，各國自動換算）
   - 填寫顯示名稱和描述

2. **程式碼實作：**
```swift
// 使用 StoreKit 2 (推薦，比 StoreKit 1 簡單很多)
import StoreKit

// 取得產品資訊
let products = try await Product.products(for: ["com.ashershih.vbj.pro.monthly"])

// 購買
let result = try await product.purchase()

// 驗證
switch result {
case .success(let verification):
    let transaction = try checkVerified(verification)
    // 解鎖功能
    await transaction.finish()
case .userCancelled:
    break
case .pending:
    break
}

// 檢查訂閱狀態
for await result in Transaction.currentEntitlements {
    // 使用者目前有效的訂閱/購買
}
```

3. **或者用 RevenueCat（推薦）：**
```swift
// RevenueCat 大幅簡化 IAP
import RevenueCat

Purchases.configure(withAPIKey: "your_api_key")

// 取得產品
let offerings = try await Purchases.shared.offerings()

// 購買
let result = try await Purchases.shared.purchase(package: package)

// 檢查權限
let customerInfo = try await Purchases.shared.customerInfo()
if customerInfo.entitlements["pro"]?.isActive == true {
    // Pro 使用者
}
```

> **強烈推薦 RevenueCat：** 免費到 $2,500 MRR，處理所有 IAP 的 edge case（退款、家庭共享、促銷優惠、Grace Period 等），還有很好的 Dashboard 看數據。

### 4.2 什麼時候可以不用 IAP？

**Apple 的規則很明確：**

| 情境 | 是否必須 IAP | 說明 |
|------|-------------|------|
| App 內購買數位內容/功能 | ✅ 必須 | 訂閱、解鎖功能、虛擬貨幣 |
| 實體商品或服務 | ❌ 不需要 | Uber、Airbnb、電商 |
| App 外已購買的內容 | ❌ 不需要 | Netflix 在網頁訂閱後在 App 觀看 |
| Reader App（閱讀器） | 可以外連 | 2022 年後可以放外部連結 |
| 一對一服務 | ❌ 不需要 | 線上諮詢、教練 |

**對語音子彈筆記 App：**
- 訂閱解鎖 Pro 功能 → **必須用 IAP**
- 你不需要自己串 Stripe 或任何金流
- **這其實是好事：** Apple 處理所有金流問題，你不碰錢，不會有官司

**如果你同時有 Web App：**
- Web App 上可以用 Stripe 收費
- iOS App 上必須用 IAP
- 使用者在 Web 付費後，可以在 iOS App 登入使用（但不能在 iOS App 內引導使用者去 Web 付費）
- 建議用 RevenueCat 統一管理跨平台訂閱狀態

### 4.3 台灣個人開發者的法律身份

**Q：需要開公司嗎？**

**A：初期不需要。** 以下是各階段建議：

| 階段 | 月營收 | 建議身份 | 原因 |
|------|--------|---------|------|
| 起步 | < $500 | 個人 | Apple Developer 用 Individual 就好，稅務簡單 |
| 成長 | $500 ~ $5,000 | 考慮設立行號 | 可以報營業支出抵稅 |
| 規模化 | > $5,000 | 設立有限公司 | 有限責任保護、稅務規劃空間大 |

**個人開發的法律風險：**
- 用 IAP → Apple 處理金流 → 金流糾紛風險極低
- 主要風險在：使用者資料隱私（需要隱私權政策）
- 以你的 App 類型（工具類、筆記類），法律風險非常低

**如果之後要設立公司：**
- 台灣：有限公司最低資本額無限制（但建議至少 10 萬台幣）
- 設立費用：約 5,000 ~ 15,000 台幣（含會計師代辦）
- 地點：可以設在家裡（住宅商業混合使用需注意規定）
- 好處：有統一編號、可以報更多營業費用、可以加入 Apple Developer Organization

### 4.4 隱私權政策

**Apple 要求所有 App 都必須有隱私權政策。**

**最簡單的做法：**

1. 用免費工具產生：
   - [Termly](https://termly.io/) - 免費方案可產生隱私權政策
   - [Privacy Policy Generator](https://app-privacy-policy-generator.firebaseapp.com/) - 完全免費
   - 或自己寫（見下方模板）

2. 放在網路上：
   - 最簡單：建一個 GitHub Pages 頁面
   - 或放在你的 Web App 上
   - 只要有一個 public URL 即可

3. 在 App Store Connect 填入 URL

**隱私權政策必須涵蓋：**
- 你收集哪些資料（語音資料、筆記內容、使用分析）
- 為什麼收集（提供服務、改善產品）
- 是否分享給第三方（OpenAI API → 是的，要揭露）
- 資料保留多久
- 使用者如何刪除資料
- 聯絡方式

**App Store Connect 隱私權營養標籤：**
- 除了隱私權政策 URL，還需要填寫「App Privacy」問卷
- 要誠實宣告收集了哪些資料
- 語音子彈筆記可能涉及：
  - ✅ User Content（使用者產生的內容：語音、筆記）
  - ✅ Usage Data（使用分析：如果有加 Analytics）
  - ✅ Identifiers（如果有帳號系統）

**使用條款（Terms of Use）：**
- 訂閱制 App 建議要有
- 涵蓋：服務說明、付費條款、退款政策、免責聲明
- 同樣可以用免費工具產生，放在 public URL

---

## 5. 語音子彈筆記 App 的具體規劃

### 5.1 核心價值主張

> **一句話：** 用說的完成一天的子彈筆記，AI 幫你整理結構和產生 insight。

**解決的痛點：**
- 子彈筆記很好用，但手寫/打字很花時間
- 語音輸入很方便，但語音轉文字後是一團亂
- 現有工具沒有完整解決「語音 → 結構化筆記 → insight」的流程

### 5.2 MVP 功能定義

**核心功能（MVP 必須有的）：**

| 功能 | 說明 | 技術 |
|------|------|------|
| 🎙️ 語音錄製 | 按一個按鈕開始講話 | AVAudioEngine |
| 📝 語音轉文字 | 即時顯示辨識結果 | Apple Speech Framework（免費、離線可用） |
| 🤖 AI 解析 | 將自然語言轉為結構化筆記 | OpenAI / Claude API |
| 📋 子彈筆記呈現 | Task（・）、Event（○）、Note（—）、Signifiers（★ !） | SwiftUI List |
| 📅 日誌檢視 | 按日期查看筆記 | SwiftUI NavigationStack |
| 💾 本地儲存 | 筆記存在手機上 | SwiftData |

**延伸功能（v1.1 以後）：**

| 功能 | 優先度 | 說明 |
|------|--------|------|
| iCloud 同步 | 高 | iPhone/iPad/Mac 同步 |
| AI Insight | 高 | 每週/月自動分析趨勢和建議 |
| 自訂 Template | 中 | 使用者自定義筆記格式 |
| Widget | 中 | 首頁小工具快速錄製 |
| Siri Shortcut | 中 | 「嘿 Siri，記筆記」 |
| 匯出 | 中 | Markdown、PDF 匯出 |
| 搜尋 | 高 | 全文搜尋歷史筆記 |
| 提醒 | 低 | 從筆記自動建立提醒 |
| Apple Watch | 低 | 手腕上錄製 |
| 多語言 | 中 | 支援中英文混合辨識 |

### 5.3 技術架構

```
┌─────────────────────────────────────┐
│              UI Layer               │
│         (SwiftUI + MVVM)            │
│                                     │
│  ┌──────────┐  ┌──────────────────┐ │
│  │ Recording │  │  Journal View    │ │
│  │   View    │  │  (Daily/Weekly)  │ │
│  └──────────┘  └──────────────────┘ │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│           Service Layer             │
│                                     │
│  ┌──────────────┐ ┌──────────────┐  │
│  │ Speech       │ │ AI Parser    │  │
│  │ Recognition  │ │ Service      │  │
│  │ Service      │ │ (OpenAI /    │  │
│  │ (Apple       │ │  Claude)     │  │
│  │  Speech)     │ │              │  │
│  └──────────────┘ └──────────────┘  │
│                                     │
│  ┌──────────────┐ ┌──────────────┐  │
│  │ Subscription │ │ Export       │  │
│  │ Manager      │ │ Service      │  │
│  │ (RevenueCat) │ │              │  │
│  └──────────────┘ └──────────────┘  │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│           Data Layer                │
│                                     │
│  ┌──────────────┐ ┌──────────────┐  │
│  │ SwiftData    │ │ iCloud       │  │
│  │ (Local DB)   │ │ (CloudKit)   │  │
│  └──────────────┘ └──────────────┘  │
└─────────────────────────────────────┘
```

**AI 解析 Prompt 設計（核心）：**

```
你是一個子彈筆記助手。將使用者的語音輸入轉換為結構化的子彈筆記格式。

規則：
- Task（待辦事項）：標記為 「・」
- Event（事件）：標記為 「○」
- Note（筆記/想法）：標記為 「—」
- Important（重要）：加上 ★
- Inspiration（靈感）：加上 !

使用者說的話：
「今天早上開了一個很重要的會，跟 PM 討論了 Q2 的 roadmap。
下午要記得買牛奶。還有明天要交那個報告。
突然想到一個好點子，可以用 AI 自動整理會議記錄。」

輸出：
○ 早上開會：與 PM 討論 Q2 roadmap ★
・買牛奶
・明天交報告 ★
— 💡 點子：用 AI 自動整理會議記錄 !
```

### 5.4 競品分析

| App | 定位 | 語音→筆記？ | 子彈筆記格式？ | AI 功能 | 定價 | 缺什麼 |
|-----|------|------------|---------------|---------|------|--------|
| **Day One** | 日記 | 有語音附件，但不轉文字 | 否 | 否 | $35/年 | 不是子彈筆記、無 AI |
| **Notion** | 全能工作空間 | Notion AI 可語音摘要 | 可自訂但複雜 | 有（$10/月） | $8-10/月 | 太重量級、學習成本高 |
| **Bear** | Markdown 筆記 | 無 | 無 | 無 | $30/年 | 無語音、無 AI |
| **Otter.ai** | 語音轉文字 | 核心功能 | 否 | 摘要 | $8.33/月 | 不是筆記工具、不是子彈筆記 |
| **Whisper Memos** | 語音備忘 | 有 | 否 | 簡單摘要 | 免費+$50/年 | 無子彈筆記格式 |
| **Siri + Notes** | 內建 | 基本語音輸入 | 否 | 否 | 免費 | 完全沒有結構化 |

**市場缺口：** 沒有任何 App 完整解決「語音 → 子彈筆記格式 → AI insight」。這是一個明確的利基市場。

**護城河分析：**
- 技術護城河：低（語音辨識和 AI 都是現有 API）
- 體驗護城河：中（UI/UX 的流暢度、prompt 設計的品質）
- 資料護城河：高（使用者累積的筆記資料，遷移成本高）
- 品牌護城河：建立中（搭配 Podcast 內容）

### 5.5 定價策略

**推薦方案：**

| 方案 | 價格 | 內容 |
|------|------|------|
| **Free** | $0 | 每天 3 次語音筆記、基本模板、本地儲存 |
| **Pro（月繳）** | $3.99/月 | 無限語音筆記、AI insight、iCloud 同步、自訂模板、匯出 |
| **Pro（年繳）** | $29.99/年（≈$2.50/月，省 37%） | 同上 |

**定價理由：**
- $3.99/月是「衝動購買」門檻以下
- 年繳折扣大（37%）鼓勵長期訂閱，降低 churn
- Free 方案讓使用者養成習慣，3 次/天的限制足夠體驗但不夠「爽」
- 與競品相比偏低（Day One $35/年，Notion $96/年），但功能聚焦

**免費試用期：**
- 7 天 Pro 免費試用（Apple 支援設定）
- 試用結束自動轉為 Free
- 試用轉付費率目標：10-15%

---

## 6. App 推廣策略

### 6.1 ASO（App Store Optimization）

**App 名稱和副標題（最重要的 SEO 要素）：**
```
名稱：Voice Bullet Journal — 語音子彈筆記
副標題：Speak Your Day, AI Organizes It
```

**關鍵字策略（100 字元以內）：**
```
語音筆記,bullet journal,子彈筆記,日記,voice memo,AI,待辦事項,日誌,recording,生產力
```

**截圖策略（依序）：**
1. 第一張：最大賣點 →「說出你的一天，AI 幫你整理」
2. 第二張：語音錄製畫面
3. 第三張：AI 解析後的子彈筆記格式
4. 第四張：AI Insight 功能
5. 第五張：iCloud 同步
6. 第六張：定價/社會證明

**App 描述結構：**
```
第一行（最重要）：用說的完成子彈筆記。AI 幫你整理結構、產生 insight。

核心功能：
・語音輸入，自動辨識
・AI 解析為子彈筆記格式（Task / Event / Note）
・每週 AI Insight 分析你的生活模式
・iCloud 跨裝置同步

為什麼選 Voice Bullet Journal？
[使用者痛點 + 解決方案]

定價資訊：
免費使用基本功能，Pro 方案解鎖無限語音筆記和 AI insight。
```

### 6.2 搭配 Podcast / 社群推廣

**與你的其他 side hustle 整合：**

| 管道 | 做法 | 效果 |
|------|------|------|
| **Podcast（02-podcast-bobo）** | 專集介紹 App 開發過程、定期使用 App 分享生活 | 精準受眾、信任度高 |
| **Build in Public（10-build-in-public）** | Twitter/X 上分享開發進度、數據透明 | 開發者社群關注 |
| **AI 教學（07-ai-teaching-courses）** | 用 Voice Bullet Journal 作為 AI 應用案例 | 建立 authority |
| **內容自動化（06-automation-content-pipeline）** | App 使用者的匿名化 insight 做成內容 | 持續內容素材 |

**具體時間線：**
- App 開發期間：Build in Public，每週分享進度
- Beta 測試：Podcast 徵集 TestFlight 測試者
- 上架：Podcast 專集 + 社群全面推廣
- 上架後：持續用 Podcast 講使用場景和 tips

### 6.3 台灣 vs 國際市場

**建議策略：國際優先，台灣同步**

| 面向 | 國際市場 | 台灣市場 |
|------|---------|---------|
| 語言 | 英文介面為主 | 繁中在地化 |
| 市場大小 | 巨大（iOS 全球用戶 > 10 億） | 小（iPhone 用戶約 500 萬） |
| 付費意願 | 美國、日本最高 | 台灣偏低但在成長 |
| 競爭 | 激烈 | 在地化 App 競爭少 |
| 行銷 | ASO + Product Hunt + Reddit | Podcast + PTT + 社群 |

**具體做法：**
1. App 預設英文，支援繁中
2. ASO 關鍵字同時做英文和中文
3. 在 Product Hunt 上 launch（目標 Top 5 of the Day）
4. Reddit r/bulletjournal、r/productivity 發文
5. 台灣用 Podcast + Facebook 社群 + PTT

---

## 7. 其他 App 點子的評估框架

### 7.1 評估矩陣

對每個 App 點子，用以下 5 個維度評分（1-5 分）：

| 維度 | 問題 | 高分標準 |
|------|------|---------|
| **痛點強度** | 這個問題有多痛？使用者現在怎麼解決？ | 現有解決方案很差或不存在 |
| **市場大小** | 有多少人有這個需求？ | > 100 萬潛在使用者 |
| **付費意願** | 使用者願意為此付費嗎？ | 已有競品成功收費 |
| **技術可行性** | 你能在 2-4 週做出 MVP 嗎？ | 核心技術已有 API/框架 |
| **獨特優勢** | 你有什麼別人沒有的？ | 技術能力 + 內容管道 + 個人經驗 |

**語音子彈筆記的評分：**
- 痛點強度：4/5（真的很多人想用語音記筆記但結果不好用）
- 市場大小：3/5（子彈筆記是 niche，但語音筆記市場較大）
- 付費意願：4/5（筆記/生產力工具付費率高）
- 技術可行性：5/5（所有技術都有現成 API）
- 獨特優勢：4/5（有 Podcast 管道、有 AI 經驗）
- **總分：20/25 → 值得做**

### 7.2 市場驗證方法（投入開發前）

**Level 1：桌面研究（1 天）**
- Google Trends 搜尋相關關鍵字趨勢
- App Store 搜尋競品，看評價和下載量
- Reddit/PTT 搜尋使用者抱怨和需求
- Product Hunt 看類似產品的反應

**Level 2：Landing Page 測試（2-3 天）**
- 做一個簡單的 landing page（用 Carrd 或自己寫）
- 描述 App 功能，放一個「Notify me when it launches」email 收集
- 用少量廣告（$50-100）投放到目標受眾
- 衡量：有多少人留 email？轉換率 > 5% 就是好訊號

**Level 3：Smoke Test / Wizard of Oz（1 週）**
- 做一個最簡版本（甚至可以是手動處理的 Shortcut / Telegram Bot）
- 讓 10-20 個人實際使用
- 觀察：他們用了幾次？會主動回來用嗎？會推薦朋友嗎？
- 最重要的問題：「如果這個工具明天消失，你會覺得困擾嗎？」

**Level 4：Pre-sale / Waitlist（2 週）**
- 在 landing page 上開放預購（年費打折）
- 如果有人願意在 App 還沒做出來時就付費 → 強驗證
- 用 Gumroad 或 Stripe Payment Link 收款

### 7.3 其他 App 點子的種子清單（搭配你的 side hustle）

| 點子 | 結合的 side hustle | 評估重點 |
|------|-------------------|---------|
| Podcast 筆記 AI（聽 Podcast → 自動筆記） | 02-podcast-bobo | 市場大，但 AI 摘要已有很多競品 |
| 冥想+AI 日記（08-mindfulness-x-ai） | 08-mindfulness-x-ai | 冥想 App 紅海，但 AI + 冥想組合較新 |
| 台股分析工具 | 01-taiwan-stock-newsletter | 台灣 niche，付費意願需驗證 |
| 內容排程工具 | 06-automation-content-pipeline | 工具型 SaaS，競品多但可做細分 |
| Build in Public Dashboard | 10-build-in-public | 開發者 niche，市場小但付費意願高 |

---

## 8. 時程規劃

### 8.1 整體 Timeline

```
Week 0 ──────── 準備
│ ・申請 Apple Developer Program
│ ・安裝 Xcode，跑通 Hello World
│ ・設定 GitHub repo
│
Week 1-2 ────── Web MVP（市場驗證用）
│ ・Next.js + Vercel
│ ・語音錄製 → Whisper API → AI 解析 → 顯示子彈筆記
│ ・分享給 10-20 人試用
│ ・收集回饋
│
Week 3-4 ────── iOS MVP 開發
│ ・SwiftUI 基本架構
│ ・語音錄製 + Apple Speech 辨識
│ ・AI 解析（OpenAI API）
│ ・子彈筆記展示 UI
│ ・本地儲存（SwiftData）
│
Week 5 ──────── 完善 + IAP
│ ・加入 RevenueCat 訂閱
│ ・UI 打磨
│ ・加入 onboarding flow
│ ・準備 App Store 素材（截圖、描述、圖示）
│
Week 6 ──────── 測試 + 提交
│ ・TestFlight beta 測試（邀請 Podcast 聽眾）
│ ・修 bug
│ ・準備隱私權政策、使用條款
│ ・提交審核
│
Week 7 ──────── 上架 + 推廣
│ ・審核通過，正式上架
│ ・Podcast 專集
│ ・Product Hunt launch
│ ・社群推廣
│
Week 8+ ─────── 迭代
  ・根據使用者回饋迭代
  ・加入 AI Insight 功能
  ・iCloud 同步
  ・持續 ASO 優化
```

### 8.2 每週時間分配建議（假設每週可用 10-15 小時）

| 時段 | 活動 | 時數 |
|------|------|------|
| 平日晚上 | 核心開發 | 1-2 小時 × 5 天 = 5-10 小時 |
| 週末 | 集中開發 + 測試 | 5 小時 |
| 零碎時間 | 學習 SwiftUI、看文件、回覆使用者回饋 | 隨時 |

### 8.3 MVP 各功能的預估開發時間

| 功能 | 預估時間 | 備註 |
|------|---------|------|
| 專案設定 + 基本架構 | 4 小時 | Xcode 專案、MVVM 架構、Navigation |
| 語音錄製 UI | 3 小時 | 錄製按鈕、波形顯示、計時器 |
| Apple Speech 辨識整合 | 4 小時 | SFSpeechRecognizer、即時辨識、錯誤處理 |
| AI 解析 Service | 4 小時 | API 呼叫、Prompt 設計、JSON 解析 |
| 子彈筆記資料模型 | 2 小時 | SwiftData Model、CRUD |
| 子彈筆記列表 UI | 4 小時 | 日檢視、icon 對應、編輯功能 |
| 日曆/日期選擇 | 3 小時 | 月曆視圖、日期切換 |
| 設定頁面 | 2 小時 | 語言、通知、帳號 |
| RevenueCat 訂閱 | 4 小時 | 產品設定、paywall UI、權限管理 |
| Onboarding | 3 小時 | 3-4 頁引導、權限請求 |
| App Store 素材 | 4 小時 | Figma 截圖、描述文案、圖示 |
| 測試 + Bug fix | 8 小時 | TestFlight、各裝置測試 |
| **合計** | **~45 小時** | **約 4-5 週（每週 10-12 小時）** |

### 8.4 關鍵里程碑與 Go/No-Go 決策點

| 時間點 | 里程碑 | Go/No-Go 判斷 |
|--------|--------|---------------|
| Week 2 | Web MVP 完成，10 人試用 | 如果沒人有興趣試用 → 重新評估需求 |
| Week 4 | iOS MVP 核心功能完成 | 語音→AI→子彈筆記 flow 是否夠流暢？ |
| Week 6 | TestFlight 發出 | Beta 使用者留存率？回饋是否正面？ |
| Month 2 | 上架一個月 | 有多少下載？免費→付費轉換率？ |
| Month 4 | 上架三個月 | MRR 趨勢？是否值得繼續投入？ |
| Month 6 | 半年回顧 | 是否達到 $500 MRR？是否 pivot？ |

---

## 附錄 A：快速行動 Checklist

**今天就可以做的：**
- [ ] 申請 Apple Developer Program（$99/年）
- [ ] 在 Mac 上安裝/更新 Xcode
- [ ] 在 Xcode 中建立新 SwiftUI 專案，跑 Hello World
- [ ] 註冊 RevenueCat 帳號（免費）
- [ ] 註冊 OpenAI API 帳號（如果還沒有）

**本週目標：**
- [ ] 完成 Web MVP 或 iOS 語音錄製 + 辨識 PoC
- [ ] 寫好 AI 解析的 prompt 並測試效果
- [ ] 在 Podcast 上預告即將開發的 App

**本月目標：**
- [ ] iOS MVP 完成
- [ ] TestFlight 發送給 20+ beta 測試者
- [ ] 準備 App Store 上架素材
- [ ] 提交審核

---

## 附錄 B：有用的資源連結

| 資源 | 連結 | 說明 |
|------|------|------|
| Apple Developer | developer.apple.com | 官方開發者入口 |
| App Store Connect | appstoreconnect.apple.com | App 管理和上架 |
| App Store Review Guidelines | developer.apple.com/app-store/review/guidelines | 審核規則（必讀） |
| Human Interface Guidelines | developer.apple.com/design/human-interface-guidelines | Apple 設計規範 |
| SwiftUI Tutorials | developer.apple.com/tutorials/swiftui | 官方 SwiftUI 教學 |
| RevenueCat Docs | docs.revenuecat.com | IAP 整合文件 |
| StoreKit 2 | developer.apple.com/storekit | 原生 IAP 文件 |
| SF Symbols | developer.apple.com/sf-symbols | 免費圖示庫 |
| App Annie / data.ai | data.ai | App 市場數據 |
| Sensor Tower | sensortower.com | ASO 工具 |

---

## 附錄 C：語音子彈筆記 Prompt 完整設計

```
System Prompt:
你是一個子彈筆記助手。你的任務是將使用者的語音轉文字輸入，解析為結構化的子彈筆記格式。

輸出規則：
1. 每一行用以下符號開頭：
   - 「・」= Task（待辦事項、需要行動的事）
   - 「○」= Event（已發生或將發生的事件）
   - 「—」= Note（想法、觀察、備忘）

2. 重要性標記（加在行尾）：
   - 「★」= 重要/優先
   - 「!」= 靈感/好點子

3. 時間標記：如果使用者提到具體時間，加在符號後面，例如「・[14:00] 開會」

4. 分類：如果內容涉及不同主題，用空行分隔並加上主題標題

5. 輸出格式：純文字，不要 markdown

6. 語言：與使用者相同的語言

7. 不要加入使用者沒說的內容
8. 如果使用者說了「嗯、呃、那個」等填充詞，直接忽略

範例輸入：
「今天早上跟 John 開了一個很重要的季度 review 會議，結論是 Q2 要 focus 在降低 churn rate。下午三點要去接小孩。然後晚上想 research 一下 SwiftUI 的動畫怎麼做。對了還有一個很好的想法，就是可以在 app 裡面加一個 mood tracker。」

範例輸出：
○ 早上與 John 開季度 review 會議 ★
— Q2 focus：降低 churn rate
・[15:00] 接小孩
・晚上 research SwiftUI 動畫
— App 功能想法：加入 mood tracker !
```

---

> **最後提醒：** 完美是好的敵人。先上架一個 80 分的 MVP，根據真實使用者回饋迭代，比花三個月做一個 100 分的 App 有效得多。你有技術能力，差的只是行動。現在就開始。

---

## 9. 後端架構與 API Key 管理

### 9.1 核心原則

**一個 API key 服務所有用戶。** 就像開餐廳：你跟食材商開一個帳戶，所有客人的菜都用你的帳戶進貨，客人不需要知道食材商是誰。

### 9.2 為什麼不能把 API Key 放在 App 裡

```
❌ 絕對不要這樣做：
iOS App 裡寫死 API key → 直接打 OpenAI/Gemini

風險：
1. 任何人都能反編譯你的 app，拿到你的 key
2. 有人寫 script 用你的 key 狂打 → 天價帳單
3. 你無法控制誰用了多少
4. 違反 OpenAI/Gemini 的使用條款
```

### 9.3 正確架構：Cloudflare Worker 當中間層

```
┌─────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  iOS App    │ ──→ │  Cloudflare Worker   │ ──→ │  OpenAI/Gemini  │
│  (用戶手機) │ ←── │  api.asherdom.me     │ ←── │  API            │
└─────────────┘     └──────────────────────┘     └─────────────────┘
                           ↑
                    你的 API key 存在這裡
                    （環境變數，用戶看不到）
```

**為什麼用 Cloudflare Worker：**
- 你已經有 Cloudflare 帳號和域名
- 免費額度：每天 100,000 次請求（遠遠夠）
- 全球部署，延遲低
- 不用自己架 Server

### 9.4 Cloudflare Worker 完整範例

```javascript
// wrangler.toml 設定
// name = "voice-bullet-journal-api"
// [vars]
// OPENAI_KEY = "sk-..." ← 用 wrangler secret put OPENAI_KEY 設定，不要寫在這裡

export default {
  async fetch(request, env) {
    // CORS 處理
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST",
          "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
      });
    }

    // 1. 驗證用戶身份
    const authToken = request.headers.get("Authorization")?.replace("Bearer ", "");
    const user = await verifyAppUser(authToken, env);
    if (!user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), {
        status: 401,
        headers: { "Content-Type": "application/json" }
      });
    }

    // 2. 檢查每日用量
    const today = new Date().toISOString().split("T")[0];
    const usageKey = `usage:${user.id}:${today}`;
    const currentUsage = parseInt(await env.KV.get(usageKey) || "0");
    const limit = user.isPro ? 50 : 3; // 付費 50 次/天，免費 3 次/天

    if (currentUsage >= limit) {
      return new Response(JSON.stringify({
        error: "Daily limit reached",
        limit: limit,
        upgrade: !user.isPro
      }), { status: 429 });
    }

    // 3. 取得用戶傳來的語音轉文字結果
    const { transcript, template } = await request.json();

    // 4. 呼叫 AI API（用你的 key，用戶看不到）
    const aiResponse = await fetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-goog-api-key": env.GEMINI_KEY  // 存在環境變數
      },
      body: JSON.stringify({
        contents: [{
          parts: [{ text: `將以下語音轉文字結果整理成子彈筆記格式：\n\nTemplate: ${template}\n\n語音內容：${transcript}` }]
        }]
      })
    });

    const result = await aiResponse.json();

    // 5. 更新用量計數
    await env.KV.put(usageKey, String(currentUsage + 1), { expirationTtl: 86400 });

    // 6. 回傳結果
    return new Response(JSON.stringify({
      bulletJournal: result.candidates[0].content.parts[0].text
    }), {
      headers: { "Content-Type": "application/json" }
    });
  }
};
```

### 9.5 API Key 申請步驟

**Gemini（推薦，最便宜）：**
1. 前往 [aistudio.google.com](https://aistudio.google.com)
2. 登入 Google 帳號
3. 左側選單 → Get API Key → Create API Key
4. 複製 key
5. 設定付費：Google Cloud Console → Billing → 綁信用卡
6. 設定用量上限：Google Cloud Console → APIs → Quotas

**OpenAI（備選）：**
1. 前往 [platform.openai.com](https://platform.openai.com)
2. 註冊/登入
3. API Keys → Create new secret key
4. Settings → Billing → 綁信用卡
5. Settings → Limits → 設定 Monthly budget（例如 $100）

### 9.6 三層費用保護

```
第一層：API 供應商後台
├── 設定每月上限（例如 $100/月）
├── 超過自動停止，不會被刷爆帳單
└── Email 警告（到 80% 時通知你）

第二層：Cloudflare Worker
├── Per-user 每日限制（免費 3 次、付費 50 次）
├── Rate limiting（每分鐘最多 10 次/user，防 script 攻擊）
└── 用 KV 記錄用量

第三層：App 端 UI
├── 顯示剩餘次數「今天還剩 47 次」
├── 免費用戶到達上限 → 顯示升級付費的畫面
└── 離線時直接擋住（不送無效請求）
```

### 9.7 成本估算

| 模型 | 每次 call 成本 | 100 用戶/月 | 1,000 用戶/月 | 10,000 用戶/月 |
|------|---------------|-------------|---------------|----------------|
| Gemini 2.0 Flash | ~$0.002 | $6 | $60 | $600 |
| GPT-5.2 mini | ~$0.005 | $15 | $150 | $1,500 |
| Claude Haiku | ~$0.003 | $9 | $90 | $900 |

假設每用戶每天平均 2 次，一個月 60 次。

**收入 vs 成本（以 Gemini Flash 為例）：**

| 付費用戶 | 月收入（$3.99） | Apple 抽成 15% | API 成本 | 淨利 | 利潤率 |
|----------|----------------|---------------|----------|------|--------|
| 100 | $399 | $60 | $6 | $333 | 83% |
| 1,000 | $3,990 | $599 | $60 | $3,331 | 83% |
| 10,000 | $39,900 | $5,985 | $600 | $33,315 | 83% |

**API 成本只佔收入的 1.5%，幾乎可以忽略。**

### 9.8 部署步驟（你已經有 Cloudflare，10 分鐘搞定）

```bash
# 1. 安裝 Wrangler CLI
npm install -g wrangler

# 2. 登入 Cloudflare
wrangler login

# 3. 建立專案
wrangler init voice-bullet-journal-api

# 4. 設定 secret（API key 不會出現在 code 裡）
wrangler secret put GEMINI_KEY
# 貼上你的 Gemini API key

# 5. 建立 KV namespace（用來記錄用量）
wrangler kv namespace create USAGE

# 6. 部署
wrangler deploy

# 7. 設定自訂域名（在 Cloudflare dashboard）
# api.asherdom.me → 指向這個 Worker
```

---

## 10. OpenClaw Skill 的定位

### 10.1 為什麼 Skill 不該是產品

OpenClaw/Claude Code 的 skill 有一個根本問題：**使用者需要自己的 LLM API token。**

```
一般人要用你的 skill：
1. 要裝 Claude Code / OpenClaw ← 刷掉 95% 的人
2. 要有自己的 API key ← 再刷掉一半
3. 要會設定 skill ← 再刷掉一些
4. 每次用還要花自己的 token 錢 ← 體驗差
```

能走完這四步的人，大概自己就能寫一個。這不是消費者產品，是開發者玩具。

### 10.2 正確定位：行銷工具

```
OpenClaw 子彈筆記 Skill（免費公開）
    → GitHub stars、SkillsMP 上架
    → 開發者社群看到你
    → 引流到 Podcast / 電子報
    → 你錄一集「我怎麼用 AI 自動寫子彈筆記」
    → 有人問「能不能不用 API key 就用？」
    → 你說「可以，下載我的 App」
    → App Store 訂閱制 $3.99/月
```

### 10.3 Skill vs App 的分工

| | OpenClaw Skill | iOS App |
|--|---------------|---------|
| 目標用戶 | 開發者（引流用） | 一般人（賺錢用） |
| 價格 | 免費 | $3.99/月 |
| API key | 用戶自己的 | 你的（藏在 Worker 裡） |
| 體驗 | 需要設定 | 下載 → 按錄音 → 完成 |
| 功能 | 基礎版 | 完整版（insight、歷史、趨勢） |
| 目的 | 建立聲量 | 營利 |

---

## 11. 市場分析：為什麼 App Store 還沒被 AI App 攻佔

### 11.1 五大障礙

| 障礙 | 影響程度 | 說明 |
|------|----------|------|
| **Apple 審核卡嚴** | 極高 | AI app 有額外審查，「ChatGPT wrapper」類 app 大量被拒 |
| **包裝問題** | 高 | 沒有獨特價值的 AI wrapper app，Apple 直接拒絕 |
| **商業模式** | 高 | 定價太高沒人買，太低不夠覆蓋 API 成本 |
| **大玩家壟斷** | 中高 | ChatGPT / Gemini / Claude 自己就有 app |
| **留存率低** | 中 | 很多 AI app 用一兩次就不用了，撐不起訂閱制 |

### 11.2 能活下來的 AI App 的共同點

**都解決一個非常具體的痛點，而不是「又一個 AI 聊天 app」。**

| 成功的 AI App | 具體痛點 | 為什麼活得下來 |
|---------------|----------|----------------|
| Be My Eyes | 視障者需要看東西 | 剛需，無可替代 |
| Otter.ai | 開會來不及記筆記 | 場景明確，用完就有價值 |
| Photomath | 學生看不懂數學題 | 拍一下就有答案 |
| Duolingo | 想學語言但沒動力 | AI 讓體驗更個人化 |

### 11.3 語音子彈筆記的市場定位

```
不是：「又一個 AI 聊天 app」
而是：「按一個按鈕，講話，自動變成整理好的子彈筆記」

痛點：想寫日記/筆記但懶得打字，語音錄完又懶得整理
場景：通勤、散步、睡前
頻率：每天都用 ← 訂閱制能活的關鍵
```

### 11.4 定價心理學

用戶不知道什麼是 token，他只關心值不值：

| 比較對象 | 月費 |
|----------|------|
| 超商咖啡 × 3 | ~NT$135 |
| Netflix | NT$390 |
| Spotify | NT$149 |
| **你的 App** | **NT$120（$3.99 USD）** |

你的 API 成本才 $0.09/user/月 — 用戶付的 $3.99 裡面只有 2% 是 token 成本。問題從來不是「token 太貴」，而是「能不能讓用戶覺得值得付錢」。

### 11.5 你的競爭優勢（大部分人被卡住的門檻你已經跨過）

| 障礙 | 一般人 | 你 |
|------|--------|-----|
| 不會寫 app | 卡住 | Google 工程師 |
| 不懂後端架構 | 卡住 | 已有 Cloudflare + web service 經驗 |
| 害怕 API 成本 | 卡住 | 算得出來只佔 2% |
| 不知道怎麼推廣 | 卡住 | 有 Podcast + 電子報 + 社群計畫 |
| 沒有具體痛點 | 做 wrapper app 被拒 | 自己就是用戶，知道痛點 |

### 11.6 最差情況分析

| 成本 | 金額 | 說明 |
|------|------|------|
| Apple Developer | $99/年 | 就算失敗也就虧這個 |
| API 費用 | $0-6/月 | 沒人用就是 $0 |
| Cloudflare Worker | $0 | 免費 |
| 你的時間 | 3-5 週 | 最大成本，但學會了 iOS 開發 |

**最差：虧 $99 + 學會 iOS 開發 + 有了作品集。不算虧。**

---

## 12. 防濫用機制

### 12.1 核心觀念

用戶碰不到你的 API token。Token 存在 Cloudflare Worker 環境變數裡，用戶只能透過你的 Worker 間接使用，Worker 裡你說了算。

### 12.2 四層防護

```
用戶瘋狂按錄音想打爆你的 API
        ↓
第 1 關：App 端 — 按鈕 cooldown 5 秒，灰掉不能按
        ↓ （如果有人繞過 app 直接打 API）
第 2 關：Cloudflare Rate Limiting — 同一 IP/User 每分鐘最多 5 次
        ↓ （每天的總量控制）
第 3 關：Cloudflare Worker — 每人每天最多 50 次（付費）/ 3 次（免費）
        ↓ （最後一道防線）
第 4 關：API 供應商後台 — 月花費上限（例如 $100），到了就全部停止
        ↓
最壞情況：這個月 API 花了 $100 就停了，你的信用卡最多被扣 $100
```

### 12.3 最壞情況計算

假設有人寫 script 繞過 app，直打你的 Worker：

```
他需要：
1. 一個有效的 auth token（要註冊 + 驗證）
2. 每分鐘只能打 5 次（Cloudflare rate limit）
3. 每天只能打 50 次（per-user limit）

50 次 × $0.002/次 = $0.10/天 — 一個壞人一天花你台幣 3 塊
```

搞 100 個假帳號的情況：
- 100 帳號 × $0.10/天 = $10/天
- API 月上限 $100 → 10 天到頂，自動停
- 但現實中，搞 100 個假帳號需要 100 個不同的 email 驗證，幾乎不會發生在小 app 上

### 12.4 分階段加強

| 階段 | 保護措施 | 什麼時候加 |
|------|----------|-----------|
| **MVP** | App cooldown + per-user limit + API 月上限 | **Day 1（必做）** |
| 100+ 用戶 | Cloudflare Rate Limiting 規則 | 有人開始濫用時 |
| 1,000+ 用戶 | 異常偵測（用量暴增 → 自動停權） | 規模到了再做 |
| 10,000+ 用戶 | 專門的 abuse detection 服務 | 那時候請得起人了 |

### 12.5 Cloudflare Rate Limiting 設定（內建免費功能）

```
Cloudflare Dashboard → 你的 Worker → Settings → Rate Limiting

規則 1：同一個 IP，每分鐘最多 10 次 → 超過回傳 429
規則 2：同一個 User ID，每天最多 50 次 → 超過回傳 429
```

### 12.6 API 供應商月上限設定

**Gemini：**
```
Google Cloud Console → APIs & Services → Quotas
→ 找到 Generative Language API
→ 設定 Requests per month 上限
→ 同時在 Billing → Budgets → 設定 $100 月預算 + email 警報
```

**OpenAI：**
```
platform.openai.com → Settings → Limits
→ Set monthly budget: $100
→ Email notification at: $80（到 80% 時通知你）
```

**MVP 階段就設 $100 月上限，這是你最簡單也最有效的保險。不要過度設計。**

---

## 13. 平滑服務用戶的完整體驗設計

### 13.1 核心原則

**永遠不要讓用戶看到「錯誤」，要讓他們看到「選擇」。**
**永遠不要讓用戶丟失資料。不管發生什麼事，錄音內容必須留在本地。**

### 13.2 完整用戶流程

```
用戶按錄音
    ↓
Apple Speech 離線轉文字（即時，不需網路）
    ↓
文字立刻存到手機本地（不管有沒有網路，錄音永遠不會丟）
    ↓
有網路嗎？
    ├── 是 → 有額度嗎？
    │        ├── 是 → 送 Worker → AI 整理 → 顯示結果
    │        │        ├── < 3秒：直接顯示
    │        │        ├── 3-10秒：顯示進度提示
    │        │        └── > 10秒：背景處理 + 推播通知
    │        │
    │        └── 否 → 顯示升級畫面（正面語氣，非錯誤畫面）
    │                 仍然保存原始文字版
    │
    └── 否 → 離線模式
             顯示原始文字版
             標記「待 AI 整理」
             有網路時自動處理
```

### 13.3 五個關鍵場景

**場景 1：免費用戶用完每日額度**

```
不要顯示：「Error: Daily limit reached」

要顯示：
┌──────────────────────────────────┐
│  今天已經記錄了 3 則筆記          │
│                                  │
│  明天會重新獲得 3 次免費額度       │
│                                  │
│  想要無限次記錄？                 │
│  ┌────────────────────────┐     │
│  │  升級 Pro — NT$120/月   │     │
│  └────────────────────────┘     │
│                                  │
│  （你今天錄的內容都已經儲存好了）   │
└──────────────────────────────────┘
```

重點：肯定用戶「你今天記了 3 則，很棒」→ 再引導升級。

**場景 2：API 回應太慢（超過 5 秒）**

```
第 0-2 秒：「AI 正在整理你的筆記...」
第 2-5 秒：「快好了，正在排版...」
第 5-10 秒：「今天比較忙，再等一下...」
第 10 秒 timeout：
  → 「AI 比較忙碌，你的錄音已經儲存」
  → 「會在背景完成整理，好了通知你」
  → 放進 queue，背景重試
```

**場景 3：API 掛掉 — 多 Provider Fallback**

Cloudflare Worker 裡的 fallback 邏輯：

```javascript
async function callAI(transcript, env) {
  const providers = [
    { name: "gemini",  fn: () => callGemini(transcript, env.GEMINI_KEY) },
    { name: "openai",  fn: () => callOpenAI(transcript, env.OPENAI_KEY) },
    { name: "claude",  fn: () => callClaude(transcript, env.CLAUDE_KEY) },
  ];

  for (const provider of providers) {
    try {
      const result = await provider.fn();
      return { result, provider: provider.name };
    } catch (e) {
      console.log(`${provider.name} failed, trying next...`);
      continue;
    }
  }

  // 全部失敗 → 回傳 null，app 端走離線儲存
  return null;
}
```

用戶端完全無感 — Gemini 掛了自動切 OpenAI，OpenAI 掛了切 Claude，全掛了才走離線模式。

**場景 4：用戶數突然暴增（被推薦、上新聞）**

Cloudflare Worker 自動 scale，不用你管。真正的瓶頸是 API rate limit：

| 階段 | 問題 | 解法 |
|------|------|------|
| 0-100 用戶 | 沒問題 | Gemini 付費 tier 夠用 |
| 100-1,000 | 尖峰偶爾塞車 | queue + 多 provider fallback |
| 1,000-5,000 | API rate limit 快到 | 申請提高額度（發信即可） |
| 5,000+ | 需要更多規劃 | 月收入 $20K+，請得起人了 |

**場景 5：沒網路（通勤、地下室、飛機上）**

這是最常見的場景 — 用戶很可能在通勤時錄音。

```
離線模式：
1. 錄音 → Apple Speech 離線轉文字（不需網路，品質OK）
2. 文字存在手機本地
3. 顯示「原始文字版」（沒 AI 整理但看得到內容）
4. 標記「待整理」圖標
5. 有網路時自動送出 → 整理完推播通知「你的筆記整理好了」
```

### 13.4 資料安全保證

不管任何情況，用戶的錄音內容永遠不會丟：

| 狀況 | 錄音/文字 | AI 整理結果 |
|------|----------|------------|
| 正常 | 本地有 | 本地有 |
| API 掛了 | 本地有 | 稍後補上 |
| 沒網路 | 本地有 | 稍後補上 |
| 額度用完 | 本地有 | 升級後或明天補上 |
| App 閃退 | 錄音檔在本地 | 重開 app 自動恢復 |

**用戶最害怕的不是「AI 沒整理好」，是「我講的東西不見了」。只要內容永遠不丟，其他都可以等。**

### 13.5 用量提示的 UX 設計

```
App 首頁頂部顯示（免費用戶）：
┌─────────────────────────────┐
│  今日：●●●○○○○○○○  3/10    │  ← 視覺化剩餘次數
│  免費額度 3 次 ｜ 升級 Pro    │
└─────────────────────────────┘

App 首頁頂部顯示（Pro 用戶）：
┌─────────────────────────────┐
│  今日已記錄 12 則 ✨  Pro     │  ← 不顯示上限，因為 50 次很難用完
└─────────────────────────────┘
```

接近上限時（剩 1 次）：
```
錄音前彈出輕提示（不是彈窗，是 banner）：
「這是今天最後 1 次免費額度，要錄嗎？」
  [錄音]  [了解 Pro]
```

### 13.6 MVP 要做 vs 之後再做

| 功能 | MVP（必做） | V2（之後加） |
|------|-----------|------------|
| 本地儲存錄音/文字 | ✅ | |
| 額度用完 → 升級畫面 | ✅ | |
| API timeout → 背景重試 | ✅ | |
| 離線錄音 + 待整理 | ✅ | |
| 多 Provider fallback | | ✅ 先只串 Gemini |
| 用量視覺化 | | ✅ 先用文字顯示 |
| 推播通知「整理好了」 | | ✅ |
| Queue 系統 | | ✅ |
