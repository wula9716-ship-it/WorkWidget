"""
桌面待办小组件 - Desktop Todo Widget
技术栈: Python 3 + tkinter (标准库，零依赖)
核心: overrideredirect(True) 无边框 + attributes("-topmost") 置顶 + JSON持久化
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import json, os
from datetime import datetime

# === 数据 ===
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
        json.dump({"date": datetime.now().strftime("%Y-%m-%d"), "tasks": tasks}, f, ensure_ascii=False, indent=2)

# === 颜色 ===
BG = "#1e1e1e"; BG_CARD = "#2d2d2d"; BG_INPUT = "#3a3a3a"
BORDER = "#444444"; ACCENT = "#ff9800"; ACCENT_HOVER = "#ffb74d"
TEXT = "#e0e0e0"; TEXT_DIM = "#888888"; GREEN = "#4caf50"; RED = "#f44336"

# === 窗口参数 ===
MIN_W, MIN_H, MAX_W, MAX_H = 280, 200, 800, 1000
EDGE = 6  # 缩放热区

# === 主窗口 ===
root = tk.Tk()
root.title("每日待办")
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.95)
root.configure(bg=BG)

WIN_W, WIN_H = 360, 520
sw = root.winfo_screenwidth()
root.geometry(f"{WIN_W}x{WIN_H}+{sw - WIN_W - 20}+60")

# === 缩放 ===
rsz = {"edge": None, "x": 0, "y": 0, "w": 0, "h": 0, "wx": 0, "wy": 0}

def get_edge(e):
    w, h = root.winfo_width(), root.winfo_height()
    ed = ""
    if e.y <= EDGE: ed += "n"
    elif e.y >= h - EDGE: ed += "s"
    if e.x <= EDGE: ed += "w"
    elif e.x >= w - EDGE: ed += "e"
    return ed

def edge_cursor(ed):
    m = {"n":"sb_v_double_arrow","s":"sb_v_double_arrow","e":"sb_h_double_arrow","w":"sb_h_double_arrow",
         "ne":"size_ne_sw","sw":"size_ne_sw","nw":"size_nw_se","se":"size_nw_se"}
    return m.get(ed, "")

def on_motion(e):
    if rsz["edge"]: return
    root.configure(cursor=edge_cursor(get_edge(e)))

def on_press(e):
    ed = get_edge(e)
    if not ed: return
    rsz.update(edge=ed, x=e.x_root, y=e.y_root, w=root.winfo_width(), h=root.winfo_height(),
               wx=root.winfo_x(), wy=root.winfo_y())

def on_drag(e):
    ed = rsz["edge"]
    if not ed: return
    dx, dy = e.x_root - rsz["x"], e.y_root - rsz["y"]
    nx, ny, nw, nh = rsz["wx"], rsz["wy"], rsz["w"], rsz["h"]
    if "e" in ed: nw = max(MIN_W, min(MAX_W, rsz["w"] + dx))
    if "w" in ed: nw = max(MIN_W, min(MAX_W, rsz["w"] - dx)); nx = rsz["wx"] + rsz["w"] - nw
    if "s" in ed: nh = max(MIN_H, min(MAX_H, rsz["h"] + dy))
    if "n" in ed: nh = max(MIN_H, min(MAX_H, rsz["h"] - dy)); ny = rsz["wy"] + rsz["h"] - nh
    root.geometry(f"{nw}x{nh}+{nx}+{ny}")

def on_release(e):
    rsz["edge"] = None

root.bind("<Motion>", on_motion)
root.bind("<Button-1>", on_press)
root.bind("<B1-Motion>", on_drag)
root.bind("<ButtonRelease-1>", on_release)

# === 最小化 ===
mini_flag = False

def minimize():
    global mini_flag
    mini_flag = True
    root.overrideredirect(False)
    root.iconify()

def on_map(e):
    global mini_flag
    if mini_flag:
        mini_flag = False
        root.overrideredirect(True)
        root.attributes("-topmost", True)

root.bind("<Map>", on_map)

# === 拖动 ===
dd = {"x": 0, "y": 0}

def start_drag(e):
    if get_edge(e): return
    dd["x"], dd["y"] = e.x, e.y

def do_drag(e):
    if rsz["edge"]: return
    root.geometry(f"+{root.winfo_x()+e.x-dd['x']}+{root.winfo_y()+e.y-dd['y']}")

# === 字体 ===
FT = tkfont.Font(family="Microsoft YaHei", size=13, weight="bold")
FD = tkfont.Font(family="Microsoft YaHei", size=9)
FNT = tkfont.Font(family="Microsoft YaHei", size=11)
FNTD = tkfont.Font(family="Microsoft YaHei", size=11, overstrike=1)
FI = tkfont.Font(family="Microsoft YaHei", size=11)
FB = tkfont.Font(family="Microsoft YaHei", size=10)
FS = tkfont.Font(family="Microsoft YaHei", size=9)
FI2 = tkfont.Font(family="Segoe UI Emoji", size=11)

tasks = load_tasks()

# === UI ===
mf = tk.Frame(root, bg=BG, padx=16, pady=12)
mf.pack(fill=tk.BOTH, expand=True)

# 标题栏
tb = tk.Frame(mf, bg=BG)
tb.pack(fill=tk.X, pady=(0, 12))
tb.bind("<Button-1>", start_drag); tb.bind("<B1-Motion>", do_drag)

lt = tk.Frame(tb, bg=BG)
lt.pack(side=tk.LEFT)
lt.bind("<Button-1>", start_drag); lt.bind("<B1-Motion>", do_drag)

tk.Label(lt, text="☑", font=FI2, fg=ACCENT, bg=BG).pack(side=tk.LEFT, padx=(0, 8))
tk.Label(lt, text="每日待办", font=FT, fg=TEXT, bg=BG).pack(side=tk.LEFT)

# 控制按钮
cf = tk.Frame(tb, bg=BG)
cf.pack(side=tk.RIGHT)

minb = tk.Label(cf, text=" — ", font=("Consolas", 12), fg=TEXT_DIM, bg=BG, cursor="hand2")
minb.pack(side=tk.LEFT, padx=1)
minb.bind("<Button-1>", lambda e: minimize())
minb.bind("<Enter>", lambda e: minb.configure(fg=ACCENT))
minb.bind("<Leave>", lambda e: minb.configure(fg=TEXT_DIM))

clb = tk.Label(cf, text=" × ", font=("Consolas", 14), fg=TEXT_DIM, bg=BG, cursor="hand2")
clb.pack(side=tk.LEFT, padx=1)
clb.bind("<Button-1>", lambda e: root.destroy())
clb.bind("<Enter>", lambda e: clb.configure(fg=RED))
clb.bind("<Leave>", lambda e: clb.configure(fg=TEXT_DIM))

# 日期
WK = {"Monday":"周一","Tuesday":"周二","Wednesday":"周三","Thursday":"周四","Friday":"周五","Saturday":"周六","Sunday":"周日"}
ds = datetime.now().strftime("%m月%d日 %A")
for k, v in WK.items(): ds = ds.replace(k, v)
dl = tk.Label(tb, text=ds, font=FD, fg=TEXT_DIM, bg=BG)
dl.pack(side=tk.RIGHT, padx=(0, 12))
dl.bind("<Button-1>", start_drag); dl.bind("<B1-Motion>", do_drag)

# 分割线
tk.Frame(mf, bg=BORDER, height=1).pack(fill=tk.X, pady=(0, 12))

# 输入区
inf = tk.Frame(mf, bg=BG_INPUT, highlightbackground=BORDER, highlightthickness=1, highlightcolor=ACCENT)
inf.pack(fill=tk.X, pady=(0, 12))
ini = tk.Frame(inf, bg=BG_INPUT)
ini.pack(fill=tk.X, padx=2, pady=2)

entry = tk.Entry(ini, font=FI, fg=TEXT, bg=BG_INPUT, insertbackground=TEXT, relief=tk.FLAT, highlightthickness=0, borderwidth=0)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0), pady=6)

ab = tk.Label(ini, text=" 添加 ", font=FB, fg="#000", bg=ACCENT, cursor="hand2", padx=12, pady=4)
ab.pack(side=tk.RIGHT, padx=(4, 4), pady=4)

# 任务列表
lc = tk.Canvas(mf, bg=BG, highlightthickness=0, borderwidth=0)
ls = tk.Scrollbar(mf, orient=tk.VERTICAL, command=lc.yview)
lf = tk.Frame(lc, bg=BG)
lf.bind("<Configure>", lambda e: lc.configure(scrollregion=lc.bbox("all")))
lc.create_window((0, 0), window=lf, anchor="nw")
lc.configure(yscrollcommand=ls.set)
ls.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 4))
lc.pack(fill=tk.BOTH, expand=True, pady=(0, 4))

lc.bind_all("<MouseWheel>", lambda e: lc.yview_scroll(int(-1*(e.delta/120)), "units"))

# 底部
bf = tk.Frame(mf, bg=BG)
bf.pack(fill=tk.X, pady=(8, 0))
tk.Frame(bf, bg=BORDER, height=1).pack(fill=tk.X, pady=(0, 8))
sf = tk.Frame(bf, bg=BG)
sf.pack(fill=tk.X)
sl = tk.Label(sf, text="", font=FS, fg=TEXT_DIM, bg=BG)
sl.pack(side=tk.LEFT)
rb = tk.Label(sf, text=" 重置 ", font=FB, fg=TEXT_DIM, bg=BG_INPUT, cursor="hand2", padx=8, pady=2)
rb.pack(side=tk.RIGHT)

# 右下角缩放指示
rg = tk.Label(mf, text="⋮⋮", font=("Consolas", 8), fg=TEXT_DIM, bg=BG, cursor="sb_se_corner")
rg.place(relx=1.0, rely=1.0, anchor="se", x=-4, y=-4)
rg.bind("<Button-1>", on_press)
rg.bind("<B1-Motion>", on_drag)
rg.bind("<ButtonRelease-1>", on_release)

# === 逻辑 ===
def update_stats():
    t, d = len(tasks), sum(1 for t in tasks if t["done"])
    sl.configure(text=f"总计 {t}  ·  完成 {d}  ·  待办 {t-d}")

def toggle(i):
    tasks[i]["done"] = not tasks[i]["done"]; save_tasks(tasks); render()

def delete(i):
    tasks.pop(i); save_tasks(tasks); render()

def add_task(event=None):
    txt = entry.get().strip()
    if not txt: return
    tasks.insert(0, {"text": txt, "done": False, "time": datetime.now().strftime("%H:%M")})
    save_tasks(tasks); entry.delete(0, tk.END); render()

def reset_all():
    tasks.clear(); save_tasks(tasks); render()

def render():
    for w in lf.winfo_children(): w.destroy()
    if not tasks:
        tk.Label(lf, text="还没有任务，添加一个吧", font=FNT, fg=TEXT_DIM, bg=BG).pack(pady=40)
        update_stats(); return
    for i, t in enumerate(tasks):
        cbg = BG_CARD if not t["done"] else "#252525"
        c = tk.Frame(lf, bg=cbg, highlightbackground=BORDER, highlightthickness=1)
        c.pack(fill=tk.X, pady=3, padx=2)
        ct = "●" if not t["done"] else "✓"
        cfg = ACCENT if not t["done"] else GREEN
        ch = tk.Label(c, text=f" {ct} ", font=FI2, fg=cfg, bg=cbg, cursor="hand2", width=3)
        ch.pack(side=tk.LEFT, padx=(8, 4), pady=8)
        ch.bind("<Button-1>", lambda e, idx=i: toggle(idx))
        tf = FNT if not t["done"] else FNTD
        tc = TEXT if not t["done"] else TEXT_DIM
        tk.Label(c, text=t["text"], font=tf, fg=tc, bg=cbg, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4, pady=8)
        db = tk.Label(c, text=" × ", font=("Consolas", 12), fg=TEXT_DIM, bg=cbg, cursor="hand2")
        db.pack(side=tk.RIGHT, padx=(4, 8), pady=8)
        db.bind("<Button-1>", lambda e, idx=i: delete(idx))
        db.bind("<Enter>", lambda e, b=db: b.configure(fg=RED))
        db.bind("<Leave>", lambda e, b=db: b.configure(fg=TEXT_DIM))
    update_stats()

def reset_confirm():
    if messagebox.askyesno("确认", "确定要清空今日所有任务吗？"):
        reset_all()

ab.bind("<Button-1>", add_task)
ab.bind("<Enter>", lambda e: ab.configure(bg=ACCENT_HOVER))
ab.bind("<Leave>", lambda e: ab.configure(bg=ACCENT))
entry.bind("<Return>", add_task)
rb.bind("<Button-1>", lambda e: reset_confirm())

render()
entry.focus_set()
root.mainloop()
