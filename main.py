"""RPi 主程式 — 整合安防線路 + Discord 通知 + 系統狀態"""

import json
import signal
import sys
import threading
import time
from datetime import datetime

import config
from mqtt.client import MQTTClient
from sensors import pir
from camera import capture, detector
from notify import discord_bot


mqtt_client = MQTTClient()
running = True


def security_loop():
    """安防線路：PIR 偵測 → 攝影機 → OpenCV → MQTT + Discord"""
    print("[安防] 線路啟動")

    pir.setup()
    capture.init()

    while running:
        if pir.detect():
            print("[安防] PIR 偵測到移動！")
            frame = capture.capture_frame()
            if frame is None:
                time.sleep(1)
                continue

            detected, boxes, confidence = detector.detect_person(frame)

            if detected:
                print(f"[安防] 偵測到人形！信心值: {confidence:.2f}")

                # 繪製偵測框並截圖
                frame = detector.draw_boxes(frame, boxes)
                img_base64 = capture.capture_to_base64(frame)
                capture.save_snapshot(frame)

                timestamp = datetime.now().isoformat()

                # MQTT 發布警報
                mqtt_client.publish(config.TOPIC_SECURITY_ALERT, {
                    "timestamp": timestamp,
                    "confidence": round(confidence, 2),
                })

                # MQTT 發布截圖
                mqtt_client.publish(config.TOPIC_SECURITY_SNAPSHOT, {
                    "timestamp": timestamp,
                    "image": img_base64,
                })

                # Discord 通知
                discord_bot.send_alert(
                    f"偵測到入侵！信心值: {confidence:.0%}",
                    image_base64=img_base64,
                )

                # 冷卻時間，SR505 不可重觸發延遲約 8 秒
                time.sleep(8)
            else:
                time.sleep(0.5)
        else:
            time.sleep(0.5)


def system_status_loop():
    """定時發布系統狀態"""
    print("[系統] 狀態發布啟動")

    while running:
        try:
            # 讀取 CPU 溫度（RPi）
            try:
                with open("/sys/class/thermal/thermal_zone0/temp") as f:
                    cpu_temp = round(int(f.read().strip()) / 1000, 1)
            except FileNotFoundError:
                cpu_temp = 0

            # 讀取 uptime
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


def on_light_control(topic, payload):
    """處理來自 Dashboard 的控燈指令（轉發，實際控制在 ESP32）"""
    print(f"[MQTT] 收到控燈指令: {payload}")


def shutdown(signum, frame):
    """優雅關閉"""
    global running
    print("\n[系統] 正在關閉...")
    running = False
    capture.release()
    pir.cleanup()
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

    # 訂閱控燈指令（監聽用，實際控制在 ESP32）
    mqtt_client.subscribe(config.TOPIC_LIGHT_CONTROL, on_light_control)

    # 啟動 Discord 上線通知
    discord_bot.send_status("RPi 安防系統已上線")

    # 啟動安防線路
    security_thread = threading.Thread(target=security_loop, daemon=True)
    security_thread.start()

    # 啟動系統狀態發布
    status_thread = threading.Thread(target=system_status_loop, daemon=True)
    status_thread.start()

    print("[系統] 所有線路已啟動，按 Ctrl+C 停止")

    # 主迴圈保持程式運行
    while running:
        time.sleep(1)


if __name__ == "__main__":
    main()
