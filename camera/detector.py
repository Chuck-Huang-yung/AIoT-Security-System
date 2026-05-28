"""OpenCV 人形偵測模組（人臉 + 上半身）"""

import cv2


# 初始化偵測器
_face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
_upperbody_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_upperbody.xml"
)


def detect_person(frame):
    """
    偵測畫面中是否有人（人臉或上半身）

    Args:
        frame: BGR numpy array

    Returns:
        (detected, boxes, confidence)
        - detected: bool，是否偵測到人
        - boxes: list of (x, y, w, h)
        - confidence: float，信心值
    """
    if frame is None:
        return False, [], 0.0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    all_boxes = []

    # 人臉偵測
    faces = _face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=2,
        minSize=(20, 20),
    )
    for (x, y, w, h) in faces:
        all_boxes.append((int(x), int(y), int(w), int(h), "Face"))

    # 上半身偵測
    bodies = _upperbody_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=2,
        minSize=(40, 40),
    )
    for (x, y, w, h) in bodies:
        all_boxes.append((int(x), int(y), int(w), int(h), "Body"))

    if len(all_boxes) == 0:
        return False, [], 0.0

    # 信心值用偵測數量估算
    confidence = min(1.0, len(all_boxes) * 0.5)
    boxes_only = [(x, y, w, h) for (x, y, w, h, _) in all_boxes]
    labels = [label for (_, _, _, _, label) in all_boxes]

    return True, list(zip(boxes_only, labels)), confidence


def draw_boxes(frame, boxes):
    """在畫面上畫出偵測框"""
    for (box, label) in boxes:
        x, y, w, h = box
        color = (0, 255, 0) if label == "Face" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(
            frame, label, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
        )
    return frame
