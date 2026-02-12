# -*- coding: utf-8 -*-
"""校园地图数据 - 北京外国语大学风格"""

# 瓦片类型定义
TILE_GRASS = 0
TILE_PATH = 1
TILE_BUILDING = 2
TILE_BUILDING_DOOR = 3
TILE_PLAYGROUND = 4
TILE_PLAYGROUND_GREEN = 5
TILE_TREE = 6
TILE_FLOWER = 7
TILE_GATE_PILLAR = 8
TILE_GATE_TOP = 9
TILE_GATE_PASS = 10
TILE_FENCE = 11
TILE_WATER = 12
TILE_BRIDGE = 13
TILE_LIBRARY = 14
TILE_LIBRARY_WINDOW = 15
TILE_DOME = 16
TILE_DOME_ARCH = 17
TILE_GRASS_DARK = 18
TILE_BUSH = 19
TILE_CANTEEN = 20       # 食堂
TILE_ADMIN = 21         # 行政楼
TILE_HALL = 22          # 礼堂
TILE_GYM = 23           # 体育馆
TILE_JAPAN = 24         # 日本楼
TILE_MAIN = 25          # 主楼
TILE_PLAZA = 26         # 小广场地砖
TILE_MAIN_WING = 32     # 主楼侧翼
TILE_MAIN_COURT = 33    # 主楼庭院
# 地下通道瓦片
TILE_TUNNEL_WALL = 27   # 通道墙壁
TILE_TUNNEL_FLOOR = 28  # 通道地面
TILE_TUNNEL_LIGHT = 29  # 通道灯光
TILE_TUNNEL_ENTRY = 30  # 通道入口
TILE_TUNNEL_EXIT = 31   # 通道出口（另一端）

# 图书馆内部瓦片
TILE_LIB_WALL = 40      # 图书馆墙壁
TILE_LIB_FLOOR = 41     # 图书馆地板
TILE_LIB_BOOKSHELF = 42 # 书架
TILE_LIB_CHAIR = 43     # 椅子
TILE_LIB_TABLE = 44     # 桌子
TILE_LIB_DOOR = 45      # 入口门
TILE_LIB_COUNTER = 46   # 服务台

MAP_TILES_WIDTH = 40
MAP_TILES_HEIGHT = 40

# 简写定义
G, P, D, T, W, R, F = 0, 1, 3, 6, 12, 4, 5
L, LW, M, MA, FE = 14, 15, 16, 17, 11
GP, GT, GS = 8, 9, 10
CA, AD, HA, GY, JP, MN, PL = 20, 21, 22, 23, 24, 25, 26
MW, MC = 32, 33  # 主楼侧翼、主楼庭院

# 图书馆内部简写
LW_WALL, LW_FLOOR, LW_BOOK, LW_CHAIR, LW_TABLE, LW_DOOR, LW_CTR = 40, 41, 42, 43, 44, 45, 46

