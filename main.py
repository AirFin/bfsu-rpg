#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
校园 RPG 游戏入口
使用 Pyxel 引擎开发
"""

import os
import pyxel
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS, RESOURCE_FILE
from src.game import Game
from src.utils.font_manager import init_font


def main():
    """游戏主入口"""
    # 初始化 Pyxel
    pyxel.init(
        WINDOW_WIDTH, 
        WINDOW_HEIGHT, 
        title=WINDOW_TITLE, 
        fps=FPS
    )
    
    # 加载自定义字体
    init_font("assets/font/ark-pixel-12px-proportional-zh_cn.bdf")
    
    # 加载资源文件（如果存在）
    if os.path.exists(RESOURCE_FILE):
        try:
            pyxel.load(RESOURCE_FILE)
            print(f"已加载资源文件: {RESOURCE_FILE}")
        except Exception as e:
            print(f"加载资源文件失败: {e}")
    else:
        print(f"资源文件 {RESOURCE_FILE} 不存在，使用程序绘制")
    
    # 创建并运行游戏
    game = Game()
    pyxel.run(game.update, game.draw)


if __name__ == "__main__":
    main()
