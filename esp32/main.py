"""ESP32 主程式 — 光敏感測器 + LED 自動控制 + MQTT"""

import json
import time
from machine import Pin, ADC

import config

# --- 硬體初始化 ---
ldr = ADC(Pin(config.LDR_PIN))
ldr.atten(ADC.ATTN_11DB)  # 量測範圍 0-3.3V，ADC 值 0-4095

led = Pin(config.LED_PIN, Pin.OUT)
led.value(0)

led_status = "off"
manual_override = False  # 手動控制時暫停自動模式
manual_override_time = 0  # 手動控制時間戳
MANUAL_OVERRIDE_DURATION = 60  # 手動控制持續 60 秒後恢復自動


# --- MQTT 連線 ---
def connect_mqtt():
    """連線到 HiveMQ Cloud MQTT Broker"""
    from lib.umqtt_simple import MQTTClient

    client = MQTTClient(
        client_id=config.MQTT_CLIENT_ID,
        server=config.MQTT_BROKER,
        port=config.MQTT_PORT,
        user=config.MQTT_USERNAME,
        password=config.MQTT_PASSWORD,
        ssl=config.MQTT_USE_SSL,
    )
    client.set_callback(on_message)
    client.connect()
    client.subscribe(config.TOPIC_LIGHT_CONTROL)
    print(f"[MQTT] 已連線，訂閱 {config.TOPIC_LIGHT_CONTROL}")
    return client


def on_message(topic, msg):
    """處理收到的 MQTT 控燈指令"""
    global led_status
    topic = topic.decode()
    try:
        payload = json.loads(msg.decode())
    except (ValueError, UnicodeError):
        return

    if topic == config.TOPIC_LIGHT_CONTROL:
        action = payload.get("action", "")
        if action == "on":
            led.value(1)
            led_status = "on"
            manual_override = True
            manual_override_time = time.time()
            print("[LED] 手動開燈")
        elif action == "off":
            led.value(0)
            led_status = "off"
            manual_override = True
            manual_override_time = time.time()
            print("[LED] 手動關燈")
        elif action == "auto":
            manual_override = False
            print("[LED] 恢復自動模式")
        publish_light_status(mqtt_client)


def publish_light_data(client, ldr_value):
    """發布亮度數據"""
    payload = json.dumps({"value": ldr_value})
    client.publish(config.TOPIC_SENSOR_LIGHT, payload)


def publish_light_status(client):
    """發布燈光狀態"""
    payload = json.dumps({"status": led_status})
    client.publish(config.TOPIC_LIGHT_STATUS, payload)


# --- 主迴圈 ---
print("[系統] ESP32 照明線路啟動")
mqtt_client = connect_mqtt()

while True:
    try:
        # 讀取光敏電阻 ADC 值（0-4095，值越小越暗）
        ldr_value = ldr.read()

        # 手動覆蓋超時，恢復自動模式
        if manual_override and (time.time() - manual_override_time > MANUAL_OVERRIDE_DURATION):
            manual_override = False
            print("[LED] 手動控制超時，恢復自動模式")

        # 自動控制 LED（手動模式下不執行）
        if not manual_override:
            if ldr_value < config.LIGHT_THRESHOLD:
                if led_status == "off":
                    led.value(1)
                    led_status = "on"
                    print(f"[LED] 自動開燈（亮度: {ldr_value}）")
                    publish_light_status(mqtt_client)
            else:
                if led_status == "on":
                    led.value(0)
                    led_status = "off"
                    print(f"[LED] 自動關燈（亮度: {ldr_value}）")
                    publish_light_status(mqtt_client)

        # 定時發布亮度數據
        publish_light_data(mqtt_client, ldr_value)

        # 每秒檢查 MQTT 訊息，每 PUBLISH_INTERVAL 秒發布數據
        for _ in range(config.PUBLISH_INTERVAL):
            mqtt_client.check_msg()
            time.sleep(1)

    except OSError as e:
        print(f"[錯誤] {e}，嘗試重新連線...")
        time.sleep(5)
        mqtt_client = connect_mqtt()
