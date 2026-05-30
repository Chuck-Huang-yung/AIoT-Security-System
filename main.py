"""RPi 主程式 — 整合安防線路 + Discord 通知 + 系統狀態"""

import json
import signal
import sys
import threading
import time
from datetime import datetime

import config
from mqtt.client import MQTTClient
from camera import capture, detector
from notify import discord_bot


mqtt_client = MQTTClient()
running = True
pir_triggered = threading.Event()


def security_loop():
    """安防線路：等待 PIR MQTT 觸發 → 攝影機 → OpenCV → MQTT + Discord"""
    print("[安防] 線路啟動（等待 ESP32 PIR 觸發）")

    capture.init()
    COOLDOWN = 15

    while running:
        # 等待 ESP32 PIR 觸發訊號
        if pir_triggered.wait(timeout=1):
            pir_triggered.clear()
            print("[安防] 收到 PIR 觸發訊號！")

            # 多幀驗證：連拍 3 張，至少 2 張偵測到人才算
            detect_count = 0
            best_frame = None
            best_boxes = []
            best_confidence = 0

            for attempt in range(3):
                frame = capture.capture_frame()
                if frame is None:
                    continue
                detected, boxes, confidence = detector.detect_person(frame)
                if detected:
                    detect_count += 1
                    if confidence > best_confidence:
                        best_frame = frame
                        best_boxes = boxes
                        best_confidence = confidence
                time.sleep(0.3)

            if detect_count >= 2 and best_frame is not None:
                print(f"[安防] 偵測到人形！信心值: {best_confidence:.2f}（{detect_count}/3 幀通過）")

                best_frame = detector.draw_boxes(best_frame, best_boxes)
                img_base64 = capture.capture_to_base64(best_frame)
                capture.save_snapshot(best_frame)

                timestamp = datetime.now().isoformat()

                mqtt_client.publish(config.TOPIC_SECURITY_ALERT, {
                    "timestamp": timestamp,
                    "confidence": round(best_confidence, 2),
                })

                mqtt_client.publish(config.TOPIC_SECURITY_SNAPSHOT, {
                    "timestamp": timestamp,
                    "image": img_base64,
                })

                discord_bot.send_alert(
                    f"偵測到入侵！信心值: {best_confidence:.0%}",
                    image_base64=img_base64,
                )
            else:
                print(f"[安防] 未確認人形（{detect_count}/3 幀），忽略")

            # 強制冷卻
            time.sleep(COOLDOWN)


def system_status_loop():
    """定時發布系統狀態"""
    print("[系統] 狀態發布啟動")

    while running:
        try:
            try:
                with open("/sys/class/thermal/thermal_zone0/temp") as f:
                    cpu_temp = round(int(f.read().strip()) / 1000, 1)
            except FileNotFoundError:
                cpu_temp = 0

            try:
                with open("/proc/uptime") as f:
                    uptime_seconds = int(float(f.read().split()[0]))
                hours, remainder = divmod(uptime_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                uptime_str = f"{hours}h {minutes}m"
            except FileNotFoundError:
                uptime_str = "--"

            mqtt_client.publish(config.TOPIC_SYSTEM_STATUS, {
                "cpu_temp": cpu_temp,
                "uptime": uptime_str,
                "timestamp": datetime.now().isoformat(),
            })

        except Exception as e:
            print(f"[系統] 狀態發布錯誤: {e}")

        time.sleep(config.SYSTEM_STATUS_INTERVAL)


def on_pir_trigger(topic, payload):
    """收到 ESP32 PIR 觸發訊號"""
    print(f"[MQTT] 收到 PIR 觸發: {payload}")
    pir_triggered.set()


def on_light_control(topic, payload):
    """處理來自 Dashboard 的控燈指令（轉發，實際控制在 ESP32）"""
    print(f"[MQTT] 收到控燈指令: {payload}")


def shutdown(signum, frame):
    """優雅關閉"""
    global running
    print("\n[系統] 正在關閉...")
    running = False
    capture.release()
    mqtt_client.disconnect()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print("=" * 50)
    print("  AIoT 智慧安防系統 — RPi 端")
    print("=" * 50)

    # 連線 MQTT
    mqtt_client.connect()
    time.sleep(2)

    # 訂閱 ESP32 PIR 觸發訊號
    mqtt_client.subscribe(config.TOPIC_SECURITY_PIR, on_pir_trigger)

    # 訂閱控燈指令（監聽用）
    mqtt_client.subscribe(config.TOPIC_LIGHT_CONTROL, on_light_control)

    # Discord 上線通知
    discord_bot.send_status("RPi 安防系統已上線")

    # 啟動安防線路
    security_thread = threading.Thread(target=security_loop, daemon=True)
    security_thread.start()

    # 啟動系統狀態發布
    status_thread = threading.Thread(target=system_status_loop, daemon=True)
    status_thread.start()

    print("[系統] 所有線路已啟動，按 Ctrl+C 停止")

    while running:
        time.sleep(1)


if __name__ == "__main__":
    main()
