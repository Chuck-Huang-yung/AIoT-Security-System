# AIoT 智慧安防與環境感測系統

> 基於 Raspberry Pi + ESP32 的人體偵測、即時監控與自動照明控制平台

---

## 1. 專題動機與目的

隨著 IoT 技術普及，智慧家庭安防成為重要應用領域。本專題結合 **AI 影像辨識**與 **IoT 感測技術**，打造一套智慧化安防系統。

### 三大核心功能

| 功能 | 說明 |
|------|------|
| 入侵偵測與警報 | PIR 偵測人體 → 攝影機拍照 → MobileNet SSD 辨識 → Discord 即時通知 |
| 環境自動照明 | 光敏電阻判斷亮度 → PIR 偵測有人且環境暗 → 自動開燈（供攝影機夜間辨識） |
| Web 即時監控 | MQTT.js 直連雲端 Broker → 即時數據 + 遠端燈光控制 + PIR 狀態顯示 |

---

## 2. 系統架構

```
┌─────────────────┐          ┌──────────────────┐          ┌─────────────────┐
│   ESP32 端       │  MQTT   │  HiveMQ Cloud    │  MQTT   │   Raspberry Pi  │
│  (MicroPython)  │ ──────► │  MQTT Broker     │ ──────► │   (Python)      │
│                 │         │  (雲端)           │         │                 │
│ ● PIR 感測器    │         │ ● TLS (8883)     │         │ ● USB Webcam    │
│ ● 光敏電阻(LDR)│         │ ● WSS (8884)     │         │ ● OpenCV DNN    │
│ ● LED 照明     │         │                  │         │ ● Discord 通知  │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                    │
                                    │ WSS
                                    ▼
                            ┌──────────────────┐
                            │  Web Dashboard   │
                            │ (Tailwind + MQTT)│
                            │                  │
                            │ ● 即時截圖       │
                            │ ● PIR 狀態       │
                            │ ● 亮度數據       │
                            │ ● 燈光控制       │
                            │ ● 警報記錄       │
                            │ ● 系統狀態       │
                            └──────────────────┘
```

### 資料流程

```
ESP32 PIR 偵測到移動
  → MQTT 發布 home/security/pir
    → RPi 收到觸發訊號
      → USB Webcam 連拍 3 張
        → MobileNet SSD 人形辨識（至少 2/3 通過）
          → 偵測到人形
            → MQTT 發布警報 + 截圖
            → Discord Webhook 推播（含截圖）
            → Dashboard 即時顯示

ESP32 同時判斷：
  PIR=1 且 LDR 值 < 閾值（暗）→ 自動開燈（供攝影機夜間使用）
  PIR=0 → 自動關燈
```

---

## 3. 硬體配置

### Raspberry Pi 端

| 元件 | 說明 | 接線 |
|------|------|------|
| Raspberry Pi 4 Model B | 安防主控 | - |
| USB Webcam (Logitech C270) | 影像擷取 | USB |

### ESP32 端

| 元件 | 說明 | 接線 |
|------|------|------|
| ESP32-WROOM-32 | 照明 + PIR 主控 | - |
| PIR 紅外線感測器 (HW-456 SR505) | 人體偵測 | OUT → GPIO 27, VCC → 5V, GND → GND |
| 光敏電阻 (LDR) | 環境亮度感測 | 一端 → 3.3V, 另一端 → GPIO 34 + 10K 下拉電阻 |
| LED | 照明輸出 | 長腳 → GPIO 2（經電阻）, 短腳 → GND |

---

## 4. MQTT 通訊設計

**Broker**：HiveMQ Cloud（免費方案）
- TLS 加密：port 8883（裝置端）
- WSS 連線：port 8884（前端 Dashboard）

### Topic 設計

| Topic | 發布者 | 訂閱者 | Payload 範例 | 說明 |
|-------|--------|--------|-------------|------|
| `home/security/pir` | ESP32 | RPi, Dashboard | `{"triggered": true, "timestamp": 12345}` | PIR 觸發訊號 |
| `home/security/alert` | RPi | Dashboard | `{"timestamp": "...", "confidence": 0.85}` | 入侵警報 |
| `home/security/snapshot` | RPi | Dashboard | `{"timestamp": "...", "image": "<Base64>"}` | 截圖影像 |
| `home/sensor/light` | ESP32 | Dashboard | `{"value": 2048}` | 環境亮度 ADC |
| `home/light/status` | ESP32 | Dashboard | `{"status": "on"}` | 燈光狀態 |
| `home/light/control` | Dashboard | ESP32 | `{"action": "on"}` | 遠端控燈 |
| `home/system/status` | RPi | Dashboard | `{"cpu_temp": 45, "uptime": "2h 30m"}` | 系統狀態 |

