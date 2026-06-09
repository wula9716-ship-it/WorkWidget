# 桌面待办小组件 Desktop Todo Widget

一个简洁的桌面悬浮待办事项管理工具，基于 Python tkinter，**零依赖、秒启动**。

## 截图

深色工业风 UI，无边框悬浮窗口，始终置顶，支持拖动。

## 功能

- 无边框悬浮窗口，始终置顶
- 深色工业风 UI（深灰背景 + 橙色强调）
- 拖动标题栏任意移动位置
- 添加 / 完成（删除线） / 删除任务
- 每日自动重置（新的一天自动清空）
- 底部实时统计（总计 / 完成 / 待办）
- 数据持久化存储（JSON 文件）

## 技术原理

```
技术栈: Python 3 + tkinter (标准库)
依赖:   零 (Zero dependencies)

核心实现:
├── overrideredirect(True)    → 去掉系统标题栏，实现无边框
├── attributes("-topmost", True) → 窗口始终置顶
├── attributes("-alpha", 0.95)  → 轻微透明效果
├── Canvas + Scrollbar         → 可滚动任务列表
├── JSON 文件存储              → 任务数据持久化
└── 日期自动检测               → 新的一天自动清空任务
```

## 使用方法

### Windows

1. 确保已安装 Python 3.6+（tkinter 为标准库，无需额外安装）
2. 双击 `桌面待办.pyw` 即可运行（无控制台窗口）

### macOS / Linux

```bash
python3 桌面待办.pyw
```

## 文件说明

```
desktop-todo-widget/
├── 桌面待办.pyw      # 主程序（.pyw 扩展名隐藏控制台窗口）
├── todo_data.json    # 任务数据（自动生成）
├── README.md         # 说明文档
└── .gitignore        # Git 忽略文件
```

## 自定义

修改 `桌面待办.pyw` 顶部的颜色变量即可自定义主题：

```python
BG = "#1e1e1e"       # 背景色
ACCENT = "#ff9800"   # 强调色
TEXT = "#e0e0e0"      # 文字色
```

## License

MIT
