# -*- coding: utf-8 -*-
"""
场景管理器
管理游戏场景的切换和更新
"""

from enum import Enum, auto


class SceneType(Enum):
    """场景类型枚举"""
    TITLE = auto()              # 标题场景
    LLM_SETUP = auto()          # LLM设置场景
    CHARACTER_CREATION = auto() # 角色创建场景
    GAME = auto()               # 游戏场景
    BATTLE = auto()             # 战斗场景
    MENU = auto()               # 菜单场景


class SceneManager:
    """场景管理器"""
    
    def __init__(self):
        """初始化场景管理器"""
        self.scenes = {}
        self.current_scene = None
        self.current_scene_type = None

        # 运行时 LLM 配置（仅本次运行有效）
        self.llm_settings = {
            "enabled": False,
            "api_key": "",
            "base_url": "",
            "model": ""
        }
        
        # 注册并设置初始场景
        self._register_scenes()
        self.change_scene(SceneType.TITLE)
        
    def _register_scenes(self):
        """注册所有场景"""
        from src.scenes.title_scene import TitleScene
        from src.scenes.llm_setup_scene import LLMSetupScene
        from src.scenes.character_creation import CharacterCreationScene
        from src.scenes.game_scene import GameScene
        from src.scenes.battle_scene import BattleScene
        
        self.scenes[SceneType.TITLE] = TitleScene(self)
        self.scenes[SceneType.LLM_SETUP] = LLMSetupScene(self)
        self.scenes[SceneType.CHARACTER_CREATION] = CharacterCreationScene(self)
        self.scenes[SceneType.GAME] = GameScene(self)
        self.scenes[SceneType.BATTLE] = BattleScene(self)
        
        # 用于存储玩家创建的数据
        self.player_data = None
        
    def change_scene(self, scene_type: SceneType):
        """切换场景"""
        if scene_type in self.scenes:
            if self.current_scene:
                self.current_scene.on_exit()
            self.current_scene_type = scene_type
            self.current_scene = self.scenes[scene_type]
            self.current_scene.on_enter()
            
    def update(self):
        """更新当前场景"""
        if self.current_scene:
            self.current_scene.update()
            
    def draw(self):
        """绘制当前场景"""
        if self.current_scene:
            self.current_scene.draw()
