"""ESP32 啟動腳本 — WiFi 連線"""

import network
import time

import config


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("[WiFi] 已連線")
        print(f"[WiFi] IP: {wlan.ifconfig()[0]}")
        return wlan

    print(f"[WiFi] 正在連線 {config.WIFI_SSID}...")
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
        print(".", end="")

    if wlan.isconnected():
        print(f"\n[WiFi] 已連線，IP: {wlan.ifconfig()[0]}")
    else:
        print("\n[WiFi] 連線失敗，重啟中...")
        import machine
        machine.reset()

    return wlan


wlan = connect_wifi()