---

## 5. 軟體技術棧

### Raspberry Pi 端 (Python)

| 技術 | 用途 |
|------|------|
| Python 3 | 主程式語言 |
| OpenCV DNN (MobileNet SSD) | 人形偵測（深度學習模型） |
| paho-mqtt v2 | MQTT Client（TLS 加密） |
| requests | Discord Webhook HTTP 請求 |
| threading | 多線程（安防 + 系統狀態） |

### ESP32 端 (MicroPython)

| 技術 | 用途 |
|------|------|
| MicroPython | 統一 Python 生態 |
| umqtt.simple | 輕量 MQTT Client（SSL） |
| machine.ADC | 光敏電阻類比讀取 |
| machine.Pin | GPIO 控制（PIR, LED） |

### 前端 / 雲端

| 技術 | 用途 |
|------|------|
| HiveMQ Cloud | MQTT Broker（免費，雲端） |
| MQTT.js | 前端 WebSocket 直連 Broker |
| Tailwind CSS | 現代深色主題 UI |
| Discord Webhook | 入侵警報推播通知 |

---

## 6. 核心程式碼

### 6.1 ESP32 — PIR + 光敏 + LED 控制

```python
# PIR 偵測 + 光敏判斷開燈邏輯
pir = Pin(27, Pin.IN, Pin.PULL_DOWN)
ldr = ADC(Pin(34))
led = Pin(2, Pin.OUT)

while True:
    ldr_value = ldr.read()
    pir_value = pir.value()

    if not manual_override:
        if pir_value == 1:
            # 有人 + 暗 → 開燈（供攝影機夜間辨識）
            if ldr_value < LIGHT_THRESHOLD:
                led.value(1)
        else:
            # 沒人 → 關燈
            led.value(0)

    # PIR 觸發 → 發 MQTT 通知 RPi 拍照
    if pir_value == 1 and (now - last_pir_time >= PIR_COOLDOWN):
        mqtt_client.publish("home/security/pir",
                           json.dumps({"triggered": True}))
```

### 6.2 RPi — 安防主迴圈（MQTT 觸發）

```python
def security_loop():
    """等待 ESP32 PIR 觸發 → 攝影機 → OpenCV → Discord"""
    capture.init()

    while running:
        if pir_triggered.wait(timeout=1):  # 等待 MQTT PIR 訊號
            pir_triggered.clear()

            # 多幀驗證：連拍 3 張，至少 2 張偵測到人
            detect_count = 0
            for attempt in range(3):
                frame = capture.capture_frame()
                detected, boxes, confidence = detector.detect_person(frame)
                if detected:
                    detect_count += 1

            if detect_count >= 2:
                # 截圖 + MQTT 警報 + Discord 通知
                discord_bot.send_alert(
                    f"偵測到入侵！信心值: {confidence:.0%}",
                    image_base64=img_base64,
                )
            time.sleep(15)  # 冷卻
```

### 6.3 OpenCV DNN — MobileNet SSD 人形偵測

```python
# 載入預訓練模型
net = cv2.dnn.readNetFromCaffe("deploy.prototxt",
                                "mobilenet_ssd.caffemodel")

def detect_person(frame):
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        0.007843, (300, 300), 127.5
    )
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        class_id = int(detections[0, 0, i, 1])
        confidence = float(detections[0, 0, i, 2])
        # class_id 15 = person
        if class_id == 15 and confidence > 0.5:
            return True, boxes, confidence
```

### 6.4 Discord Webhook — 帶截圖警報

```python
def send_alert(message, image_base64):
    embed = {
        "title": "入侵警報",
        "description": message,
        "color": 0xFF0000,
        "image": {"url": "attachment://snapshot.jpg"},
    }
    # multipart/form-data 上傳圖片
    files = {
        "payload_json": (None, json.dumps({"embeds": [embed]})),
        "files[0]": ("snapshot.jpg", BytesIO(image_data)),
    }
    requests.post(DISCORD_WEBHOOK_URL, files=files)
```

---

## 7. Web Dashboard

純靜態 HTML/JS，透過 MQTT.js (WSS) 直連 HiveMQ Cloud，無需後端伺服器。

### 功能模組

| 模組 | 訂閱/發布 | 說明 |
|------|----------|------|
| PIR 感測器 | subscribe `home/security/pir` | 即時顯示 PIR 狀態（0/1），偵測到移動時紅色警示 |
| 即時截圖 | subscribe `home/security/snapshot` | Base64 圖片即時渲染 |
| 警報事件 | subscribe `home/security/alert` | 入侵警報列表 |
| 環境亮度 | subscribe `home/sensor/light` | ESP32 ADC 即時數據 |
| 燈光控制 | publish `home/light/control` | 手動開/關燈按鈕（60 秒覆蓋自動模式） |
| 系統狀態 | subscribe `home/system/status` | RPi CPU 溫度、運行時間 |

