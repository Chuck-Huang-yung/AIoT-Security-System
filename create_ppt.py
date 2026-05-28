"""產生 AIoT 專題報告 PPT"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# 配色方案
BG_DARK = RGBColor(0x0F, 0x17, 0x2A)       # 深藍背景
BG_CARD = RGBColor(0x1E, 0x29, 0x3B)       # 卡片背景
ACCENT_BLUE = RGBColor(0x38, 0xBD, 0xF8)   # 亮藍
ACCENT_GREEN = RGBColor(0x4A, 0xDE, 0x80)  # 綠色
ACCENT_RED = RGBColor(0xF8, 0x71, 0x71)    # 紅色
ACCENT_YELLOW = RGBColor(0xFB, 0xBF, 0x24) # 黃色
ACCENT_PURPLE = RGBColor(0xA7, 0x8B, 0xFA) # 紫色
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x94, 0xA3, 0xB8)
LIGHT_GRAY = RGBColor(0xCB, 0xD5, 0xE1)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)


def add_bg(slide, color=BG_DARK):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, left, top, width, height, fill_color=BG_CARD, border_color=None, radius=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, left, top, width, height, text, font_size=18, color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, font_name="Microsoft JhengHei"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_bullet_text(slide, left, top, width, height, items, font_size=16, color=WHITE, bullet_color=ACCENT_BLUE):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(8)
        # bullet dot
        run1 = p.add_run()
        run1.text = "●  "
        run1.font.size = Pt(font_size - 2)
        run1.font.color.rgb = bullet_color
        run1.font.name = "Microsoft JhengHei"
        # text
        run2 = p.add_run()
        run2.text = item
        run2.font.size = Pt(font_size)
        run2.font.color.rgb = color
        run2.font.name = "Microsoft JhengHei"
    return txBox


def add_code_block(slide, left, top, width, height, code, font_size=11):
    shape = add_shape(slide, left, top, width, height, fill_color=RGBColor(0x0D, 0x11, 0x17), border_color=RGBColor(0x30, 0x3B, 0x50))
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(12)
    tf.margin_right = Pt(12)
    tf.margin_top = Pt(8)
    tf.margin_bottom = Pt(8)
    for i, line in enumerate(code.split('\n')):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(2)
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_size)
        run.font.color.rgb = ACCENT_GREEN
        run.font.name = "Consolas"
    return shape


def slide_title_bar(slide, title, subtitle=None):
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.6), title, font_size=32, color=WHITE, bold=True)
    if subtitle:
        add_text(slide, Inches(0.8), Inches(1.0), Inches(11), Inches(0.4), subtitle, font_size=16, color=GRAY)
    # 底線
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(2), Pt(3))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_BLUE
    line.line.fill.background()


# ============================================================
# Slide 1: 封面
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)

add_text(slide, Inches(0.8), Inches(1.5), Inches(11.5), Inches(1.2),
         "AIoT 智慧安防與環境感測系統", font_size=44, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_text(slide, Inches(0.8), Inches(2.8), Inches(11.5), Inches(0.8),
         "基於 Raspberry Pi + ESP32 的人體偵測、即時監控與自動照明控制平台",
         font_size=20, color=GRAY, alignment=PP_ALIGN.CENTER)

# 三個特色標籤
tags = [
    ("Raspberry Pi", ACCENT_BLUE),
    ("ESP32", ACCENT_GREEN),
    ("MQTT", ACCENT_PURPLE),
]
for i, (tag, color) in enumerate(tags):
    x = Inches(4.2 + i * 1.8)
    shape = add_shape(slide, x, Inches(3.8), Inches(1.5), Inches(0.45), fill_color=BG_CARD, border_color=color)
    tf = shape.text_frame
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = tag
    run.font.size = Pt(14)
    run.font.color.rgb = color
    run.font.bold = True
    run.font.name = "Consolas"

add_text(slide, Inches(0.8), Inches(5.5), Inches(11.5), Inches(0.5),
         "AIoT 期末專題", font_size=16, color=GRAY, alignment=PP_ALIGN.CENTER)


# ============================================================
# Slide 2: 專題動機與目的
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "專題動機與目的")

items = [
    "隨著 IoT 技術普及，智慧家庭安防成為重要應用領域",
    "結合 AI 影像辨識與 IoT 感測，打造智慧化安防系統",
    "採用 Raspberry Pi + ESP32 雙裝置分散式架構",
    "透過雲端 MQTT Broker 實現跨裝置、跨網路通訊",
]
add_bullet_text(slide, Inches(0.8), Inches(1.8), Inches(5.5), Inches(3), items, font_size=18)

# 三個功能卡片
features = [
    ("入侵偵測與警報", "PIR → 攝影機 → OpenCV\n→ Discord 即時通知", ACCENT_RED),
    ("環境自動照明", "光敏電阻 → ADC 判斷\n→ LED 自動開關", ACCENT_YELLOW),
    ("Web 即時監控", "MQTT.js 直連 Broker\n→ 即時數據 + 遠端控制", ACCENT_BLUE),
]
for i, (title, desc, color) in enumerate(features):
    x = Inches(7.2)
    y = Inches(1.8 + i * 1.7)
    card = add_shape(slide, x, y, Inches(5.3), Inches(1.4), border_color=color)
    add_text(slide, x + Inches(0.3), y + Inches(0.15), Inches(4.5), Inches(0.4), title, font_size=18, color=color, bold=True)
    add_text(slide, x + Inches(0.3), y + Inches(0.6), Inches(4.5), Inches(0.7), desc, font_size=14, color=LIGHT_GRAY)


# ============================================================
# Slide 3: 系統架構總覽
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "系統架構總覽")

# ESP32 區塊
esp_card = add_shape(slide, Inches(0.5), Inches(1.8), Inches(3.5), Inches(3.2), border_color=ACCENT_GREEN)
add_text(slide, Inches(0.8), Inches(1.9), Inches(3), Inches(0.4), "ESP32（MicroPython）", font_size=16, color=ACCENT_GREEN, bold=True)
add_text(slide, Inches(0.8), Inches(2.3), Inches(3), Inches(0.3), "照明控制線路", font_size=13, color=GRAY)
esp_items = ["光敏電阻（ADC 直讀）", "LED 自動/手動控制", "MQTT 發布亮度數據", "MQTT 訂閱控燈指令"]
add_bullet_text(slide, Inches(0.8), Inches(2.7), Inches(3), Inches(2.2), esp_items, font_size=13, bullet_color=ACCENT_GREEN)

# RPi 區塊
rpi_card = add_shape(slide, Inches(0.5), Inches(5.2), Inches(3.5), Inches(2.0), border_color=ACCENT_BLUE)
add_text(slide, Inches(0.8), Inches(5.3), Inches(3), Inches(0.4), "Raspberry Pi（Python）", font_size=16, color=ACCENT_BLUE, bold=True)
add_text(slide, Inches(0.8), Inches(5.7), Inches(3), Inches(0.3), "安防偵測線路", font_size=13, color=GRAY)
rpi_items = ["PIR 紅外線感測器", "USB Webcam + OpenCV", "Discord 警報推播"]
add_bullet_text(slide, Inches(0.8), Inches(6.1), Inches(3), Inches(1.5), rpi_items, font_size=13, bullet_color=ACCENT_BLUE)

# MQTT Broker 中間
mqtt_card = add_shape(slide, Inches(5.0), Inches(2.8), Inches(3.3), Inches(2.0), border_color=ACCENT_PURPLE)
add_text(slide, Inches(5.3), Inches(2.9), Inches(2.7), Inches(0.4), "HiveMQ Cloud", font_size=18, color=ACCENT_PURPLE, bold=True)
add_text(slide, Inches(5.3), Inches(3.35), Inches(2.7), Inches(0.3), "MQTT Broker（雲端）", font_size=13, color=GRAY)
mqtt_items = ["TLS 加密（port 8883）", "WSS 連線（port 8884）", "免費方案，外網可存取"]
add_bullet_text(slide, Inches(5.3), Inches(3.8), Inches(2.7), Inches(1.5), mqtt_items, font_size=12, bullet_color=ACCENT_PURPLE)

# 使用者端
user_card = add_shape(slide, Inches(9.3), Inches(1.8), Inches(3.5), Inches(2.2), border_color=ACCENT_YELLOW)
add_text(slide, Inches(9.6), Inches(1.9), Inches(3), Inches(0.4), "Web Dashboard", font_size=16, color=ACCENT_YELLOW, bold=True)
add_text(slide, Inches(9.6), Inches(2.3), Inches(3), Inches(0.3), "即時監控介面", font_size=13, color=GRAY)
user_items = ["即時截圖顯示", "亮度數值 + 燈光控制", "警報事件列表", "系統狀態監控"]
add_bullet_text(slide, Inches(9.6), Inches(2.7), Inches(3), Inches(1.8), user_items, font_size=13, bullet_color=ACCENT_YELLOW)

discord_card = add_shape(slide, Inches(9.3), Inches(4.3), Inches(3.5), Inches(1.2), border_color=ACCENT_RED)
add_text(slide, Inches(9.6), Inches(4.4), Inches(3), Inches(0.4), "Discord 通知", font_size=16, color=ACCENT_RED, bold=True)
add_text(slide, Inches(9.6), Inches(4.8), Inches(3), Inches(0.5), "Webhook 即時推播\n入侵警報 + 截圖", font_size=13, color=LIGHT_GRAY)

# 箭頭文字（簡化用文字表示連線）
arrows = [
    (Inches(4.1), Inches(3.0), "MQTT →", ACCENT_GREEN),
    (Inches(4.1), Inches(5.8), "MQTT →", ACCENT_BLUE),
    (Inches(8.4), Inches(2.5), "→ WSS", ACCENT_YELLOW),
    (Inches(8.4), Inches(4.6), "→ HTTP", ACCENT_RED),
]
for x, y, text, color in arrows:
    add_text(slide, x, y, Inches(1), Inches(0.3), text, font_size=12, color=color, bold=True)


# ============================================================
# Slide 4: 安防線路流程
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "線路一：安防偵測流程", "Raspberry Pi — PIR → Camera → OpenCV → MQTT → Discord")

# 流程步驟卡片
steps = [
    ("1", "PIR 偵測", "紅外線感測器\n偵測人體移動", ACCENT_BLUE),
    ("2", "攝影機擷取", "USB Webcam\n擷取即時畫面", ACCENT_GREEN),
    ("3", "OpenCV 辨識", "HOG + SVM\n人形偵測演算法", ACCENT_PURPLE),
    ("4", "截圖儲存", "Base64 編碼\n本地備份", ACCENT_YELLOW),
    ("5", "MQTT 發布", "警報事件\n+ 截圖影像", ACCENT_BLUE),
    ("6", "Discord 通知", "Webhook 推播\n含入侵截圖", ACCENT_RED),
]

for i, (num, title, desc, color) in enumerate(steps):
    x = Inches(0.5 + i * 2.1)
    y = Inches(2.0)
    card = add_shape(slide, x, y, Inches(1.85), Inches(2.0), border_color=color)
    # 數字圓圈
    circle = add_shape(slide, x + Inches(0.65), y + Inches(0.15), Inches(0.55), Inches(0.55), fill_color=color)
    tf = circle.text_frame
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = num
    run.font.size = Pt(20)
    run.font.color.rgb = BG_DARK
    run.font.bold = True
    run.font.name = "Consolas"

    add_text(slide, x + Inches(0.1), y + Inches(0.8), Inches(1.65), Inches(0.35), title, font_size=15, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.1), y + Inches(1.2), Inches(1.65), Inches(0.7), desc, font_size=12, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    # 箭頭
    if i < len(steps) - 1:
        add_text(slide, x + Inches(1.85), y + Inches(0.75), Inches(0.3), Inches(0.4), "→", font_size=20, color=GRAY, alignment=PP_ALIGN.CENTER)

# 冷卻機制說明
add_shape(slide, Inches(0.5), Inches(4.5), Inches(12.3), Inches(1.2), border_color=ACCENT_YELLOW)
add_text(slide, Inches(0.8), Inches(4.6), Inches(11.5), Inches(0.35), "防抖動機制", font_size=16, color=ACCENT_YELLOW, bold=True)
add_text(slide, Inches(0.8), Inches(5.0), Inches(11.5), Inches(0.6),
         "冷卻時間 15 秒：PIR 觸發後 15 秒內不重複處理，避免連續誤觸發導致系統過載。SR505 本身為不可重觸發型，延遲約 8 秒。",
         font_size=14, color=LIGHT_GRAY)


# ============================================================
# Slide 5: 照明線路流程
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "線路二：自動照明流程", "ESP32（MicroPython）— 光敏電阻 → LED 自動控制 → MQTT")

steps2 = [
    ("1", "WiFi 連線", "boot.py\n自動連線熱點", ACCENT_BLUE),
    ("2", "MQTT 連線", "HiveMQ Cloud\nTLS 加密", ACCENT_PURPLE),
    ("3", "ADC 讀取", "光敏電阻\n亮度值 0-4095", ACCENT_GREEN),
    ("4", "自動控制", "亮度 < 閾值 → 開燈\n亮度 ≥ 閾值 → 關燈", ACCENT_YELLOW),
    ("5", "MQTT 發布", "亮度數據\n+ 燈光狀態", ACCENT_BLUE),
    ("6", "遠端控制", "Dashboard 手動\n開/關燈指令", ACCENT_RED),
]

for i, (num, title, desc, color) in enumerate(steps2):
    x = Inches(0.5 + i * 2.1)
    y = Inches(2.0)
    card = add_shape(slide, x, y, Inches(1.85), Inches(2.0), border_color=color)
    circle = add_shape(slide, x + Inches(0.65), y + Inches(0.15), Inches(0.55), Inches(0.55), fill_color=color)
    tf = circle.text_frame
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = num
    run.font.size = Pt(20)
    run.font.color.rgb = BG_DARK
    run.font.bold = True
    run.font.name = "Consolas"

    add_text(slide, x + Inches(0.1), y + Inches(0.8), Inches(1.65), Inches(0.35), title, font_size=15, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.1), y + Inches(1.2), Inches(1.65), Inches(0.7), desc, font_size=12, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    if i < len(steps2) - 1:
        add_text(slide, x + Inches(1.85), y + Inches(0.75), Inches(0.3), Inches(0.4), "→", font_size=20, color=GRAY, alignment=PP_ALIGN.CENTER)

# 手動覆蓋說明
add_shape(slide, Inches(0.5), Inches(4.5), Inches(12.3), Inches(1.2), border_color=ACCENT_GREEN)
add_text(slide, Inches(0.8), Inches(4.6), Inches(11.5), Inches(0.35), "手動覆蓋機制", font_size=16, color=ACCENT_GREEN, bold=True)
add_text(slide, Inches(0.8), Inches(5.0), Inches(11.5), Inches(0.6),
         "Dashboard 手動控燈後，自動模式暫停 60 秒，避免自動控制立即覆蓋手動操作。超時後自動恢復感測控制。每秒檢查 MQTT 訊息，確保控制指令即時響應。",
         font_size=14, color=LIGHT_GRAY)


# ============================================================
# Slide 6: MQTT 通訊架構
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "MQTT 通訊架構", "Topic 設計與訊息格式")

# Topic 表格
topics = [
    ("home/security/alert", "RPi", "Dashboard\nDiscord", '{"timestamp":"...",\n "confidence":0.85}', "入侵警報", ACCENT_RED),
    ("home/security/snapshot", "RPi", "Dashboard", '{"timestamp":"...",\n "image":"<Base64>"}', "截圖影像", ACCENT_RED),
    ("home/sensor/light", "ESP32", "Dashboard", '{"value": 2048}', "亮度數值", ACCENT_GREEN),
    ("home/light/status", "ESP32", "Dashboard", '{"status": "on"}', "燈光狀態", ACCENT_GREEN),
    ("home/light/control", "Dashboard", "ESP32", '{"action": "on"}', "遠端控燈", ACCENT_YELLOW),
    ("home/system/status", "RPi", "Dashboard", '{"cpu_temp":45,\n "uptime":"2h 30m"}', "系統狀態", ACCENT_BLUE),
]

# 表頭
headers = ["Topic", "發布者", "訂閱者", "Payload", "說明"]
header_widths = [Inches(2.8), Inches(1.0), Inches(1.2), Inches(3.5), Inches(1.5)]
x_start = Inches(0.8)
y_header = Inches(1.8)

x_pos = x_start
for header, w in zip(headers, header_widths):
    add_text(slide, x_pos, y_header, w, Inches(0.35), header, font_size=13, color=ACCENT_BLUE, bold=True)
    x_pos += w

# 分隔線
line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_start, Inches(2.15), Inches(10.0), Pt(1))
line.fill.solid()
line.fill.fore_color.rgb = RGBColor(0x30, 0x3B, 0x50)
line.line.fill.background()

# 表格內容
for row_i, (topic, pub, sub, payload, desc, color) in enumerate(topics):
    y = Inches(2.3 + row_i * 0.75)
    row_data = [topic, pub, sub, payload, desc]
    x_pos = x_start
    for col_i, (data, w) in enumerate(zip(row_data, header_widths)):
        c = ACCENT_GREEN if col_i == 0 else (color if col_i == 4 else LIGHT_GRAY)
        fs = 11 if col_i == 0 or col_i == 3 else 13
        fn = "Consolas" if col_i == 0 or col_i == 3 else "Microsoft JhengHei"
        txBox = slide.shapes.add_textbox(x_pos, y, w, Inches(0.7))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data
        p.font.size = Pt(fs)
        p.font.color.rgb = c
        p.font.name = fn
        x_pos += w


# ============================================================
# Slide 7: 硬體配置
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "硬體配置")

# RPi 硬體
rpi_hw = add_shape(slide, Inches(0.5), Inches(1.8), Inches(5.8), Inches(4.5), border_color=ACCENT_BLUE)
add_text(slide, Inches(0.8), Inches(1.9), Inches(5), Inches(0.4), "Raspberry Pi 端", font_size=20, color=ACCENT_BLUE, bold=True)

rpi_parts = [
    "Raspberry Pi 4 Model B — 安防主控",
    "USB Webcam — 影像擷取（OpenCV）",
    "PIR 紅外線感測器（HW-456 SR505）— GPIO 17",
    "供電：5V USB-C",
]
add_bullet_text(slide, Inches(0.8), Inches(2.5), Inches(5.2), Inches(2.5), rpi_parts, font_size=15, bullet_color=ACCENT_BLUE)

rpi_pin = "PIR 接線：\n  OUT → GPIO 17\n  GND → GND\n  VCC → 5V"
add_code_block(slide, Inches(0.8), Inches(4.8), Inches(5.2), Inches(1.2), rpi_pin, font_size=12)

# ESP32 硬體
esp_hw = add_shape(slide, Inches(7.0), Inches(1.8), Inches(5.8), Inches(4.5), border_color=ACCENT_GREEN)
add_text(slide, Inches(7.3), Inches(1.9), Inches(5), Inches(0.4), "ESP32 端", font_size=20, color=ACCENT_GREEN, bold=True)

esp_parts = [
    "ESP32-WROOM-32 — 照明主控",
    "光敏電阻（LDR）— GPIO 34（ADC）",
    "LED — GPIO 2",
    "供電：USB（獨立運作）",
]
add_bullet_text(slide, Inches(7.3), Inches(2.5), Inches(5.2), Inches(2.5), esp_parts, font_size=15, bullet_color=ACCENT_GREEN)

esp_pin = "LDR 接線：\n  一端 → 3.3V\n  另一端 → GPIO 34 + 10K 下拉電阻\nLED 接線：\n  長腳 → GPIO 2（經電阻）\n  短腳 → GND"
add_code_block(slide, Inches(7.3), Inches(4.5), Inches(5.2), Inches(1.5), esp_pin, font_size=12)


# ============================================================
# Slide 8: 軟體技術棧
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "軟體技術棧")

tech_categories = [
    ("Raspberry Pi", ACCENT_BLUE, [
        ("Python 3", "主程式語言"),
        ("OpenCV", "HOG+SVM 人形偵測"),
        ("paho-mqtt", "MQTT Client（TLS）"),
        ("RPi.GPIO", "GPIO 控制"),
        ("requests", "Discord Webhook"),
    ]),
    ("ESP32", ACCENT_GREEN, [
        ("MicroPython", "統一 Python 生態"),
        ("umqtt.simple", "輕量 MQTT Client"),
        ("machine.ADC", "類比訊號讀取"),
        ("machine.Pin", "GPIO 控制"),
    ]),
    ("雲端 / 前端", ACCENT_PURPLE, [
        ("HiveMQ Cloud", "MQTT Broker（免費）"),
        ("MQTT.js", "前端 MQTT 直連"),
        ("Tailwind CSS", "現代深色主題 UI"),
        ("Discord Webhook", "警報推播通知"),
    ]),
]

for col_i, (cat_name, color, techs) in enumerate(tech_categories):
    x = Inches(0.5 + col_i * 4.2)
    card = add_shape(slide, x, Inches(1.8), Inches(3.8), Inches(5.0), border_color=color)
    add_text(slide, x + Inches(0.3), Inches(1.9), Inches(3.2), Inches(0.4), cat_name, font_size=18, color=color, bold=True)

    for i, (tech, desc) in enumerate(techs):
        y = Inches(2.5 + i * 0.85)
        # 技術名
        add_text(slide, x + Inches(0.3), y, Inches(3.2), Inches(0.3), tech, font_size=15, color=WHITE, bold=True)
        # 說明
        add_text(slide, x + Inches(0.3), y + Inches(0.3), Inches(3.2), Inches(0.3), desc, font_size=12, color=GRAY)


# ============================================================
# Slide 9: 核心程式碼 — RPi 安防主迴圈
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "核心程式碼 — RPi 安防主迴圈", "main.py → security_loop()")

code_security = """def security_loop():
    pir.setup()
    capture.init()
    last_trigger_time = 0
    COOLDOWN = 15

    while running:
        if pir.detect():
            now = time.time()
            if now - last_trigger_time < COOLDOWN:
                time.sleep(1)
                continue

            last_trigger_time = now
            frame = capture.capture_frame()
            detected, boxes, confidence = detector.detect_person(frame)

            if detected:
                frame = detector.draw_boxes(frame, boxes)
                img_base64 = capture.capture_to_base64(frame)
                capture.save_snapshot(frame)

                mqtt_client.publish("home/security/alert", {
                    "timestamp": timestamp,
                    "confidence": round(confidence, 2),
                })
                discord_bot.send_alert(
                    f"偵測到入侵！信心值: {confidence:.0%}",
                    image_base64=img_base64,
                )"""

add_code_block(slide, Inches(0.5), Inches(1.7), Inches(7.5), Inches(5.5), code_security, font_size=11)

# 右側說明
notes = [
    ("PIR 觸發", "GPIO 17 偵測到高電位\n表示有人體移動", ACCENT_BLUE),
    ("冷卻機制", "15 秒內不重複觸發\n防止連續誤報", ACCENT_YELLOW),
    ("OpenCV 辨識", "HOG + SVM 演算法\n判斷是否為人形", ACCENT_PURPLE),
    ("多管道通知", "MQTT → Dashboard\nWebhook → Discord", ACCENT_RED),
]
for i, (title, desc, color) in enumerate(notes):
    y = Inches(1.8 + i * 1.3)
    card = add_shape(slide, Inches(8.5), y, Inches(4.3), Inches(1.1), border_color=color)
    add_text(slide, Inches(8.8), y + Inches(0.1), Inches(3.7), Inches(0.3), title, font_size=14, color=color, bold=True)
    add_text(slide, Inches(8.8), y + Inches(0.45), Inches(3.7), Inches(0.6), desc, font_size=12, color=LIGHT_GRAY)


# ============================================================
# Slide 10: 核心程式碼 — ESP32 照明控制
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "核心程式碼 — ESP32 照明控制", "esp32/main.py — MicroPython")

code_esp32 = """# 硬體初始化
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)  # 0-3.3V, ADC 0-4095
led = Pin(2, Pin.OUT)

