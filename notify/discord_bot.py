"""Discord Webhook 通知模組"""

import base64
import json
from datetime import datetime
from io import BytesIO

import requests

import config


def send_alert(message, image_base64=None):
    """發送警報通知到 Discord（含可選圖片）"""
    if not config.DISCORD_WEBHOOK_URL:
        print("[Discord] Webhook URL 未設定，跳過通知")
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    embed = {
        "title": "🚨 入侵警報",
        "description": message,
        "color": 0xFF0000,
        "timestamp": datetime.now().isoformat(),
        "footer": {"text": "AIoT 智慧安防系統"},
        "fields": [
            {"name": "時間", "value": timestamp, "inline": True},
        ],
    }

    if image_base64 and not image_base64.startswith("data:"):
        # 有圖片：用 multipart/form-data 上傳
        image_data = base64.b64decode(image_base64)
        embed["image"] = {"url": "attachment://snapshot.jpg"}

        payload = {"embeds": [embed]}
        files = {
            "payload_json": (None, json.dumps(payload), "application/json"),
            "files[0]": ("snapshot.jpg", BytesIO(image_data), "image/jpeg"),
        }

        response = requests.post(config.DISCORD_WEBHOOK_URL, files=files)
    else:
        # 無圖片：純 JSON
        payload = {"embeds": [embed]}
        response = requests.post(
            config.DISCORD_WEBHOOK_URL,
            json=payload,
        )

    if response.status_code == 204:
        print(f"[Discord] 警報已發送: {message}")
        return True
    else:
        print(f"[Discord] 發送失敗 ({response.status_code}): {response.text}")
        return False


def send_status(message):
    """發送一般狀態訊息"""
    if not config.DISCORD_WEBHOOK_URL:
        return False

    payload = {
        "embeds": [
            {
                "title": "ℹ️ 系統通知",
                "description": message,
                "color": 0x00BFFF,
                "timestamp": datetime.now().isoformat(),
            }
        ]
    }

    response = requests.post(config.DISCORD_WEBHOOK_URL, json=payload)
    return response.status_code == 204
