# 📡 AIoT 智慧安防與環境感測系統 
**(AIoT Smart Security & Environment Sensing System)**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Edge%20AI-C51A4A?logo=raspberry-pi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-MicroPython-E7352C?logo=espressif&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-HiveMQ-660066?logo=mqtt&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-MobileNet%20SSD-5C3EE8?logo=opencv&logoColor=white)

---

## 💡專案簡介
> 本專案初衷源於「校園天台生態園」的夜間管理痛點。為解決戶外缺乏照明、長明燈耗能及防盜監控需求，本系統結合「架構解耦 (Decoupling)」與「邊緣運算 (Edge AI)」思維，打造「人走過即亮」並同步啟動 AI 人形辨識的智慧安防系統。
>
> 本架構目前已於教室場域完成概念驗證 (PoC) 與初步實作，具備高擴充性，未來可無痛導入大型「畜牧業與農田」等規模化場域。

---

## ⚡開發角色與核心貢獻 
 * **團隊規模：** 5 人專題團隊
 * **我的核心負責項目：** 擔任**系統整合與前端監控頁面設計**
   * 負責導入 MQTT 雲端通訊協定（HiveMQ）。
   * 打通 ESP32 微控制器與樹莓派邊緣運算端的雙向溝通。
   * 開發 Serverless Web Dashboard，實現跨網域即時監控與遠端硬體防衝突控制。

---

## 🛠️ 技術棧 
* **邊緣運算與 AI (Raspberry Pi)：** Python 3, OpenCV, MobileNet SSD (Caffe Model)
* **微控制器與感測 (ESP32)：** MicroPython, PWM 伺服馬達控制, ADC 類比訊號處理
* **通訊協定與雲端：** MQTT (HiveMQ Cloud Broker), TLS/SSL 加密連線
* **前端與警報：** Serverless Web Dashboard (HTML/JS + MQTT.js), Discord Webhook
  
---

## 📂 專案模組化結構 
```text
AIoT_Smart_Security/
├── esp32/                  # ESP32 微控制器端 (MicroPython)
│   ├── boot.py             # WiFi 自動連線腳本
│   └── main.py             # PIR、光敏、微型馬達與 MQTT 通訊主邏輯
├── camera/                 # 視覺與 AI 辨識模組
│   ├── capture.py          # OpenCV 影像擷取
│   └── detector.py         # MobileNet SSD 人形偵測核心
├── model/                  # 深度學習模型檔
│   ├── deploy.prototxt     # 模型結構定義
│   └── mobilenet_ssd.caffemodel # 預訓練權重
├── mqtt/                   # 雲端通訊模組
│   └── client.py           # MQTT 連線封裝 (TLS 加密)
├── notify/                 # 警報模組
│   └── discord_bot.py      # Discord Webhook 即時影像推播
├── web/                    # Serverless 監控前端
│   └── index.html          # Tailwind CSS + MQTT.js 即時儀表板
├── config.py               # 系統全域設定檔
└── main.py                 # Raspberry Pi 邊緣運算主程式入口
```

---

## ✨ 系統核心亮點與深度技術解析 

### 1. 分散式架構與 MQTT 跨裝置通訊 (Decoupling)
屏除傳統單一開發板全包的作法，將「感測控制端 (ESP32)」與「核心運算端 (樹莓派)」徹底物理分離。
* **輕量化通訊：** 雙端透過雲端 HiveMQ Broker 溝通，定義了清晰的 Topic 結構（如 `home/security/pir` 觸發警報、`home/light/control` 遠端控燈）。
* **高擴充性：** 支援「多點部署」，未來只需增加 ESP32 節點，即可採集各角落數據計算平均值（Sensor Fusion），準確掌握大場域真實亮度。

### 2. 邊緣 AI 影像辨識與「多幀防呆」機制
捨棄傳統 PIR 感測器容易受動物或風吹草動誤觸的缺點，導入 AI 進行二次特徵萃取。
* **深度學習模型：** 於邊緣端 (Raspberry Pi) 運行 MobileNet SSD 模型進行人形偵測，降低雲端運算延遲與頻寬消耗。
* **防抖動驗證邏輯：** 實作連拍驗證機制（2 張影像中需有 1 張信心值 > 0.5 判定為人），有效過濾偽陽性誤報。

### 3. 軟硬整合：硬體防浮接與手/自動防衝突機制
真正落地的 IoT 系統必須考量物理環境的極端狀況與使用者體驗：
* **硬體除錯：** 針對 PIR 感測器持續誤觸發問題，透過硬體配置 Pull-down 電阻搭配軟體冷卻時間（Cooldown）徹底解決 GPIO 浮接問題。
* **狀態機防衝突：** 系統預設為「有人且暗」自動開燈，但若使用者透過儀表板「手動」切換燈光，系統會啟動 `manual_override` 防衝突機制，暫停自動感測 60 秒，避免手自動邏輯互相覆蓋。
* **微型馬達實體控燈：** 透過 ESP32 輸出 PWM 訊號控制伺服馬達轉臂，以「物理按壓」方式直接驅動傳統電燈開關，避開高風險且高成本的電路改線工程。

### 4. 無伺服器 (Serverless) 監控與即時警報
* **極低延遲儀表板：** Web 監控介面採純靜態 HTML/JS 撰寫，透過 MQTT.js WebSocket (WSS) 直連雲端 Broker。無需額外建置後端伺服器，即可達成即時亮度顯示、PIR 狀態更新與遠端控燈。
* **Discord 即時推播：** 當樹莓派確認入侵事件後，透過 Discord Webhook 結合 `multipart/form-data` 協定，將 Base64 轉換後的現場截圖與信心值即時推播至管理員手機。

---

## 🔌 硬體接線與腳位配置 

**ESP32-WROOM-32 (感測與控制節點)**
* `GPIO 27 (IN)`: PIR 紅外線人體感測器 (配置下拉電阻)
* `GPIO 34 (ADC)`: 光敏電阻 (LDR) 採集環境亮度 (0-4095)
* `GPIO 2 (PWM)`: 微型伺服馬達訊號線 (頻率 50Hz 控制物理開關)

**Raspberry Pi 4B (邊緣運算節點)**
* `USB 埠`: Logitech C270 網路攝影機

---

## 📂 完整系統規格與實作報告

> **💡 深入了解系統分析與設計**
> 包含完整的資料流程圖、MQTT Payload 格式定義、開發踩坑紀錄與未來展望，請參閱下方之完整專案企劃書。

[📄 點擊查看：黃俊洋_軟硬整合與物聯網_AIoT智慧安防與環境感測系統.pdf](https://drive.google.com/file/d/1iZCVn5eixFR19OWdjDlvM9Zd0QW38sR9/view?usp=sharing) 