# 主迴圈
while True:
    ldr_value = ldr.read()

    # 手動覆蓋超時，恢復自動
    if manual_override and \\
       (time.time() - manual_override_time > 60):
        manual_override = False

    # 自動控制（手動模式下跳過）
    if not manual_override:
        if ldr_value < LIGHT_THRESHOLD:
            led.value(1)   # 開燈
            led_status = "on"
        else:
            led.value(0)   # 關燈
            led_status = "off"

    # 發布亮度數據
    client.publish("home/sensor/light",
                   json.dumps({"value": ldr_value}))

    # 每秒檢查 MQTT（控燈指令）
    for _ in range(PUBLISH_INTERVAL):
        client.check_msg()
        time.sleep(1)"""

add_code_block(slide, Inches(0.5), Inches(1.7), Inches(7.5), Inches(5.5), code_esp32, font_size=11)

notes2 = [
    ("ADC 讀取", "ESP32 內建 12-bit ADC\n直讀光敏電阻 0-4095", ACCENT_GREEN),
    ("自動控制", "亮度低於閾值自動開燈\n高於閾值自動關燈", ACCENT_YELLOW),
    ("手動覆蓋", "Dashboard 控制後\n暫停自動 60 秒", ACCENT_PURPLE),
    ("即時響應", "每秒檢查 MQTT 訊息\n確保控燈指令即時", ACCENT_BLUE),
]
for i, (title, desc, color) in enumerate(notes2):
    y = Inches(1.8 + i * 1.3)
    card = add_shape(slide, Inches(8.5), y, Inches(4.3), Inches(1.1), border_color=color)
    add_text(slide, Inches(8.8), y + Inches(0.1), Inches(3.7), Inches(0.3), title, font_size=14, color=color, bold=True)
    add_text(slide, Inches(8.8), y + Inches(0.45), Inches(3.7), Inches(0.6), desc, font_size=12, color=LIGHT_GRAY)


# ============================================================
# Slide 11: Web Dashboard
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "Web Dashboard 即時監控", "Tailwind CSS + MQTT.js — 純靜態，無需後端")

# 功能區塊
dashboard_features = [
    ("即時截圖", "subscribe home/security/snapshot\nBase64 圖片即時渲染", ACCENT_RED),
    ("警報事件列表", "subscribe home/security/alert\n入侵警報即時顯示", ACCENT_RED),
    ("環境亮度", "subscribe home/sensor/light\nESP32 ADC 即時數據", ACCENT_GREEN),
    ("燈光控制", "publish home/light/control\n手動開關燈按鈕", ACCENT_YELLOW),
    ("系統狀態", "subscribe home/system/status\nCPU 溫度、運行時間", ACCENT_BLUE),
    ("連線設定", "MQTT Broker 設定\nlocalStorage 儲存", ACCENT_PURPLE),
]

for i, (title, desc, color) in enumerate(dashboard_features):
    col = i % 3
    row = i // 3
    x = Inches(0.5 + col * 4.2)
    y = Inches(1.8 + row * 2.5)
    card = add_shape(slide, x, y, Inches(3.8), Inches(2.0), border_color=color)
    add_text(slide, x + Inches(0.3), y + Inches(0.2), Inches(3.2), Inches(0.4), title, font_size=18, color=color, bold=True)
    add_text(slide, x + Inches(0.3), y + Inches(0.7), Inches(3.2), Inches(1.0), desc, font_size=14, color=LIGHT_GRAY)

# 技術亮點
add_shape(slide, Inches(0.5), Inches(6.2), Inches(12.3), Inches(0.9), border_color=ACCENT_BLUE)
add_text(slide, Inches(0.8), Inches(6.3), Inches(11.5), Inches(0.7),
         "技術亮點：MQTT.js 透過 WebSocket Secure（WSS）直連 HiveMQ Cloud，無需後端伺服器。前端純靜態 HTML/JS，可部署於任何 Web Server 或直接本地開啟。",
         font_size=14, color=LIGHT_GRAY)


# ============================================================
# Slide 12: Discord 通知
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "Discord 即時通知", "Webhook — 入侵警報 + 截圖推播")

# 左側：程式碼
code_discord = """def send_alert(message, image_base64=None):
    embed = {
        "title": "入侵警報",
        "description": message,
        "color": 0xFF0000,
        "timestamp": datetime.now().isoformat(),
        "image": {"url": "attachment://snapshot.jpg"},
    }

    # 圖片用 multipart/form-data 上傳
    image_data = base64.b64decode(image_base64)
    files = {
        "payload_json": (None, json.dumps(payload)),
        "files[0]": ("snapshot.jpg", BytesIO(image_data)),
    }

    requests.post(DISCORD_WEBHOOK_URL, files=files)"""

add_code_block(slide, Inches(0.5), Inches(1.7), Inches(6.5), Inches(4.2), code_discord, font_size=11)

# 右側說明
add_shape(slide, Inches(7.5), Inches(1.7), Inches(5.3), Inches(4.2), border_color=ACCENT_RED)
add_text(slide, Inches(7.8), Inches(1.8), Inches(4.7), Inches(0.4), "通知功能", font_size=18, color=ACCENT_RED, bold=True)

discord_items = [
    "Embed 格式：標題 + 描述 + 時間戳",
    "附帶入侵截圖（JPG 圖片）",
    "multipart/form-data 上傳圖片",
    "系統上線 / 下線通知",
    "無需 Bot Token，使用 Webhook URL",
]
add_bullet_text(slide, Inches(7.8), Inches(2.4), Inches(4.7), Inches(3), discord_items, font_size=14, bullet_color=ACCENT_RED)


# ============================================================
# Slide 13: 專案目錄結構
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "專案目錄結構")

dir_structure = """AIOT_final/
├── config.py                  # RPi 設定檔（MQTT、GPIO、Discord）
├── main.py                    # RPi 主程式入口
├── .env                       # 敏感資訊（MQTT 密碼、Webhook URL）
│
├── sensors/
│   └── pir.py                 # PIR 紅外線感測器模組
│
├── camera/
│   ├── capture.py             # 攝影機擷取（OpenCV）
│   └── detector.py            # HOG+SVM 人形偵測
│
├── mqtt/
│   └── client.py              # MQTT 連線封裝（paho-mqtt）
│
├── notify/
│   └── discord_bot.py         # Discord Webhook 通知
│
├── web/
│   └── index.html             # Dashboard（Tailwind + MQTT.js）
│
├── esp32/                     # ESP32 MicroPython
│   ├── boot.py                # WiFi 自動連線
│   ├── main.py                # 光敏+LED+MQTT 主程式
│   ├── config.py              # ESP32 設定
│   └── lib/
│       └── umqtt_simple.py    # MQTT 函式庫
│
└── snapshots/                 # 截圖儲存目錄"""

