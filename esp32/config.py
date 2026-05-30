"""ESP32 MicroPython 設定檔"""

# --- WiFi ---
WIFI_SSID = "奶昔是隻薩摩耶"
WIFI_PASSWORD = "123456789"

# --- MQTT (HiveMQ Cloud) ---
MQTT_BROKER = "068e8edd005b4906afea0dfa79bc96c7.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "aiot_final"
MQTT_PASSWORD = "a1234A1234"
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
