"""ESP32 MicroPython 設定檔"""

# --- WiFi ---
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# --- MQTT (HiveMQ Cloud) ---
MQTT_BROKER = "your-cluster.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "your_username"
MQTT_PASSWORD = "your_password"
MQTT_CLIENT_ID = "esp32-light"
MQTT_USE_SSL = True

# --- MQTT Topics ---
TOPIC_SENSOR_LIGHT = "home/sensor/light"
TOPIC_LIGHT_STATUS = "home/light/status"
TOPIC_LIGHT_CONTROL = "home/light/control"

# --- GPIO Pin ---
LDR_PIN = 34      # 光敏電阻（ADC）
LED_PIN = 2       # LED 輸出

# --- 閾值 ---
LIGHT_THRESHOLD = 1000  # 亮度閾值（ADC 值 0-4095，越小越暗）
PUBLISH_INTERVAL = 5    # MQTT 發布間隔（秒）