add_code_block(slide, Inches(0.5), Inches(1.7), Inches(7.0), Inches(5.5), dir_structure, font_size=11)

# 右側模組說明
modules = [
    ("RPi 端", "安防偵測 + 系統監控\nPython 3 + OpenCV + paho-mqtt", ACCENT_BLUE),
    ("ESP32 端", "照明控制\nMicroPython + umqtt", ACCENT_GREEN),
    ("前端", "即時監控 Dashboard\nHTML/JS + Tailwind + MQTT.js", ACCENT_YELLOW),
    ("雲端", "HiveMQ Cloud Broker\n+ Discord Webhook", ACCENT_PURPLE),
]
for i, (title, desc, color) in enumerate(modules):
    y = Inches(1.8 + i * 1.3)
    card = add_shape(slide, Inches(8.0), y, Inches(4.8), Inches(1.1), border_color=color)
    add_text(slide, Inches(8.3), y + Inches(0.1), Inches(4.2), Inches(0.3), title, font_size=15, color=color, bold=True)
    add_text(slide, Inches(8.3), y + Inches(0.45), Inches(4.2), Inches(0.6), desc, font_size=13, color=LIGHT_GRAY)


# ============================================================
# Slide 14: 開發過程與問題解決
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "開發過程與問題解決")

