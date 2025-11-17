# GitHub Pages 部署指南

由於專案分支命名限制，您需要手動在 GitHub 網頁介面設置 GitHub Pages。請按照以下步驟操作：

## 📋 設置步驟

### 方法一：使用現有分支（最簡單）

1. **前往 GitHub 倉庫**
   - 開啟 https://github.com/a4ltw/MilP

2. **進入 Settings（設置）**
   - 點擊倉庫頂部的 "Settings" 標籤

3. **找到 Pages 設置**
   - 在左側選單中找到 "Pages"

4. **配置 Source（來源）**
   - 在 "Build and deployment" 區域
   - Source 選擇：**Deploy from a branch**
   - Branch 選擇：**claude/military-vocab-learning-01SF7YSmsicxQi2knzADGRmH**
   - 資料夾選擇：**/ (root)**
   - 點擊 **Save**

5. **等待部署**
   - GitHub 會自動開始建置
   - 約 1-2 分鐘後，頁面會顯示網站 URL
   - URL 格式：`https://a4ltw.github.io/MilP/`

### 方法二：使用 GitHub Actions（推薦）

如果您希望從 main 分支發布，需要先將代碼合併到 main：

1. **在 GitHub 網頁建立 Pull Request**
   - 前往 "Pull requests" 標籤
   - 點擊 "New pull request"
   - Base: main (如果不存在，會自動建立)
   - Compare: claude/military-vocab-learning-01SF7YSmsicxQi2knzADGRmH
   - 點擊 "Create pull request"
   - 合併 PR

2. **設置 GitHub Pages**
   - 按照方法一的步驟 1-5
   - 但在第 4 步選擇 **main** 分支

## ✅ 驗證部署

部署完成後：

1. **訪問網站**
   ```
   https://a4ltw.github.io/MilP/
   ```

2. **檢查功能**
   - 確認詞彙資料正常載入
   - 測試各個功能模組
   - 檢查在不同裝置上的顯示

## 🔧 常見問題

### Q: 為什麼我看不到 Pages 選項？
A: 確認您有倉庫的管理權限，並且倉庫是 Public（公開）。私有倉庫需要 GitHub Pro。

### Q: 部署後顯示 404？
A:
- 檢查分支名稱是否正確
- 確認 index.html 在根目錄
- 等待 2-3 分鐘讓部署完成

### Q: 資料載入失敗？
A:
- 確認 data/vocabulary.json 檔案存在
- 檢查瀏覽器控制台的錯誤訊息
- 確認所有檔案路徑使用相對路徑

### Q: 更新代碼後網站沒變化？
A:
- 推送新代碼後，GitHub Pages 需要幾分鐘重新建置
- 清除瀏覽器快取（Ctrl+F5 或 Cmd+Shift+R）
- 檢查 Actions 標籤確認部署狀態

## 📱 分享您的學習網站

部署完成後，您可以：

1. **分享連結**
   ```
   https://a4ltw.github.io/MilP/
   ```

2. **添加到 README**
   在 README.md 頂部加入：
   ```markdown
   ## 🌐 線上使用

   立即訪問：[https://a4ltw.github.io/MilP/](https://a4ltw.github.io/MilP/)
   ```

3. **設置自訂網域**（可選）
   - 在 Pages 設置中輸入您的網域
   - 在網域提供商設置 CNAME 記錄

## 🚀 下一步

部署完成後：
- ✅ 立即開始線上學習
- ✅ 可在任何裝置存取
- ✅ 分享給需要的朋友
- ✅ 學習進度依然儲存在本地瀏覽器

---

**注意**：由於使用 localStorage，學習進度只儲存在您使用的瀏覽器中。若在不同裝置使用，需要用「匯出進度」功能同步。

如遇問題，歡迎在 GitHub Issues 中提出！
