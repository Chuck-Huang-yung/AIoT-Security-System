"""PIR 紅外線感測器模組（HW-456 SR505）"""

import config

# 嘗試載入 RPi.GPIO，若不在樹莓派上則用模擬模式
try:
    import RPi.GPIO as GPIO
    MOCK_MODE = False
except ImportError:
    MOCK_MODE = True
    print("[PIR] 非 RPi 環境，使用模擬模式")


def setup():
    """初始化 PIR 感測器 GPIO"""
    if MOCK_MODE:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.PIR_PIN, GPIO.IN)
    print(f"[PIR] 已初始化，GPIO {config.PIR_PIN}")


def detect():
    """偵測是否有人體（回傳 True/False）"""
    if MOCK_MODE:
        return False
    return GPIO.input(config.PIR_PIN) == 1


def on_motion(callback):
    """註冊人體偵測中斷回調"""
    if MOCK_MODE:
        print("[PIR] 模擬模式，無法註冊中斷回調")
        return
    GPIO.add_event_detect(
        config.PIR_PIN,
        GPIO.RISING,
        callback=callback,
        bouncetime=8000,  # SR505 不可重觸發延遲約 8 秒
    )
    print("[PIR] 已註冊移動偵測回調 (SR505)")


def cleanup():
    """清理 GPIO"""
    if not MOCK_MODE:
        GPIO.cleanup(config.PIR_PIN)