---

## 8. 專案目錄結構

```
AIOT_final/
├── config.py                  # RPi 設定檔（MQTT、GPIO、Discord）
├── main.py                    # RPi 主程式入口
├── .env                       # 敏感資訊（MQTT 密碼、Webhook URL）
│
├── camera/
│   ├── capture.py             # 攝影機擷取（OpenCV）
│   ├── detector.py            # MobileNet SSD 人形偵測
│   └── model/
│       ├── deploy.prototxt    # 模型定義
│       └── mobilenet_ssd.caffemodel  # 預訓練權重
│
├── mqtt/
│   └── client.py              # MQTT 連線封裝（paho-mqtt v2）
│
├── notify/
│   └── discord_bot.py         # Discord Webhook 通知
│
├── web/
│   └── index.html             # Dashboard（Tailwind + MQTT.js）
│
├── esp32/                     # ESP32 MicroPython
│   ├── boot.py                # WiFi 自動連線
│   ├── main.py                # PIR + 光敏 + LED + MQTT
│   ├── config.py              # ESP32 設定
│   └── lib/
│       └── umqtt_simple.py    # MQTT 函式庫
│
└── snapshots/                 # 截圖儲存目錄
```

---

## 9. 開發過程與問題解決

| 問題 | 原因 | 解決方案 |
|------|------|---------|
| PIR 持續誤觸發 | GPIO 浮接導致持續高電位 | 加入 pull-down 電阻 + 軟體冷卻機制（15 秒） |
| picamera2 與 USB Webcam 衝突 | picamera2 用 libcamera 開啟 USB Webcam 導致凍結 | 硬編碼使用 OpenCV VideoCapture |
| ESP32 ussl 模組更名 | MicroPython v1.25 將 ussl 更名為 ssl | umqtt_simple.py 加入 try/except 相容處理 |
| Haar Cascade 把衣服誤判為人 | upperbody 偵測器誤報率高 | 改用 MobileNet SSD 深度學習模型，精準度大幅提升 |
| 手動控燈被自動覆蓋 | 自動模式立即覆蓋手動操作 | 加入 manual_override 機制，手動控制後暫停自動 60 秒 |
| WiFi WPA3 不相容 | RPi/ESP32 無法連線 WPA3 熱點 | 手機端改用 WPA2 安全性設定 |
| PIR 與攝影機位置衝突 | PIR 和攝影機放一起，角度難以兼顧 | PIR 移至 ESP32 端，透過 MQTT 遠端觸發 RPi 攝影機 |
| 攝影機角度拍到天花板 | USB Webcam 未固定 | 調整並固定 Webcam 角度朝向走道方向 |

---

## 10. 系統成果

### 安防偵測完整流程
ESP32 PIR 偵測人體移動 → MQTT 觸發 RPi → 攝影機連拍 3 張 → MobileNet SSD 多幀驗證（2/3 通過）→ MQTT 發布警報 → Discord 推播通知（含入侵截圖）

### 智慧照明控制
PIR 偵測到有人 + 光敏電阻判斷環境暗 → 自動開燈供攝影機夜間辨識。無人時自動關燈。Dashboard 可手動控制（60 秒覆蓋）。

### Web 即時監控
MQTT.js 透過 WSS 直連 HiveMQ Cloud，純靜態網頁無需後端。即時顯示 PIR 狀態、截圖、亮度數據、燈光控制、系統狀態。

### 雲端分散式架構
RPi + ESP32 雙裝置透過 HiveMQ Cloud 協同運作。PIR 在 ESP32 端偵測，攝影機在 RPi 端拍照辨識，兩者透過 MQTT 解耦。支援外網存取，手機可即時收到 Discord 警報。

### 開機自動啟動
RPi 使用 systemd service，開機自動啟動安防系統。異常退出 10 秒後自動重啟。

---

## 11. 技術總結

| 項目 | 技術選型 |
|------|---------|
| 安防主控 | Raspberry Pi 4 + Python |
| 感測主控 | ESP32 + MicroPython |
| 人形偵測 | OpenCV DNN + MobileNet SSD (Caffe) |
| 通訊協定 | MQTT over TLS / WSS |
| 雲端 Broker | HiveMQ Cloud（免費） |
| 推播通知 | Discord Webhook（Embed + 圖片附件） |
| 前端 | Tailwind CSS + MQTT.js（純靜態） |
| 部署 | systemd 開機自啟動 |
