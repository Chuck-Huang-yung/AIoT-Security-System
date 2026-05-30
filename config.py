"""RPi 端設定檔"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- MQTT (HiveMQ Cloud) ---
MQTT_BROKER = os.getenv("MQTT_BROKER", "")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_USE_TLS = True

# --- MQTT Topics ---
TOPIC_SECURITY_ALERT = "home/security/alert"
TOPIC_SECURITY_SNAPSHOT = "home/security/snapshot"
TOPIC_SECURITY_PIR = "home/security/pir"
TOPIC_SENSOR_LIGHT = "home/sensor/light"
TOPIC_LIGHT_STATUS = "home/light/status"
TOPIC_LIGHT_CONTROL = "home/light/control"
TOPIC_SYSTEM_STATUS = "home/system/status"

# --- Discord ---
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# --- GPIO Pin（RPi）---
PIR_PIN = 17  # PIR 紅外線感測器

# --- OpenCV ---
JPEG_QUALITY = 70  # 截圖壓縮品質 (0-100)

# --- 系統 ---
SYSTEM_STATUS_INTERVAL = 30  # 系統狀態發布間隔（秒）
