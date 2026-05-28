"""攝影機擷取模組"""

import base64
import os
from datetime import datetime

import cv2

import config

# USB Webcam 直接用 OpenCV
USE_PICAMERA = False

_camera = None


def init():
    """初始化攝影機"""
    global _camera
    if USE_PICAMERA:
        _camera = Picamera2()
        _camera.configure(_camera.create_still_configuration())
        print("[CAM] 使用 PiCamera2")
    else:
        _camera = cv2.VideoCapture(0)
        if _camera.isOpened():
            print("[CAM] 使用 USB Webcam (OpenCV)")
        else:
            print("[CAM] 無可用攝影機，截圖功能將無法使用")
            _camera = None


def capture_frame():
    """擷取一幀畫面，回傳 numpy array（BGR）"""
    if _camera is None:
        return None

    if USE_PICAMERA:
        return _camera.capture_array()
    else:
        ret, frame = _camera.read()
        return frame if ret else None


def capture_to_base64(frame=None):
    """擷取截圖並轉為 Base64 字串"""
    if frame is None:
        frame = capture_frame()
    if frame is None:
        return None

    _, buffer = cv2.imencode(
        ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, config.JPEG_QUALITY]
    )
    return base64.b64encode(buffer).decode("utf-8")


def save_snapshot(frame=None):
    """儲存截圖到 snapshots/ 目錄，回傳檔案路徑"""
    if frame is None:
        frame = capture_frame()
    if frame is None:
        return None

    os.makedirs("snapshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"snapshots/{timestamp}.jpg"
    cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, config.JPEG_QUALITY])
    print(f"[CAM] 截圖已儲存: {filepath}")
    return filepath


def release():
    """釋放攝影機資源"""
    global _camera
    if _camera is not None:
        if not USE_PICAMERA:
            _camera.release()
        _camera = None
