# AIoT 智慧安防與環境感測系統 📡

本專案結合「架構解耦 (Decoupling)」與「邊緣運算 (Edge AI)」思維，打造針對校園天台生態園與戶外大型場域設計的人形辨識與智慧安防系統。

## 🛠️ 技術棧 (Tech Stack)
* **邊緣運算核心：** Raspberry Pi, Python
* **AI 影像辨識：** MobileNet SSD
* **微控制器與感測：** ESP32, 空間光敏陣列, 微型伺服馬達
* **通訊與前端：** MQTT (HiveMQ Broker), HTML/JS (Serverless WebSocket)

## ✨ 系統核心亮點
* **分散式架構與 MQTT 通訊：** 徹底拆分感測端 (ESP32) 與核心運算端 (樹莓派)，透過雲端 HiveMQ Broker 實現跨裝置通訊，大幅提升系統擴充性與部署彈性。
* **邊緣 AI 與多幀驗證防呆：** 於邊緣端運行 MobileNet SSD 進行人形偵測，並實作連拍驗證機制（2 張影像中需有 1 張判定為人），有效過濾動物或衣物造成的偽陽性誤報。
* **多感測器融合 (Sensor Fusion)：** 透過多節點 ESP32 採集各角落光敏數據計算平均值，消弭單一感測器死角；並以 PWM 訊號控制伺服馬達轉臂，「物理驅動」實體燈管，避開高成本與高風險的電路改線工程。
* **無伺服器 (Serverless) 監控前端：** 監控儀表板採純靜態 HTML/JS 撰寫，透過 MQTT.js WebSocket 直連雲端 Broker，達成極低延遲的即時連線，且無須額外建置後端伺服器。
