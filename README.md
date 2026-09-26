# 📡 AIoT 智慧安防與環境感測系統

本專案結合**「架構解耦 (Decoupling)」** 與**「邊緣運算 (Edge AI)」** 思維，打造針對校園天台生態園與戶外大型場域設計的人形辨識與智慧安防系統。

---

## 🛠️ 技術棧 (Tech Stack)

* **邊緣運算核心**：`Raspberry Pi` / `Python`
* **AI 影像辨識**：`MobileNet SSD` (深度學習物件偵測模型)
* **微控制器與感測**：`ESP32` / `空間光敏陣列` / `微型伺服馬達` / `PIR 紅外線感測器`
* **通訊與前端**：`MQTT (HiveMQ Broker)` / `HTML` / `JavaScript` (Serverless WebSocket)

---

## ✨ 系統核心亮點

### 1. 分散式架構與 MQTT 通訊
徹底拆分感測端 (ESP32) 與核心運算端 (樹莓派)。透過雲端 HiveMQ Broker 實現跨裝置通訊，大幅提升系統擴充性與部署彈性。

### 2. 邊緣 AI 與多幀驗證防呆
於邊緣端運行 MobileNet SSD 進行人形偵測，並實作連拍驗證機制（2 張影像中需有 1 張判定為人），有效過濾動物或衣物造成的偽陽性誤報。

### 3. 智慧照明與防衝突機制
結合 PIR 偵測與光敏電阻判斷，實現「有人且暗時自動開燈」。並設計 `manual_override` 防衝突機制，當接收遠端手動指令後，自動暫停感測 60 秒，確保使用者體驗。

### 4. 物理驅動降低部署門檻
透過 ESP32 輸出 PWM 訊號控制伺服馬達轉臂，「物理驅動」實體燈管開關，避開高成本與高風險的電路改線工程。

### 5. 無伺服器 (Serverless) 監控前端
監控儀表板採純靜態 HTML/JS 撰寫，透過 MQTT.js WebSocket 直連雲端 Broker，達成極低延遲的即時連線，且無須額外建置後端伺服器。

---

## 📂 系統架構與實作報告

### 💡 完整系統規格書
本專案的完整資料流程圖、MQTT Topic 設計格式（包含 Payload 範例）、硬體接線配置與測試成果，請參閱本儲存庫內附之 PDF 報告。

👉 **[📄 點擊查看：AIoT 智慧安防與環境感測系統_完整實作報告.pdf](https://drive.google.com/file/d/1iZCVn5eixFR19OWdjDlvM9Zd0QW38sR9/view?usp=sharing)**
