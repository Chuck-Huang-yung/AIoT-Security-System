"""MQTT 連線模組 — 封裝 HiveMQ Cloud TLS 連線、publish、subscribe"""

import json
import ssl
import paho.mqtt.client as mqtt

import config


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(
            client_id="rpi-main",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        )
        self.client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)

        if config.MQTT_USE_TLS:
            self.client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        self._subscriptions = {}

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("[MQTT] 已連線到 Broker")
            for topic in self._subscriptions:
                self.client.subscribe(topic)
                print(f"[MQTT] 已訂閱 {topic}")
        else:
            print(f"[MQTT] 連線失敗，代碼: {rc}")

    def _on_disconnect(self, client, userdata, flags, rc, properties=None):
        print(f"[MQTT] 已斷線，代碼: {rc}")

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        try:
            payload = json.loads(msg.payload.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = msg.payload

        if topic in self._subscriptions:
            self._subscriptions[topic](topic, payload)

    def connect(self):
        """連線到 MQTT Broker"""
        print(f"[MQTT] 正在連線 {config.MQTT_BROKER}:{config.MQTT_PORT}...")
        self.client.connect(config.MQTT_BROKER, config.MQTT_PORT, keepalive=60)
        self.client.loop_start()

    def disconnect(self):
        """斷開連線"""
        self.client.loop_stop()
        self.client.disconnect()
        print("[MQTT] 已斷開連線")

    def publish(self, topic, payload):
        """發布訊息（自動轉 JSON）"""
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        result = self.client.publish(topic, payload)
        result.wait_for_publish()

    def subscribe(self, topic, callback):
        """訂閱 topic 並綁定回調函式"""
        self._subscriptions[topic] = callback
        if self.client.is_connected():
            self.client.subscribe(topic)
