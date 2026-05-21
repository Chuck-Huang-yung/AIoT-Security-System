"""OpenCV 人形偵測模組（HOG + SVM）"""

import cv2


# 初始化 HOG 人形偵測器
_hog = cv2.HOGDescriptor()
_hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detect_person(frame):
    """
    偵測畫面中是否有人形

    Args:
        frame: BGR numpy array

    Returns:
        (detected, boxes, confidence)
        - detected: bool，是否偵測到人
        - boxes: list of (x, y, w, h)
        - confidence: float，最高信心值
    """
    if frame is None:
        return False, [], 0.0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    boxes, weights = _hog.detectMultiScale(
        gray,
        winStride=(8, 8),
        padding=(4, 4),
        scale=1.05,
    )

    if len(boxes) == 0:
        return False, [], 0.0

    confidence = float(max(weights))
    boxes_list = [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in boxes]

    return True, boxes_list, confidence


def draw_boxes(frame, boxes):
    """在畫面上畫出偵測框"""
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(
            frame, "Person", (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2
        )
    return frame
