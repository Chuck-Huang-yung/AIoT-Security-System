"""OpenCV DNN 人形偵測模組（MobileNet SSD）"""

import os
import cv2


# MobileNet SSD 類別名稱（只關注 person，index=15）
PERSON_CLASS_ID = 15
CONFIDENCE_THRESHOLD = 0.5  # 信心值門檻

# 載入模型
_model_dir = os.path.join(os.path.dirname(__file__), "model")
_prototxt = os.path.join(_model_dir, "deploy.prototxt")
_caffemodel = os.path.join(_model_dir, "mobilenet_ssd.caffemodel")

_net = None


def _load_model():
    global _net
    if _net is None:
        _net = cv2.dnn.readNetFromCaffe(_prototxt, _caffemodel)
        print("[偵測] MobileNet SSD 模型已載入")
    return _net


def detect_person(frame):
    """
    偵測畫面中是否有人

    Args:
        frame: BGR numpy array

    Returns:
        (detected, boxes, confidence)
        - detected: bool
        - boxes: list of ((x, y, w, h), label)
        - confidence: float，最高信心值
    """
    if frame is None:
        return False, [], 0.0

    net = _load_model()

    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        0.007843, (300, 300), 127.5
    )
    net.setInput(blob)
    detections = net.forward()

    boxes = []
    max_confidence = 0.0

    for i in range(detections.shape[2]):
        class_id = int(detections[0, 0, i, 1])
        confidence = float(detections[0, 0, i, 2])

        # 只偵測 person 類別
        if class_id != PERSON_CLASS_ID:
            continue
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        # 轉換座標
        box = detections[0, 0, i, 3:7] * [w, h, w, h]
        x1, y1, x2, y2 = box.astype("int")
        x1 = max(0, x1)
        y1 = max(0, y1)
        bw = x2 - x1
        bh = y2 - y1

        boxes.append(((x1, y1, bw, bh), f"Person {confidence:.0%}"))
        max_confidence = max(max_confidence, confidence)

    if len(boxes) == 0:
        return False, [], 0.0

    return True, boxes, max_confidence


def draw_boxes(frame, boxes):
    """在畫面上畫出偵測框"""
    for (box, label) in boxes:
        x, y, w, h = box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame, label, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
        )
    return frame