problems = [
    ("PIR 持續誤觸發",
     "GPIO 浮接導致持續高電位",
     "加入 pull-down 電阻 + 軟體冷卻機制（15 秒）",
     ACCENT_RED),
    ("picamera2 與 USB Webcam 衝突",
     "picamera2 嘗試用 libcamera 開啟 USB Webcam 導致凍結",
     "硬編碼使用 OpenCV VideoCapture，跳過 picamera2",
     ACCENT_YELLOW),
    ("ESP32 ussl 模組更名",
     "MicroPython v1.25 將 ussl 更名為 ssl",
     "umqtt_simple.py 加入 try/except 相容處理",
     ACCENT_GREEN),
    ("手動控燈被自動覆蓋",
     "手動開燈後，下一個 loop 自動模式立即關燈",
     "加入 manual_override 機制，手動控制後暫停自動 60 秒",
     ACCENT_BLUE),
    ("WiFi WPA3 不相容",
     "RPi 無法連線 WPA3 手機熱點",
     "手機端改用 WPA2 安全性設定",
     ACCENT_PURPLE),
]

for i, (problem, cause, solution, color) in enumerate(problems):
    y = Inches(1.7 + i * 1.1)
    card = add_shape(slide, Inches(0.5), y, Inches(12.3), Inches(0.95), border_color=color)
    add_text(slide, Inches(0.8), y + Inches(0.05), Inches(2.8), Inches(0.3), problem, font_size=14, color=color, bold=True)
    add_text(slide, Inches(3.8), y + Inches(0.05), Inches(4.0), Inches(0.85), "原因：" + cause, font_size=12, color=GRAY)
    add_text(slide, Inches(7.8), y + Inches(0.05), Inches(4.8), Inches(0.85), "解法：" + solution, font_size=12, color=ACCENT_GREEN)


