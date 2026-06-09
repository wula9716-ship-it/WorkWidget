"""
桌面待办小组件 - Desktop Todo Widget
一个简洁的桌面悬浮待办事项管理工具

技术栈: Python 3 + tkinter (标准库，零依赖)
原理:
  - 使用 tkinter 创建无边框、始终置顶的悬浮窗口
  - overrideredirect(True) 去掉系统标题栏
  - attributes("-topmost", True) 保持窗口置顶
  - 任务数据存储在本地 JSON 文件中
  - 自动检测日期，新的一天自动清空任务
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import json
import os
from datetime import datetime

# === 数据存储 ===
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo_data.json")

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                return data.get("tasks", [])
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tasks": tasks
        }, f, ensure_ascii=False, indent=2)

# === 颜色方案 (工业/机械风格) ===
BG = "#1e1e1e"
BG_CARD = "#2d2d2d"
BG_INPUT = "#3a3a3a"
BORDER = "#444444"
ACCENT = "#ff9800"
ACCENT_HOVER = "#ffb74d"
TEXT = "#e0e0e0"
TEXT_DIM = "#888888"
GREEN = "#4caf50"
RED = "#f44336"

# === 主窗口 ===
root = tk.Tk()
root.title("每日待办")
root.overrideredirect(True)      # 无边框
root.attributes("-topmost", True)  # 始终置顶
root.attributes("-alpha", 0.95)   # 轻微透明
root.configure(bg=BG)

WIN_W = 360
WIN_H = 520
screen_w = root.winfo_screenwidth()
root.geometry(f"{WIN_W}x{WIN_H}+{screen_w - WIN_W - 20}+60")

# === 拖动 ===
drag_data = {"x": 0, "y": 0}

def start_drag(event):
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def do_drag(event):
    root.geometry(f"+{root.winfo_x() + event.x - drag_data['x']}+{root.winfo_y() + event.y - drag_data['y']}")

# === 字体 ===
FONT_TITLE = tkfont.Font(family="Microsoft YaHei", size=13, weight="bold")
FONT_DATE = tkfont.Font(family="Microsoft YaHei", size=9)
FONT_TASK = tkfont.Font(family="Microsoft YaHei", size=11)
FONT_TASK_DONE = tkfont.Font(family="Microsoft YaHei", size=11, overstrike=1)
FONT_INPUT = tkfont.Font(family="Microsoft YaHei", size=11)
FONT_BTN = tkfont.Font(family="Microsoft YaHei", size=10)
FONT_STAT = tkfont.Font(family="Microsoft YaHei", size=9)
FONT_ICON = tkfont.Font(family="Segoe UI Emoji", size=11)

tasks = load_tasks()

# === UI构建 ===
main_frame = tk.Frame(root, bg=BG, padx=16, pady=12)
main_frame.pack(fill=tk.BOTH, expand=True)

# 标题栏
title_bar = tk.Frame(main_frame, bg=BG)
title_bar.pack(fill=tk.X, pady=(0, 12))
for w in [title_bar]:
    w.bind("<Button-1>", start_drag)
    w.bind("<B1-Motion>", do_drag)

left_title = tk.Frame(title_bar, bg=BG)
left_title.pack(side=tk.LEFT)
left_title.bind("<Button-1>", start_drag)
left_title.bind("<B1-Motion>", do_drag)

icon_label = tk.Label(left_title, text="☑", font=FONT_ICON, fg=ACCENT, bg=BG)
icon_label.pack(side=tk.LEFT, padx=(0, 8))
icon_label.bind("<Button-1>", start_drag)
icon_label.bind("<B1-Motion>", do_drag)

title_label = tk.Label(left_title, text="每日待办", font=FONT_TITLE, fg=TEXT, bg=BG)
title_label.pack(side=tk.LEFT)
title_label.bind("<Button-1>", start_drag)
title_label.bind("<B1-Motion>", do_drag)

close_btn = tk.Label(title_bar, text=" × ", font=("Consolas", 14), fg=TEXT_DIM, bg=BG, cursor="hand2")
close_btn.pack(side=tk.RIGHT)
close_btn.bind("<Button-1>", lambda e: root.destroy())
close_btn.bind("<Enter>", lambda e: close_btn.configure(fg=RED))
close_btn.bind("<Leave>", lambda e: close_btn.configure(fg=TEXT_DIM))

WEEKDAYS = {"Monday": "周一", "Tuesday": "周二", "Wednesday": "周三",
            "Thursday": "周四", "Friday": "周五", "Saturday": "周六", "Sunday": "周日"}
date_str = datetime.now().strftime("%m月%d日 %A")
for en, zh in WEEKDAYS.items():
    date_str = date_str.replace(en, zh)

date_label = tk.Label(title_bar, text=date_str, font=FONT_DATE, fg=TEXT_DIM, bg=BG)
date_label.pack(side=tk.RIGHT, padx=(0, 12))
date_label.bind("<Button-1>", start_drag)
date_label.bind("<B1-Motion>", do_drag)

# 分割线
tk.Frame(main_frame, bg=BORDER, height=1).pack(fill=tk.X, pady=(0, 12))

# 输入区
input_frame = tk.Frame(main_frame, bg=BG_INPUT, highlightbackground=BORDER, highlightthickness=1, highlightcolor=ACCENT)
input_frame.pack(fill=tk.X, pady=(0, 12))

input_inner = tk.Frame(input_frame, bg=BG_INPUT)
input_inner.pack(fill=tk.X, padx=2, pady=2)

entry = tk.Entry(input_inner, font=FONT_INPUT, fg=TEXT, bg=BG_INPUT, insertbackground=TEXT,
                 relief=tk.FLAT, highlightthickness=0, borderwidth=0)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0), pady=6)

add_btn = tk.Label(input_inner, text=" 添加 ", font=FONT_BTN, fg="#000", bg=ACCENT, cursor="hand2", padx=12, pady=4)
add_btn.pack(side=tk.RIGHT, padx=(4, 4), pady=4)

# 任务列表
list_canvas = tk.Canvas(main_frame, bg=BG, highlightthickness=0, borderwidth=0)
list_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=list_canvas.yview)
list_frame = tk.Frame(list_canvas, bg=BG)

list_frame.bind("<Configure>", lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
list_canvas.create_window((0, 0), window=list_frame, anchor="nw")
list_canvas.configure(yscrollcommand=list_scrollbar.set)

list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 4))
list_canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 4))

def on_mousewheel(event):
    list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
list_canvas.bind_all("<MouseWheel>", on_mousewheel)

# 底部
bottom_frame = tk.Frame(main_frame, bg=BG)
bottom_frame.pack(fill=tk.X, pady=(8, 0))

tk.Frame(bottom_frame, bg=BORDER, height=1).pack(fill=tk.X, pady=(0, 8))

stats_frame = tk.Frame(bottom_frame, bg=BG)
stats_frame.pack(fill=tk.X)

stats_label = tk.Label(stats_frame, text="", font=FONT_STAT, fg=TEXT_DIM, bg=BG)
stats_label.pack(side=tk.LEFT)

reset_btn = tk.Label(stats_frame, text=" 重置 ", font=FONT_BTN, fg=TEXT_DIM, bg=BG_INPUT, cursor="hand2", padx=8, pady=2)
reset_btn.pack(side=tk.RIGHT)

# === 逻辑 ===
def update_stats():
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    stats_label.configure(text=f"总计 {total}  ·  完成 {done}  ·  待办 {total - done}")

def toggle_task(idx):
    tasks[idx]["done"] = not tasks[idx]["done"]
    save_tasks(tasks)
    render_tasks()

def delete_task(idx):
    tasks.pop(idx)
    save_tasks(tasks)
    render_tasks()

def add_task(event=None):
    text = entry.get().strip()
    if not text:
        return
    tasks.insert(0, {"text": text, "done": False, "time": datetime.now().strftime("%H:%M")})
    save_tasks(tasks)
    entry.delete(0, tk.END)
    render_tasks()

def reset_tasks():
    tasks.clear()
    save_tasks(tasks)
    render_tasks()

def render_tasks():
    for widget in list_frame.winfo_children():
        widget.destroy()

    if not tasks:
        tk.Label(list_frame, text="还没有任务，添加一个吧", font=FONT_TASK, fg=TEXT_DIM, bg=BG).pack(pady=40)
        update_stats()
        return

    for idx, task in enumerate(tasks):
        card_bg = BG_CARD if not task["done"] else "#252525"
        card = tk.Frame(list_frame, bg=card_bg, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill=tk.X, pady=3, padx=2)

        check_text = "●" if not task["done"] else "✓"
        check_fg = ACCENT if not task["done"] else GREEN
        checkbox = tk.Label(card, text=f" {check_text} ", font=FONT_ICON, fg=check_fg, bg=card_bg, cursor="hand2", width=3)
        checkbox.pack(side=tk.LEFT, padx=(8, 4), pady=8)
        checkbox.bind("<Button-1>", lambda e, i=idx: toggle_task(i))

        task_font = FONT_TASK if not task["done"] else FONT_TASK_DONE
        text_color = TEXT if not task["done"] else TEXT_DIM
        tk.Label(card, text=task["text"], font=task_font, fg=text_color, bg=card_bg, anchor="w").pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=4, pady=8)

        del_btn = tk.Label(card, text=" × ", font=("Consolas", 12), fg=TEXT_DIM, bg=card_bg, cursor="hand2")
        del_btn.pack(side=tk.RIGHT, padx=(4, 8), pady=8)
        del_btn.bind("<Button-1>", lambda e, i=idx: delete_task(i))
        del_btn.bind("<Enter>", lambda e, btn=del_btn: btn.configure(fg=RED))
        del_btn.bind("<Leave>", lambda e, btn=del_btn: btn.configure(fg=TEXT_DIM))

    update_stats()

def reset_with_confirm():
    if messagebox.askyesno("确认", "确定要清空今日所有任务吗？"):
        reset_tasks()

# === 绑定 ===
add_btn.bind("<Button-1>", add_task)
add_btn.bind("<Enter>", lambda e: add_btn.configure(bg=ACCENT_HOVER))
add_btn.bind("<Leave>", lambda e: add_btn.configure(bg=ACCENT))
entry.bind("<Return>", add_task)
reset_btn.bind("<Button-1>", lambda e: reset_with_confirm())

render_tasks()
entry.focus_set()
root.mainloop()
