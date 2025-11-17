# 📖 GitHub Pages 部署完整指南

## 🎯 目標

將軍事詞彙學習系統部署到：`https://a4ltw.github.io/MilP/`

---

## ⚡ 快速解決 404 問題

如果您看到 404 錯誤，**最可能的原因是 GitHub Pages 還沒有啟用**。

### 解決方案：啟用 GitHub Actions 部署

我已經為您配置好了自動部署腳本，您只需要：

---

## 📝 詳細步驟（帶截圖說明）

### 步驟 1：開啟 GitHub 倉庫設置

1. 前往您的倉庫：https://github.com/a4ltw/MilP
2. 點擊頂部導航欄的 **Settings**（設置）標籤
   - 如果看不到 Settings，確認您已登入且有倉庫權限

### 步驟 2：進入 Pages 設置

1. 在左側設置選單中，向下滾動找到 **Pages**
   - Pages 選項在 "Code and automation" 區域
2. 點擊 **Pages**

### 步驟 3：配置部署來源（重要！）

在 "Build and deployment" 區域：

#### 選項 A：使用 GitHub Actions（推薦✨）

1. 找到 **Source** 下拉選單
2. 選擇 **GitHub Actions**（不是 "Deploy from a branch"）
3. 無需其他設置，GitHub 會自動使用我們的 workflow

#### 選項 B：使用分支部署

1. **Source** 選擇：`Deploy from a branch`
2. **Branch** 選擇：`claude/military-vocab-learning-01SF7YSmsicxQi2knzADGRmH`
3. **Folder** 選擇：`/ (root)`
4. 點擊 **Save**

### 步驟 4：觸發部署

#### 如果您選擇了 GitHub Actions：

1. 點擊倉庫頂部的 **Actions** 標籤
2. 您會看到 "Deploy to GitHub Pages" workflow
3. 如果沒有自動運行，點擊 "Run workflow" 手動觸發
4. 等待約 1-2 分鐘，直到顯示綠色勾號 ✓

#### 如果您選擇了分支部署：

- GitHub 會自動開始部署
- 無需額外操作

### 步驟 5：驗證部署

1. 回到 **Settings > Pages**
2. 頁面頂部會顯示：
   ```
   Your site is live at https://a4ltw.github.io/MilP/
   ```
3. 點擊連結測試網站
4. 如果還是 404，等待 2-3 分鐘後重新整理

---

## 🔍 檢查清單

在設置前，請確認：

- [ ] 倉庫是 **Public**（公開）狀態
  - Settings > General > Danger Zone 可以查看
- [ ] 您有倉庫的 **管理權限**
  - 如果是 fork 的倉庫，確認您是擁有者
- [ ] 所有檔案都已推送到遠端
  - 執行 `git status` 確認沒有未提交的更改

---

## ❓ 常見問題排解

### Q1: 我看不到 "Pages" 選項

**原因**：倉庫可能是私有的

**解決方案**：
1. 前往 Settings > General
2. 滾動到最下方 "Danger Zone"
3. 點擊 "Change visibility"
4. 將倉庫設為 Public（公開）

### Q2: 部署後仍顯示 404

**可能原因**：
1. **部署還在進行中** - 等待 2-3 分鐘
2. **瀏覽器快取** - 按 Ctrl+F5 強制重新整理
3. **部署失敗** - 檢查 Actions 標籤是否有錯誤

**解決方案**：
```bash
# 檢查 Actions 運行狀態
1. 點擊倉庫頂部 "Actions" 標籤
2. 查看最新的 workflow 運行
3. 如果有紅色 X，點擊查看錯誤訊息
```

### Q3: Actions 顯示權限錯誤

**錯誤訊息**：
```
Error: The process '/usr/bin/git' failed with exit code 128
```

**解決方案**：
1. Settings > Actions > General
2. 向下滾動到 "Workflow permissions"
3. 選擇 **Read and write permissions**
4. 勾選 **Allow GitHub Actions to create and approve pull requests**
5. 點擊 Save
6. 重新運行 workflow

### Q4: Source 只有 "Deploy from a branch" 選項

**原因**：GitHub Actions 部署需要先有 workflow 文件

**解決方案**：
- 確認 `.github/workflows/deploy.yml` 文件存在
- 推送後等待幾分鐘，GitHub 會自動偵測
- 或者使用 "Deploy from a branch" 選項

### Q5: 資料無法載入（空白頁面）

**檢查步驟**：
1. 打開瀏覽器開發者工具（F12）
2. 切換到 Console 標籤
3. 查看是否有錯誤訊息
4. 切換到 Network 標籤
5. 重新整理頁面，查看哪個檔案載入失敗

**常見問題**：
- 檔案路徑大小寫問題
- CORS 錯誤（通常不會發生在 GitHub Pages）

---

## 🎨 部署成功後的檢查

訪問 `https://a4ltw.github.io/MilP/` 後，測試以下功能：

- [ ] 首頁正常載入
- [ ] 詞彙瀏覽標籤顯示詞彙列表
- [ ] 搜尋功能正常運作
- [ ] 學習模式可以開啟閃卡
- [ ] 測驗模式可以答題
- [ ] 進度追蹤顯示統計資料

---

## 🔄 更新網站內容

之後如果您修改了代碼，只需：

### 使用 GitHub Actions 部署：
```bash
git add .
git commit -m "您的更新說明"
git push
```
推送後，GitHub Actions 會自動重新部署（約 1-2 分鐘）

### 使用分支部署：
```bash
git add .
git commit -m "您的更新說明"
git push
```
推送後，GitHub Pages 會自動重新建置（約 2-5 分鐘）

---

## 📊 監控部署狀態

### 查看 Actions 運行歷史
1. 前往 https://github.com/a4ltw/MilP/actions
2. 查看所有部署記錄
3. 點擊任一運行查看詳細日誌

### 查看 Pages 狀態
1. 前往 Settings > Pages
2. 查看當前發布狀態
3. 查看最後部署時間

---

## 🎯 成功！

當您看到這個畫面，表示部署成功：

```
✓ 網址：https://a4ltw.github.io/MilP/
✓ 詞彙列表正常顯示
✓ 所有功能都能使用
✓ 手機、平板、電腦都能訪問
```

---

## 💡 進階技巧

### 自訂網域

如果您有自己的網域（例如 vocab.example.com）：

1. Settings > Pages > Custom domain
2. 輸入您的網域名稱
3. 在您的網域提供商設置 CNAME 記錄：
   ```
   CNAME vocab.example.com a4ltw.github.io
   ```

### 啟用 HTTPS

GitHub Pages 預設啟用 HTTPS，但如果使用自訂網域：

1. 等待 DNS 記錄生效（可能需要 24 小時）
2. Settings > Pages
3. 勾選 "Enforce HTTPS"

---

## 🆘 還是無法解決？

如果您嘗試了以上所有方法仍然無法部署：

1. **檢查 GitHub Status**：https://www.githubstatus.com/
   - GitHub Pages 服務可能暫時中斷

2. **查看社群討論**：
   - GitHub Community：https://github.community/

3. **查看完整錯誤日誌**：
   - Actions 標籤中的詳細錯誤訊息

4. **聯絡我**：
   - 提供錯誤截圖和訊息，我會幫您診斷問題

---

**祝您部署順利！** 🚀

一旦部署成功，您就能隨時隨地學習軍事詞彙了！
