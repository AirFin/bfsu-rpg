# Pyxel 像素 RPG 游戏

一个使用 Pyxel 引擎开发的像素风格 RPG 游戏。

## 项目结构

```
RPG/
├── main.py              # 游戏入口文件
├── config.py            # 游戏配置（窗口大小、FPS等）
├── README.md            # 项目说明
├── requirements.txt     # Python 依赖
│
├── src/                 # 源代码目录
│   ├── __init__.py
│   ├── game.py          # 游戏主类
│   ├── scenes/          # 场景管理
│   │   ├── __init__.py
│   │   ├── scene_manager.py    # 场景管理器
│   │   ├── title_scene.py      # 标题场景
│   │   ├── game_scene.py       # 游戏场景
│   │   └── battle_scene.py     # 战斗场景
│   │
│   ├── entities/        # 游戏实体
│   │   ├── __init__.py
│   │   ├── player.py    # 玩家角色
│   │   ├── npc.py       # NPC
│   │   ├── enemy.py     # 敌人
│   │   └── item.py      # 物品
│   │
│   ├── systems/         # 游戏系统
│   │   ├── __init__.py
│   │   ├── input_handler.py    # 输入处理
│   │   ├── collision.py        # 碰撞检测
│   │   ├── combat.py           # 战斗系统
│   │   ├── inventory.py        # 背包系统
│   │   ├── dialogue.py         # 对话系统
│   │   └── save_load.py        # 存档系统
│   │
│   ├── map/             # 地图相关
│   │   ├── __init__.py
│   │   ├── tilemap.py   # 瓦片地图
│   │   ├── camera.py    # 相机/视口
│   │   └── world.py     # 世界管理
│   │
│   ├── ui/              # UI 界面
│   │   ├── __init__.py
│   │   ├── hud.py       # 游戏内 HUD
│   │   ├── menu.py      # 菜单
│   │   └── textbox.py   # 文本框
│   │
│   └── utils/           # 工具函数
│       ├── __init__.py
│       ├── helpers.py   # 辅助函数
│       └── constants.py # 常量定义
│
├── assets/              # 游戏资源
│   ├── images/          # 图片资源
│   │   ├── characters/  # 角色精灵图
│   │   ├── tiles/       # 地图瓦片
│   │   ├── items/       # 物品图标
│   │   └── ui/          # UI 元素
│   │
│   ├── sounds/          # 音效
│   │   ├── bgm/         # 背景音乐
│   │   └── sfx/         # 音效
│   │
│   └── my_resource.pyxres  # Pyxel 资源文件
│
├── data/                # 游戏数据
│   ├── maps/            # 地图数据 (JSON/YAML)
│   ├── enemies.json     # 敌人数据
│   ├── items.json       # 物品数据
│   ├── dialogues.json   # 对话数据
│   └── quests.json      # 任务数据
│
└── saves/               # 存档目录
    └── .gitkeep
```

## 环境配置

```bash
# 激活 conda 环境
conda activate pyxel_env

# 安装依赖
pip install -r requirements.txt

# 运行游戏
python main.py
```

## 开发说明

- **Pyxel** 是一个复古游戏引擎，分辨率为 256x256，支持 16 色调色板
- 使用 Pyxel Editor 编辑资源文件：`pyxel edit assets/my_resource.pyxres`
- 支持最多 3 个图像库、8 个瓦片地图和 64 个音效

## 游戏架构

1. **场景系统**：管理不同游戏场景（标题、游戏、战斗等）
2. **实体系统**：玩家、NPC、敌人等游戏对象
3. **系统模块**：输入、碰撞、战斗、对话等核心系统
4. **地图系统**：瓦片地图加载和相机跟随
