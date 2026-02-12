# -*- coding: utf-8 -*-
"""
AI 对话系统模块
支持玩家与 NPC 进行实时文字对话
"""

import pyxel
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_WHITE, COLOR_BLACK
from src.systems.llm_client import get_llm_client
from src.utils.font_manager import draw_text, text_width

# 各NPC的专属问候语（根据人设定制）
NPC_GREETINGS = {
    # 学生
    "小明": [
        "Hi there! 有什么事吗？",
        "欢迎来到北外！我是英语系的~",
        "Hey! 你是新生吗？",
        "今天有English corner，要一起来吗？",
        "Nice to meet you!",
    ],
    "小红": [
        "Bonjour! 你好呀~",
        "嗨！今天天气真好呢！",
        "你也喜欢在这里散步吗？",
        "哎呀，被你发现我在偷懒了~",
        "Salut! 有什么事？",
    ],
    "小李": [
        "こんにちは！啊，你好！",
        "刚从图书馆出来，眼睛好累...",
        "你也是来借书的吗？",
        "今天在看村上春树的书~",
        "哦，你好你好！",
    ],
    # 教授
    "王教授": [
        "哦，同学你好。",
        "有什么学术问题要讨论吗？",
        "年轻人要多读书啊。",
        "今天的天气适合散步。",
        "嗯？有事找我？",
    ],
    "李老师": [
        "مرحبا！啊，你好！",
        "阿拉伯语很有趣的，要学吗？",
        "同学好！今天精神不错嘛。",
        "小广场的活动你参加了吗？",
        "有什么我可以帮忙的？",
    ],
    # 工作人员
    "张阿姨": [
        "哎哟，同学来啦！",
        "吃饭了没？今天有好菜！",
        "来来来，阿姨给你多打点！",
        "学习辛苦了，要吃饱饭啊！",
        "今天想吃点什么？",
    ],
    # 留学生
    "田中": [
        "あ、こんにちは！",
        "你好！我日语说得不太好...",
        "北外的校园真漂亮呢！",
        "我来中国留学一年了~",
        "えーと...你好你好！",
    ],
    # 猫咪
    "大橘": ["喵~", "喵喵？", "呼噜呼噜...", "喵！（伸懒腰）", "...zzZ"],
    "小橙": ["喵喵喵！", "喵~喵~", "（蹭蹭）", "喵！（跳来跳去）", "喵喵！"],
    "花花": ["喵？", "喵...（盯着池塘）", "（舔爪子）", "喵~（看鱼）", "呼噜..."],
    "小黑": ["喵...", "...（警惕地看着你）", "喵。", "（眯眼睛）", "...喵"],
    "斑斑": ["喵~", "喵喵？", "（晒太阳）", "喵~（打哈欠）", "（翻肚皮）"],
    "胖胖": ["喵喵！", "喵~（摇尾巴）", "喵！喵！", "（期待地看着你）", "喵喵喵~"],
}

# 默认问候语（如果NPC不在列表中）
DEFAULT_GREETINGS = [
    "嗨，有什么事吗？",
    "哦，是你啊！",
    "有什么我能帮你的吗？",
    "今天天气不错呢~",
    "你好！",
]