# ============================================================
# Slide 15: 成果展示
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
slide_title_bar(slide, "系統成果")

results = [
    ("安防偵測完整流程", "PIR 偵測人體 → 攝影機截圖 → OpenCV 人形辨識\n→ MQTT 發布警報 → Discord 推播通知（含截圖）", ACCENT_RED),
    ("自動照明控制", "光敏電阻即時偵測環境亮度 → 自動開/關 LED\n→ MQTT 發布狀態 → Dashboard 即時顯示", ACCENT_GREEN),
    ("Web Dashboard 即時監控", "MQTT.js 直連雲端 Broker → 即時截圖、亮度數據\n燈光手動控制、系統狀態監控", ACCENT_YELLOW),
    ("雲端通訊架構", "RPi + ESP32 雙裝置透過 HiveMQ Cloud 協同運作\n支援外網存取，手機可即時收到警報", ACCENT_BLUE),
]

for i, (title, desc, color) in enumerate(results):
    col = i % 2
    row = i // 2
    x = Inches(0.5 + col * 6.4)
    y = Inches(1.8 + row * 2.5)
    card = add_shape(slide, x, y, Inches(6.0), Inches(2.2), border_color=color)
    add_text(slide, x + Inches(0.3), y + Inches(0.2), Inches(5.4), Inches(0.4), title, font_size=18, color=color, bold=True)
    add_text(slide, x + Inches(0.3), y + Inches(0.7), Inches(5.4), Inches(1.2), desc, font_size=15, color=LIGHT_GRAY)


