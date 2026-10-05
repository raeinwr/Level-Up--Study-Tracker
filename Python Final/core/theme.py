from PyQt6.QtGui import QFontDatabase

BG = "#6EC8F2"
PANEL = "#FFF8E7"
PANEL_DARK = "#1B2A52"
INK = "#17213F"

GOLD = "#FFD83D"
GREEN = "#55B84A"
RED = "#E94343"
GREY = "#5D6780"
BLUE = "#2F80ED"

PURPLE = "#7659C7"
DARK_PURPLE = "#18264A"
LIGHT_CYAN = "#D9F4FF"
WHITE = "#FFFFFF"
SKY = "#6EC8F2"
CREAM = "#FFF8E7"
BORDER = "#1B2A52"


def apply_theme(app):
    fonts = QFontDatabase.families()

    if "Pixelify Sans" in fonts:
        main_font = "Pixelify Sans"
    elif "Silkscreen" in fonts:
        main_font = "Silkscreen"
    else:
        main_font = "Courier New"

    title_font = "Press Start 2P" if "Press Start 2P" in fonts else main_font
    stat_font = "VT323" if "VT323" in fonts else main_font

    app.setStyleSheet(f"""
    QWidget {{
        background: transparent;
        color: {INK};
        font-family: "{main_font}";
        font-size: 14px;
    }}

    QLabel {{
        background: transparent;
        color: {INK};
    }}

    QLabel[role="title"] {{
        color: {BLUE};
        font-family: "{title_font}";
        font-size: 22px;
        font-weight: bold;
    }}

    QLabel[role="h2"] {{
        color: {BLUE};
        font-family: "{title_font}";
        font-size: 15px;
        font-weight: bold;
    }}

    QLabel[role="section"] {{
        color: {WHITE};
        font-family: "{title_font}";
        font-size: 12px;
        font-weight: bold;
    }}

    QLabel[role="quest_title"] {{
        color: {INK};
        font-family: "{title_font}";
        font-size: 16px;
        font-weight: bold;
    }}

    QLabel[role="small"] {{
        color: {GREY};
        font-size: 12px;
    }}

    QLabel[role="ghost"] {{
        color: {GREY};
        font-size: 13px;
    }}

    QLabel[role="clock"] {{
        background: {PANEL_DARK};
        color: {GOLD};
        font-family: "{stat_font}";
        font-size: 54px;
        font-weight: bold;
        padding: 8px 14px;
        border: none;
        border-radius: 12px;
    }}

    QFrame {{
        background: transparent;
        border: none;
    }}

    QFrame#header {{
        background: {RED};
        border: 3px solid {BORDER};
        border-radius: 14px;
    }}

    QFrame#header QLabel {{
        color: {WHITE};
    }}

    QFrame#quest {{
        background: {CREAM};
        border: 3px solid {BORDER};
        border-radius: 14px;
    }}

    QFrame#quest QLabel[role="small"] {{
        color: {GREY};
    }}

    QFrame#hud {{
        background: {CREAM};
        border: 3px solid {BORDER};
        border-radius: 14px;
    }}

    QFrame#card {{
        background: {CREAM};
        border: 3px solid {BORDER};
        border-radius: 14px;
    }}

    QPushButton {{
        background: {BLUE};
        color: {WHITE};
        border: 2px solid {BORDER};
        border-radius: 9px;
        padding: 8px 12px;
        font-family: "{main_font}";
        font-size: 13px;
        font-weight: bold;
    }}

    QPushButton:hover {{
        background: {GOLD};
        color: {INK};
    }}

    QPushButton:pressed {{
        background: {GREEN};
        color: {WHITE};
    }}

    QPushButton[variant="gold"] {{
        background: {GOLD};
        color: {INK};
    }}

    QPushButton[variant="gold"]:hover {{
        background: #FFE978;
    }}

    QPushButton[variant="green"] {{
        background: {GREEN};
        color: {WHITE};
    }}

    QPushButton[variant="red"] {{
        background: {RED};
        color: {WHITE};
    }}

    QPushButton[variant="grey"] {{
        background: #69758D;
        color: {WHITE};
    }}

    QPushButton[variant="purple"] {{
        background: {PURPLE};
        color: {WHITE};
    }}

    QLineEdit, QDoubleSpinBox, QComboBox {{
        background: {WHITE};
        color: {INK};
        border: 2px solid {BORDER};
        border-radius: 8px;
        padding: 7px 9px;
        font-family: "{main_font}";
        font-size: 13px;
    }}

    QLineEdit:focus, QDoubleSpinBox:focus, QComboBox:focus {{
        border: 2px solid {BLUE};
    }}

    QComboBox QAbstractItemView {{
        background: {WHITE};
        color: {INK};
        border: 2px solid {BORDER};
        selection-background-color: {BLUE};
        selection-color: {WHITE};
    }}

    QListWidget {{
        background: {WHITE};
        color: {INK};
        border: 2px solid {BORDER};
        border-radius: 8px;
        padding: 4px;
    }}

    QListWidget::item {{
        padding: 8px;
        border-bottom: 1px solid #D8DDE8;
    }}

    QListWidget::item:selected {{
        background: {LIGHT_CYAN};
        color: {INK};
    }}

    QCheckBox#questCheck {{
        background: transparent;
        color: {INK};
        spacing: 10px;
        padding: 8px 2px;
        border: none;
        border-bottom: 1px solid #D8DDE8;
        border-radius: 0;
        font-family: "{main_font}";
        font-size: 13px;
    }}

    QCheckBox#questCheck:hover {{
        background: {LIGHT_CYAN};
    }}

    QCheckBox#questCheck::indicator {{
        width: 20px;
        height: 20px;
        border: 2px solid {BORDER};
        border-radius: 4px;
        background: {WHITE};
    }}

    QCheckBox#questCheck::indicator:hover {{
        border-color: {BLUE};
    }}

    QCheckBox#questCheck::indicator:checked {{
        background: {GREEN};
        border-color: {BORDER};
    }}

    QProgressBar {{
        background: #DDECF4;
        border: 2px solid {BORDER};
        border-radius: 7px;
        height: 18px;
        text-align: center;
        color: {INK};
        font-family: "{main_font}";
        font-size: 12px;
        font-weight: bold;
    }}

    QProgressBar::chunk {{
        background: {GREEN};
        border-radius: 5px;
    }}

    QScrollBar:vertical {{
        background: #DCECF5;
        width: 10px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical {{
        background: {BLUE};
        min-height: 30px;
        border-radius: 5px;
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QToolTip {{
        background: {PANEL_DARK};
        color: {WHITE};
        border: 1px solid {GOLD};
        padding: 5px;
    }}
    """)
