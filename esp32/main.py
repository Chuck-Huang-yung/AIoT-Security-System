"""ESP32 主程式 — PIR 偵測 + 光敏判斷開燈 + MQTT"""

import json
import time
from machine import Pin, ADC

import config

# --- 硬體初始化 ---
ldr = ADC(Pin(config.LDR_PIN))
ldr.atten(ADC.ATTN_11DB)  # 量測範圍 0-3.3V，ADC 值 0-4095

led = Pin(config.LED_PIN, Pin.OUT)
led.value(0)

pir = Pin(config.PIR_PIN, Pin.IN, Pin.PULL_DOWN)

led_status = "off"
manual_override = False
manual_override_time = 0
MANUAL_OVERRIDE_DURATION = 60

PIR_COOLDOWN = 10
last_pir_time = 0
last_publish_time = 0


# --- MQTT 連線 ---
def connect_mqtt():
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
    global led_status, manual_override, manual_override_time
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
    payload = json.dumps({"value": ldr_value})
    client.publish(config.TOPIC_SENSOR_LIGHT, payload)


def publish_light_status(client):
    payload = json.dumps({"status": led_status})
    client.publish(config.TOPIC_LIGHT_STATUS, payload)


def set_led(client, on):
    """控制 LED 並發布狀態"""
    global led_status
    if on and led_status == "off":
        led.value(1)
        led_status = "on"
        print("[LED] 自動開燈（PIR + 暗）")
        publish_light_status(client)
    elif not on and led_status == "on":
        led.value(0)
        led_status = "off"
        print("[LED] 自動關燈（無人）")
        publish_light_status(client)


# --- 主迴圈 ---
print("[系統] ESP32 PIR + 照明線路啟動")
mqtt_client = connect_mqtt()

while True:
    try:
        ldr_value = ldr.read()
        pir_value = pir.value()
        now = time.time()

        # 手動覆蓋超時，恢復自動
        if manual_override and (now - manual_override_time > MANUAL_OVERRIDE_DURATION):
            manual_override = False
            print("[LED] 手動控制超時，恢復自動模式")

        # 自動控制（手動模式下跳過）
        if not manual_override:
            if pir_value == 1:
                # 有人 + 暗 → 開燈
                if ldr_value < config.LIGHT_THRESHOLD:
                    set_led(mqtt_client, True)
                # 有人 + 亮 → 不需要開燈
            else:
                # 沒人 → 關燈
                set_led(mqtt_client, False)

        # PIR 觸發 → 發 MQTT 通知 RPi 拍照
        if pir_value == 1 and (now - last_pir_time >= PIR_COOLDOWN):
            last_pir_time = now
            print("[PIR] 偵測到移動！發布 MQTT")
            payload = json.dumps({"triggered": True, "timestamp": now})
            mqtt_client.publish(config.TOPIC_SECURITY_PIR, payload)

        # 定時發布亮度數據
        if now - last_publish_time >= config.PUBLISH_INTERVAL:
            last_publish_time = now
            publish_light_data(mqtt_client, ldr_value)

        # 每秒檢查 MQTT 訊息
        mqtt_client.check_msg()
        time.sleep(1)

    except OSError as e:
        print(f"[錯誤] {e}，嘗試重新連線...")
        time.sleep(5)
        mqtt_client = connect_mqtt()