# ============================================================
# Slide 16: 結尾
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)

add_text(slide, Inches(0.8), Inches(2.0), Inches(11.5), Inches(1.0),
         "Thank You", font_size=52, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_text(slide, Inches(0.8), Inches(3.3), Inches(11.5), Inches(0.6),
         "AIoT 智慧安防與環境感測系統", font_size=24, color=GRAY, alignment=PP_ALIGN.CENTER)

# 技術標籤
techs_footer = ["Raspberry Pi", "ESP32", "OpenCV", "MQTT", "Discord", "Tailwind CSS"]
for i, tech in enumerate(techs_footer):
    x = Inches(2.3 + i * 1.5)
    colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_YELLOW, ACCENT_RED, ACCENT_BLUE]
    shape = add_shape(slide, x, Inches(4.5), Inches(1.3), Inches(0.4), fill_color=BG_CARD, border_color=colors[i])
    tf = shape.text_frame
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = tech
    run.font.size = Pt(11)
    run.font.color.rgb = colors[i]
    run.font.bold = True
    run.font.name = "Consolas"


# ============================================================
# 儲存
# ============================================================
output_path = "/Users/ianho/AIOT_final/AIoT_期末專題報告.pptx"
prs.save(output_path)
print(f"PPT 已儲存: {output_path}")