# 校园地图 40x40
# 布局参考：清真寺(M)在上中, 食堂(CA)右上, 行政楼(AD)左中, 图书馆(L)中间
# 池塘(W)右中, 礼堂(HA)中左, 体育馆(GY)中右, 小广场(PL)中间
# 操场(R/F)中下, 日本楼(JP)右下, 主楼(MN)左下, 校门底部中间
CAMPUS_MAP = [
    [FE]*40,  # 第0行：围栏
    [G,G,T,G,G,G,G,G,G,G,M,M,M,M,M,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,T,G],
    [G,G,G,G,G,G,G,G,G,G,M,M,M,M,M,P,P,P,P,P,P,P,P,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,T,G,G,G,G,G,G,G,G,M,M,M,M,M,P,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,T,G],
    [G,G,G,G,G,G,G,G,G,G,M,MA,MA,MA,M,P,G,G,G,G,G,G,G,P,G,G,G,G,CA,CA,CA,CA,CA,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,P,P,P,P,P,G,G,G,G,G,G,G,P,G,G,G,G,CA,CA,CA,CA,CA,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,P,G,G,G,G,G,G,G,P,G,G,G,G,CA,CA,D,CA,CA,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,P,G,G,G,G,G,G,G,P,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,P,L,L,L,L,L,L,L,L,P,P,P,P,P,P,P,P,P,P,P,G,G,G,G,G,G,G,G,G],
    [G,G,AD,AD,AD,AD,AD,G,G,G,G,P,L,LW,LW,LW,LW,LW,LW,L,P,G,G,G,W,W,W,W,W,W,W,G,G,G,G,G,G,G,T,G],
    [G,G,AD,AD,AD,AD,AD,G,G,G,G,P,L,LW,LW,LW,LW,LW,LW,L,P,G,G,G,W,W,W,W,W,W,W,W,G,G,G,G,G,G,G,G],
    [G,G,AD,AD,D,AD,AD,G,G,G,G,P,L,L,D,L,L,L,L,L,P,G,G,G,W,W,W,W,W,W,W,W,G,G,G,G,G,G,G,G],
    [G,G,G,G,P,G,G,G,G,G,G,P,G,G,P,G,G,G,G,G,P,G,G,G,W,W,W,W,W,W,W,G,G,G,G,G,G,G,G,G],
    [G,T,G,G,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,G,G,G,T,G,G],
    [G,G,G,G,G,G,G,G,HA,HA,HA,HA,HA,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,GY,GY,GY,GY,GY,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,HA,HA,HA,HA,HA,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,GY,GY,GY,GY,GY,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,HA,HA,D,HA,HA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,GY,GY,D,GY,GY,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,P,G,G,P,PL,PL,PL,PL,PL,PL,PL,PL,PL,PL,P,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G],
    [G,T,G,G,G,G,G,G,G,G,P,G,G,P,PL,PL,PL,PL,PL,PL,PL,PL,PL,PL,P,G,G,G,G,G,G,G,P,G,G,G,G,T,G,G],
    [G,G,G,G,G,G,G,G,G,G,P,G,G,P,PL,PL,PL,PL,PL,PL,PL,PL,PL,PL,P,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,P,P,P,P,PL,PL,PL,PL,PL,PL,PL,PL,PL,PL,P,P,P,P,P,P,P,P,P,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,G,G,G,G,G,JP,JP,JP,JP,JP,G,G,G,G,G,G],
    [G,G,G,G,G,G,R,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,R,G,G,G,G,G,JP,JP,JP,JP,JP,G,G,G,G,G,G],
    [G,T,G,G,G,G,R,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,R,G,G,G,G,G,JP,JP,D,JP,JP,G,G,G,G,T,G],
    [G,G,G,G,G,G,R,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,R,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,R,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,R,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,R,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,R,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G],
    [G,T,G,G,G,G,G,G,G,G,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,G,G,G,G,G,G,T,G],
    [G,G,G,G,MW,MW,MN,MN,MN,MN,MN,MN,MN,MW,MW,P,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,MW,MW,MN,MN,MN,MN,MN,MN,MN,MW,MW,P,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,MW,MW,MC,MC,MC,D,MC,MC,MC,MW,MW,P,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,P,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,P,P,P,P,P,P,P,P,P,P,P,P,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,GP,GT,GT,GT,GT,GT,GT,GP,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE],
    [G,G,G,G,G,G,G,G,G,G,G,G,GP,GS,GS,GS,GS,GS,GS,GP,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,GP,GS,GS,GS,GS,GS,GS,GP,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,P,P,P,P,P,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,P,P,P,P,P,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
]

# 碰撞地图
COLLISION_MAP = []
for row in CAMPUS_MAP:
    collision_row = []
    for tile in row:
        if tile in [14, 15, 16, 12, 11, 6, 8, 20, 21, 22, 23, 24, 25, 32]:
            collision_row.append(1)
        else:
            collision_row.append(0)
    COLLISION_MAP.append(collision_row)

# 校门位置
GATE_POSITION = {"left_pillar_x": 12, "right_pillar_x": 19, "top_y": 35, "bottom_y": 37}

# 树木位置
TREE_POSITIONS = [(x, y) for y, row in enumerate(CAMPUS_MAP) for x, tile in enumerate(row) if tile == 6]

# 玩家初始位置（东校区校门内侧）
PLAYER_START_TILE_X = 16
PLAYER_START_TILE_Y = 34  # 校门内侧（第35行是围栏/校门）

# NPC数据
NPC_DATA = [
    {"id": "student_1", "name": "小明", "type": "student", "x": 18*16, "y": 18*16, "direction": "down",
     "dialogues": ["你好！欢迎来到北外！", "图书馆在北边，很大的那栋楼。"], "personality": "北外英语系学生。"},
    {"id": "student_2", "name": "小红", "type": "student_female", "x": 14*16, "y": 22*16, "direction": "right",
     "dialogues": ["你好呀！", "操场很大，可以踢足球~"], "personality": "北外法语系学生。"},
    {"id": "student_3", "name": "小李", "type": "student", "x": 21*16, "y": 12*16, "direction": "left",
     "dialogues": ["我刚从图书馆出来。", "那里的书很全！"], "personality": "北外日语系学生。"},
    {"id": "professor_1", "name": "王教授", "type": "professor", "x": 24*16, "y": 28*16, "direction": "left",
     "can_play_football": True, "dialogues": ["同学你好。", "主楼是我们学校的标志性建筑。"], "personality": "北外资深教授。"},
    {"id": "professor_2", "name": "李老师", "type": "professor", "x": 11*16, "y": 17*16, "direction": "right",
     "can_play_football": True, "dialogues": ["欢迎来到北外！", "小广场经常有活动。"], "personality": "阿拉伯语系老师。"},
    {"id": "canteen_staff", "name": "张阿姨", "type": "staff", "x": 27*16, "y": 6*16, "direction": "right",
     "dialogues": ["同学吃饭了吗？", "今天有红烧肉！"], "personality": "食堂工作人员。"},
    {"id": "student_japan", "name": "田中", "type": "student", "x": 28*16, "y": 23*16, "direction": "right",
     "dialogues": ["你好！我是日本留学生。", "日本楼是我上课的地方。"], "personality": "日本留学生。"},
]

# 猫咪数据
CAT_DATA = [
    {"id": "cat_orange_1", "name": "大橘", "type": "cat_orange", "x": 20*16, "y": 19*16, "dialogues": ["喵~"], "personality": "小广场的橘猫。"},
    {"id": "cat_orange_2", "name": "小橙", "type": "cat_orange", "x": 21*16, "y": 8*16, "dialogues": ["喵喵喵~"], "personality": "活泼的橘猫。"},
    {"id": "cat_calico", "name": "花花", "type": "cat_calico", "x": 24*16, "y": 9*16, "dialogues": ["喵？"], "personality": "池塘边的三花猫，喜欢看锦鲤。"},
    {"id": "cat_black", "name": "小黑", "type": "cat_black", "x": 5*16, "y": 12*16, "dialogues": ["喵..."], "personality": "行政楼附近的黑猫。"},
    {"id": "cat_calico_2", "name": "斑斑", "type": "cat_calico", "x": 25*16, "y": 25*16, "dialogues": ["喵~"], "personality": "日本楼旁的三花猫。"},
    {"id": "cat_orange_3", "name": "胖胖", "type": "cat_orange", "x": 16*16, "y": 37*16, "dialogues": ["喵喵！"], "personality": "校门口的橘猫。"},
]


# ========== 地下通道地图 (20x30) ==========
# 从东校区到西校区：从上往下走
# TW=墙壁, TF=地面, TL=灯光, TE=入口(上), TX=出口(下)
TUNNEL_WIDTH = 20
TUNNEL_HEIGHT = 30

TW, TF, TL, TE, TX = 27, 28, 29, 30, 31

TUNNEL_MAP = [
    [TW,TW,TW,TW,TW,TW,TW,TE,TE,TE,TE,TE,TE,TW,TW,TW,TW,TW,TW,TW],  # 入口（从东校区来）
    [TW,TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TL,TF,TF,TL,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TL,TF,TF,TL,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TL,TF,TF,TL,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TL,TF,TF,TL,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TL,TF,TF,TL,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TL,TF,TF,TL,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TF,TF,TF,TF,TF,TF,TF,TF,TW,TW,TW,TW,TW,TW],
    [TW,TW,TW,TW,TW,TW,TW,TX,TX,TX,TX,TX,TX,TW,TW,TW,TW,TW,TW,TW],  # 出口（通往西校区）
]

# 地下通道碰撞地图
TUNNEL_COLLISION_MAP = []
for i, row in enumerate(TUNNEL_MAP):
    collision_row = []
    for j, tile in enumerate(row):
        if tile == TW:  # 墙壁不可通行
            collision_row.append(1)
        # 第27行（索引26-27）中间位置设置为施工区域不可通行
        elif i in [26, 27] and 7 <= j <= 12:
            collision_row.append(1)  # 施工牌子区域
        else:
            collision_row.append(0)
    TUNNEL_COLLISION_MAP.append(collision_row)


# ========== 西校区地图 (40x40) ==========
# 简单版本：校门在上方，其余为空地
WEST_MAP_WIDTH = 40
WEST_MAP_HEIGHT = 40

WEST_CAMPUS_MAP = [
    [G,G,G,G,G,G,G,G,G,G,G,G,G,P,P,P,P,P,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,P,P,P,P,P,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,GP,GS,GS,GS,GS,GS,GS,GP,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,GP,GS,GS,GS,GS,GS,GS,GP,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,GP,GT,GT,GT,GT,GT,GT,GP,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,T,G,G,G,G,G,G,G,G,G,G,G,P,P,P,P,P,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,T,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,T,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,T,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,T,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,T,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,T,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,T,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,T,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,T,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,T,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,T,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,P,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],
    [FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE],
    [FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE,FE],
]

# 西校区碰撞地图
WEST_COLLISION_MAP = []
for row in WEST_CAMPUS_MAP:
    collision_row = []
    for tile in row:
        if tile in [TILE_LIBRARY, TILE_LIBRARY_WINDOW, TILE_DOME, TILE_WATER, 
                    TILE_FENCE, TILE_TREE, TILE_GATE_PILLAR, TILE_CANTEEN, 
                    TILE_ADMIN, TILE_HALL, TILE_GYM, TILE_JAPAN, TILE_MAIN]:
            collision_row.append(1)
        else:
            collision_row.append(0)
    WEST_COLLISION_MAP.append(collision_row)

# 西校区校门位置
WEST_GATE_POSITION = {"left_pillar_x": 12, "right_pillar_x": 19, "top_y": 4, "bottom_y": 1}

# 西校区树木位置
WEST_TREE_POSITIONS = [(x, y) for y, row in enumerate(WEST_CAMPUS_MAP) for x, tile in enumerate(row) if tile == TILE_TREE]

# ========== 图书馆内部地图 (16x12) ==========
# 书架、桌椅、服务台布局
LIBRARY_WIDTH = 16
LIBRARY_HEIGHT = 12

# 简写
_W, _F, _B, _C, _T, _D, _R = LW_WALL, LW_FLOOR, LW_BOOK, LW_CHAIR, LW_TABLE, LW_DOOR, LW_CTR

LIBRARY_MAP = [
    [_W,_W,_W,_W,_W,_W,_W,_W,_W,_W,_W,_W,_W,_W,_W,_W],  # 北墙
    [_W,_B,_B,_F,_F,_F,_F,_F,_F,_F,_F,_F,_B,_B,_B,_W],  # 书架排
    [_W,_B,_B,_F,_F,_F,_F,_F,_F,_F,_F,_F,_B,_B,_B,_W],  # 书架排
    [_W,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_W],  # 通道
    [_W,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_W],  # 通道
    [_W,_B,_B,_F,_F,_F,_F,_F,_F,_F,_F,_F,_B,_B,_B,_W],  # 书架排
    [_W,_B,_B,_F,_F,_F,_F,_F,_F,_F,_F,_F,_B,_B,_B,_W],  # 书架排
    [_W,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_F,_W],  # 通道
    [_W,_B,_B,_F,_F,_F,_F,_F,_F,_F,_F,_F,_B,_B,_B,_W],  # 书架
    [_W,_F,_F,_F,_F,_R,_R,_R,_R,_F,_F,_F,_F,_F,_F,_W],  # 服务台
    [_W,_F,_F,_F,_F,_F,_F,_D,_F,_F,_F,_F,_F,_F,_F,_W],  # 入口
    [_W,_W,_W,_W,_W,_W,_W,_D,_W,_W,_W,_W,_W,_W,_W,_W],  # 南墙+门
]

# 图书馆碰撞地图
LIBRARY_COLLISION_MAP = []
for row in LIBRARY_MAP:
    collision_row = []
    for tile in row:
        if tile in [_W, _B, _T, _R]:  # 墙壁、书架、桌子、服务台不可通行
            collision_row.append(1)
        else:
            collision_row.append(0)
    LIBRARY_COLLISION_MAP.append(collision_row)

# 图书馆内NPC数据
LIBRARY_NPC_DATA = []

# 图书馆书架内容（不同位置显示不同语言的书）
LIBRARY_BOOKSHELF_CONTENT = {
    # 左侧书架（亚洲语言）
    (1, 1): {"title": "日语书架", "books": ["《源氏物语》", "《挪威的森林》", "《日语语法大全》"]},
    (2, 1): {"title": "韩语书架", "books": ["《韩语入门》", "《朝鲜半岛史》", "《韩国文化研究》"]},
    (1, 2): {"title": "阿拉伯语书架", "books": ["《一千零一夜》", "《古兰经研究》", "《阿拉伯语教程》"]},
    (2, 2): {"title": "泰语书架", "books": ["《泰语基础》", "《东南亚文化》", "《泰国历史》"]},
    # 右侧书架（欧洲语言）
    (12, 1): {"title": "英语书架", "books": ["《莎士比亚全集》", "《傲慢与偏见》", "《英语词汇学》"]},
    (13, 1): {"title": "法语书架", "books": ["《悲惨世界》", "《小王子》", "《法语语法》"]},
    (14, 1): {"title": "德语书架", "books": ["《浮士德》", "《少年维特的烦恼》", "《德语教程》"]},
    (12, 2): {"title": "西班牙语书架", "books": ["《堂吉诃德》", "《百年孤独》", "《西班牙语入门》"]},
    (13, 2): {"title": "俄语书架", "books": ["《战争与和平》", "《罪与罚》", "《俄语语法》"]},
    (14, 2): {"title": "意大利语书架", "books": ["《神曲》", "《十日谈》", "《意大利语基础》"]},
    # 左下书架
    (1, 5): {"title": "中文古典", "books": ["《红楼梦》", "《三国演义》", "《诗经》"]},
    (2, 5): {"title": "中文现代", "books": ["《围城》", "《活着》", "《平凡的世界》"]},
    (1, 6): {"title": "语言学", "books": ["《语言学概论》", "《索绪尔语言学》", "《对比语言学》"]},
    (2, 6): {"title": "翻译学", "books": ["《翻译理论与实践》", "《口译技巧》", "《文学翻译研究》"]},
    # 右下书架
    (12, 5): {"title": "葡萄牙语书架", "books": ["《葡萄牙语入门》", "《巴西文化》", "《葡语会话》"]},
    (13, 5): {"title": "波兰语书架", "books": ["《波兰语教程》", "《东欧文学》", "《波兰历史》"]},
    (14, 5): {"title": "希腊语书架", "books": ["《伊利亚特》", "《希腊神话》", "《现代希腊语》"]},
    (12, 6): {"title": "荷兰语书架", "books": ["《荷兰语基础》", "《低地国家文化》", "《商务荷兰语》"]},
    (13, 6): {"title": "瑞典语书架", "books": ["《瑞典语入门》", "《北欧文学》", "《斯堪的纳维亚研究》"]},
    (14, 6): {"title": "越南语书架", "books": ["《越南语教程》", "《越南历史》", "《东南亚政治》"]},
    # 底部书架
    (1, 8): {"title": "外交学", "books": ["《外交学概论》", "《国际关系》", "《外交礼仪》"]},
    (2, 8): {"title": "国际贸易", "books": ["《国际贸易实务》", "《商务英语》", "《跨文化沟通》"]},
    (12, 8): {"title": "新闻传播", "books": ["《新闻学概论》", "《国际传播》", "《媒体英语》"]},
    (13, 8): {"title": "法学", "books": ["《国际法》", "《外交法》", "《比较法学》"]},
    (14, 8): {"title": "经济学", "books": ["《国际经济学》", "《发展经济学》", "《宏观经济学》"]},
}