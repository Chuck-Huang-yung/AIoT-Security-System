"""ESP32 MicroPython 設定檔"""
"""範本設定格式"""

# --- WiFi ---
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# --- MQTT (HiveMQ Cloud) ---
MQTT_BROKER = "YOUR_BROKER_URL.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "YOUR_MQTT_USERNAME"
MQTT_PASSWORD = "YOUR_MQTT_PASSWORD"
MQTT_CLIENT_ID = "esp32-light"
MQTT_USE_SSL = True

# --- MQTT Topics ---
TOPIC_SENSOR_LIGHT = "home/sensor/light"
TOPIC_LIGHT_STATUS = "home/light/status"
TOPIC_LIGHT_CONTROL = "home/light/control"
TOPIC_SECURITY_PIR = "home/security/pir"

# --- GPIO Pin ---
LDR_PIN = 34      # 光敏電阻（ADC）
LED_PIN = 2       # LED 輸出
PIR_PIN = 27      # PIR 紅外線感測器

# --- 閾值 ---
LIGHT_THRESHOLD = 1000  # 亮度閾值（ADC 值 0-4095，越小越暗）
PUBLISH_INTERVAL = 5    # MQTT 發布間隔（秒）