class AIDialogueSystem:
    """AI 驱动的对话系统"""
    
    def __init__(self):
        """初始化 AI 对话系统"""
        self.active = False
        self.npc_name = ""
        self.npc_personality = ""
        self.npc_can_play_football = False  # NPC是否可以踢足球
        
        # 对话历史
        self.conversation_history = []
        
        # 输入相关
        self.input_text = ""
        self.input_active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        
        # 显示相关
        self.npc_response = ""
        self.response_display_index = 0  # 打字机效果
        self.text_speed = 2
        self.frame_counter = 0
        
        # 状态
        self.waiting_for_response = False
        self.show_exit_hint = True
        self.failure_message = None  # 一次性失败提示
        
        # LLM 客户端
        self.llm = get_llm_client()
        
        # 输入延迟（防止重复输入）
        self.input_delay = 0
        
        # 动作回调
        self.action_callback = None  # 当NPC需要执行动作时的回调函数
        self.pending_action = None  # 待执行的动作
        
    def start_dialogue(self, npc_name, npc_personality, can_play_football=False):
        """
        开始与 NPC 的 AI 对话
        
        参数:
            npc_name: NPC 名称
            npc_personality: NPC 人物设定描述
            can_play_football: NPC 是否可以踢足球
        """
        self.active = True
        self.npc_name = npc_name
        self.npc_personality = npc_personality
        self.npc_can_play_football = can_play_football
        self.conversation_history = []
        self.input_text = ""
        # 根据NPC名字选择专属问候语
        greetings = NPC_GREETINGS.get(npc_name, DEFAULT_GREETINGS)
        self.npc_response = random.choice(greetings)
        self.response_display_index = 0
        self.waiting_for_response = False
        self.input_active = True
        self.pending_action = None
        self.failure_message = None
        
        # 清空 Pyxel 的输入缓冲
        pyxel.input_text
        
    def end_dialogue(self):
        """结束对话"""
        # 注意：不清空 pending_action，让 game_scene 在下一帧处理
        self.active = False
        self.conversation_history = []
        self.input_text = ""
        self.npc_response = ""
        self.waiting_for_response = False
        self.input_active = True
        
    def set_action_callback(self, callback):
        """设置动作回调函数"""
        self.action_callback = callback
        
    def update(self):
        """更新对话系统"""
        if not self.active:
            return
            
        # 如果正在等待响应，检查队列
        if self.waiting_for_response:
            response = self.llm.check_response()
            if response is not None:
                print(f"[AI对话] 收到回复: {response}")
                self._process_response(response)
                if not self.active:
                    return
            
        # 更新输入延迟
        if self.input_delay > 0:
            self.input_delay -= 1
            
        # 光标闪烁
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible
            
        # 打字机效果
        if self.response_display_index < len(self.npc_response):
            self.frame_counter += 1
            if self.frame_counter >= self.text_speed:
                self.frame_counter = 0
                self.response_display_index += 1
                
        # 检查 TAB 键退出
        if pyxel.btnp(pyxel.KEY_TAB):
            self.end_dialogue()
            return
            
        # 如果正在等待回复，不处理输入
        if self.waiting_for_response:
            return
            
        # 处理文字输入
        if self.input_active:
            self._handle_text_input()
            
    def _handle_text_input(self):
        """处理文字输入"""
        # 获取输入的文字
        input_chars = pyxel.input_text
        if input_chars and self.input_delay == 0:
            for char in input_chars:
                # 过滤控制字符
                if ord(char) >= 32:  # 可打印字符
                    self.input_text += char
                    
        # 退格键删除
        if pyxel.btnp(pyxel.KEY_BACKSPACE, 10, 3):
            if self.input_text:
                self.input_text = self.input_text[:-1]
                
        # 回车键发送
        if pyxel.btnp(pyxel.KEY_RETURN) and self.input_delay == 0:
            if self.input_text.strip():
                self._send_message()
                self.input_delay = 10
                
    def _send_message(self):
        """发送消息给 AI"""
        user_message = self.input_text.strip()
        if not user_message:
            return
            
        # 添加到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # 清空输入
        self.input_text = ""
        
        # 显示等待状态
        self.npc_response = "正在思考..."
        self.response_display_index = 0
        self.waiting_for_response = True
        self.input_active = False
        
        # 构建消息
        messages = self._build_messages()
        
        # 打印调试信息
        print(f"[AI对话] 发送消息: {user_message}")
        
        # 异步请求 AI（使用队列方式）
        self.llm.chat_async(messages, None)
        
    def _build_messages(self):
        """构建发送给 AI 的消息列表"""
        # 构建可用动作列表
        available_actions = ""
        if self.npc_can_play_football:
            available_actions = """

你可以执行的动作：
- 如果玩家请求你去踢足球/踢球/运动，你可以答应并在回复末尾加上 [动作:踢足球]
- 只有当玩家明确请求时才触发动作
- 动作标签必须放在回复的最后"""
        
        # 系统提示词 - 使用中文回复
        system_prompt = f"""你是一个名叫"{self.npc_name}"的游戏NPC角色。
{self.npc_personality}

对话规则：
1. 始终保持角色扮演，用第一人称回应
2. 回复要简短自然，像真人对话一样（控制在50字以内）
3. 可以表达情绪和性格
4. 不要跳出角色或提及自己是AI
5. 用中文回复{available_actions}"""

        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加对话历史（最近10轮）
        history = self.conversation_history[-20:]  # 最多10轮对话
        messages.extend(history)
        
        return messages
            
    def _process_response(self, response):
        """在主线程中处理响应"""
        if response == "(AI not enabled)" or response.startswith("(Error:"):
            self.failure_message = "LLM失败，已切换预设回复"
            print(f"[AI对话] 检测到失败响应，准备降级: {response}")
            self.end_dialogue()
            return

        # 检查是否包含动作指令
        action = None
        display_response = response
        
        if '[动作:踢足球]' in response:
            action = 'play_football'
            display_response = response.replace('[动作:踢足球]', '').strip()
            self.pending_action = action
            print(f"[AI对话] 检测到动作指令: {action}")
        
        self.npc_response = display_response
        self.response_display_index = 0
        self.waiting_for_response = False
        self.input_active = True
        
        # 添加到对话历史（保存原始响应）
        self.conversation_history.append({
            "role": "assistant",
            "content": display_response
        })

    def consume_failure_message(self):
        """获取失败提示（一次性）"""
        message = self.failure_message
        self.failure_message = None
        return message
        
    def draw(self):
        """绘制对话界面"""
        if not self.active:
            return
            
        # 半透明背景覆盖
        for y in range(0, WINDOW_HEIGHT, 2):
            pyxel.line(0, y, WINDOW_WIDTH, y, 0)
            
        # 对话框背景
        box_x = 10
        box_y = 30
        box_w = WINDOW_WIDTH - 20
        box_h = WINDOW_HEIGHT - 60
        
        # 主对话框
        pyxel.rect(box_x, box_y, box_w, box_h, 1)
        pyxel.rectb(box_x, box_y, box_w, box_h, 7)
        pyxel.rectb(box_x + 2, box_y + 2, box_w - 4, box_h - 4, 12)
        
        # NPC 名称标签
        name_w = text_width(self.npc_name) + 12
        pyxel.rect(box_x + 8, box_y - 6, name_w, 14, 1)
        draw_text(box_x + 12, box_y - 4, self.npc_name, 10)
        
        # 绘制 NPC 回复区域
        self._draw_response_area(box_x, box_y, box_w)
        
        # 绘制输入区域
        self._draw_input_area(box_x, box_y + box_h - 40, box_w)
        
        # 绘制提示
        self._draw_hints()
        
    def _draw_response_area(self, box_x, box_y, box_w):
        """绘制 NPC 回复区域"""
        # 回复区域背景
        response_y = box_y + 14
        response_h = WINDOW_HEIGHT - 130
        pyxel.rect(box_x + 8, response_y, box_w - 16, response_h, 0)
        
        # 显示 NPC 回复（带打字机效果）
        display_text = self.npc_response[:self.response_display_index]
        
        # 文字换行 - 根据对话框宽度计算
        max_width = box_w - 28
        lines = self._wrap_text(display_text, max_width)
            
        # 计算可显示的行数（中文字体高度约14像素）
        line_height = 14
        max_lines = (response_h - 20) // line_height
        for i, line in enumerate(lines[-max_lines:]):
            draw_text(box_x + 12, response_y + 4 + i * line_height, line, 7)
            
        # 等待指示器
        if self.waiting_for_response:
            dots = "." * ((pyxel.frame_count // 20) % 4)
            draw_text(box_x + 12, response_y + response_h - 14, f"等待中{dots}", 6)
            
    def _draw_input_area(self, box_x, input_y, box_w):
        """绘制输入区域"""
        # 输入框背景
        input_h = 32
        pyxel.rect(box_x + 8, input_y, box_w - 16, input_h, 5)
        pyxel.rectb(box_x + 8, input_y, box_w - 16, input_h, 7)
        
        # 输入提示
        draw_text(box_x + 12, input_y + 4, "你:", 10)
        
        # 输入的文字 - 根据对话框宽度计算可显示字符数
        max_width = box_w - 40
        display_input = self.input_text
        while text_width(display_input) > max_width and len(display_input) > 0:
            display_input = "..." + display_input[4:]
            
        text_x = box_x + 12
        text_y = input_y + 16
        draw_text(text_x, text_y, display_input, 7)
        
        # 光标
        if self.input_active and self.cursor_visible:
            cursor_x = text_x + text_width(display_input)
            pyxel.rect(cursor_x, text_y, 2, 12, 7)
            
    def _draw_hints(self):
        """绘制操作提示"""
        hint_y = WINDOW_HEIGHT - 14
        draw_text(10, hint_y, "Enter:发送  Tab:退出", 6)
        
        # AI 状态指示
        if self.llm.is_available():
            draw_text(WINDOW_WIDTH - 60, hint_y, "[AI在线]", 11)
        else:
            draw_text(WINDOW_WIDTH - 70, hint_y, "[AI离线]", 8)
            
    def _wrap_text(self, text, max_width):
        """将文本按最大宽度换行"""
        lines = []
        current_line = ""
        
        for char in text:
            test_line = current_line + char
            if text_width(test_line) > max_width:
                if current_line:
                    lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
                
        if current_line:
            lines.append(current_line)
            
        return lines if lines else [""]
