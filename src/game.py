# -*- coding: utf-8 -*-
"""
游戏主类
管理游戏状态和场景
"""

import pyxel
import random
from src.scenes.scene_manager import SceneManager


class Game:
    """游戏主类"""
    
    def __init__(self):
        """初始化游戏"""
        self.scene_manager = SceneManager()
        
        # 音乐相关
        self.tones = ["t", "s", "p"]  # 三角波、方波、脉冲波
        self.current_tone_index = 2   # 当前使用脉冲波 (p)
        self.melody = self._get_melody()
        
        # 初始化背景音乐
        self._init_music()
        
        # 播放背景音乐（不循环，手动控制切换音色）
        pyxel.playm(0, loop=False)
        
    def _get_melody(self):
        """获取小星星旋律"""
        return (
            # 一闪一闪亮晶晶
            "c1 c1 g1 g1 a1 a1 g1 r "
            # 满天都是小星星
            "f1 f1 e1 e1 d1 d1 c1 r "
            # 挂在天空放光明
            "g1 g1 f1 f1 e1 e1 d1 r "
            # 好像许多小眼睛
            "g1 g1 f1 f1 e1 e1 d1 r "
            # 一闪一闪亮晶晶
            "c1 c1 g1 g1 a1 a1 g1 r "
            # 满天都是小星星
            "f1 f1 e1 e1 d1 d1 c1 r r r"
        )
        
    def _init_music(self):
        """初始化音乐 - 小星星 (Twinkle Twinkle Little Star)"""
        tone = self.tones[self.current_tone_index]
        
        # 设置音效1为小星星旋律
        pyxel.sounds[1].set(
            self.melody,  # notes: 音符序列
            tone,         # tones: 音色
            "3",          # volumes: 音量 (较低，柔和)
            "f",          # effects: 效果 (f=淡出，更柔和)
            45            # speed: 速度（更慢，更舒缓）
        )
        
        # 创建音乐轨道0
        pyxel.musics[0].set(
            [1],  # ch0: 使用sound 1
            [],   # ch1: 空
            [],   # ch2: 空
            []    # ch3: 空
        )
    
    def _switch_tone_and_replay(self):
        """切换音色并重新播放"""
        # 随机选择一个不同的音色
        available = [i for i in range(len(self.tones)) if i != self.current_tone_index]
        self.current_tone_index = random.choice(available)
        
        # 重新设置音乐
        self._init_music()
        
        # 重新播放
        pyxel.playm(0, loop=False)
        
    def update(self):
        """更新游戏逻辑（每帧调用）"""
        # 全局退出检测
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        # 检查音乐是否播放完毕，如果是则切换音色重新播放
        if not pyxel.play_pos(0):
            self._switch_tone_and_replay()
        
        # 更新当前场景
        self.scene_manager.update()
        
    def draw(self):
        """绘制游戏画面（每帧调用）"""
        # 清屏
        pyxel.cls(0)
        
        # 绘制当前场景
        self.scene_manager.draw()
