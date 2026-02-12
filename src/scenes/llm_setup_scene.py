# -*- coding: utf-8 -*-
"""
LLM 设置场景
在进入角色创建前，选择是否开启 LLM 并填写配置
"""

import pyxel
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from src.utils.font_manager import draw_text, text_width
from src.systems.llm_client import get_llm_client


class LLMSetupScene:
    """LLM 设置场景"""

    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.llm_client = get_llm_client()

        self.selected_option = 0
        self.options_count = 5  # 开启LLM、API Key、Base URL、Model、继续

        self.llm_enabled = False  # 默认关闭
        self.api_key = ""
        self.base_url = ""
        self.model = ""

        self.editing_field = False
        self.edit_field_index = -1

        self.cursor_visible = True
        self.cursor_timer = 0

        self.status_message = ""
        self.status_color = 7

    def on_enter(self):
        self.selected_option = 0
        self.editing_field = False
        self.edit_field_index = -1
        self.llm_enabled = False  # 每次进入默认关闭

        env_config = self.llm_client.read_env_config()
        self.api_key = env_config["api_key"]
        self.base_url = env_config["base_url"]
        self.model = env_config["model"]

        if self.api_key or self.base_url or self.model:
            self.status_message = "已从 .env 读取，可编辑"
            self.status_color = 11
        else:
            self.status_message = "未检测到 .env 配置，请手动填写"
            self.status_color = 8

    def on_exit(self):
        pass

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

        # 未进入编辑状态时，也允许在字段上直接粘贴
        if (not self.editing_field and self.llm_enabled and self.selected_option in [1, 2, 3]
                and self._is_paste_shortcut()):
            self.editing_field = True
            self.edit_field_index = self.selected_option
            if not self._paste_from_clipboard(self.edit_field_index):
                self.status_message = "未获取到粘贴内容，请再试一次"
                self.status_color = 8
            return

        if self.editing_field:
            self._handle_text_edit()
            return

        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.selected_option = (self.selected_option - 1) % self.options_count
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.selected_option = (self.selected_option + 1) % self.options_count

        if self.selected_option == 0:
            if (pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A) or
                    pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D)):
                self.llm_enabled = not self.llm_enabled

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            from src.scenes.scene_manager import SceneType
            self.scene_manager.change_scene(SceneType.TITLE)
            return

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE):
            self._confirm_current_option()

    def _confirm_current_option(self):
        if self.selected_option == 0:
            self.llm_enabled = not self.llm_enabled
            return

        if self.selected_option in [1, 2, 3]:
            if not self.llm_enabled:
                self.status_message = "请先开启LLM再编辑配置"
                self.status_color = 8
                return
            self.editing_field = True
            self.edit_field_index = self.selected_option
            return

        if self.selected_option == 4:
            self._continue_to_character_creation()

    def _handle_text_edit(self):
        current_value = self._get_field_value(self.edit_field_index)

        if self._is_paste_shortcut():
            if self._paste_from_clipboard(self.edit_field_index):
                self.status_message = "已粘贴"
                self.status_color = 11
            else:
                self.status_message = "无法读取剪贴板，请手动输入"
                self.status_color = 8
            return

        input_chars = pyxel.input_text
        if input_chars:
            for char in input_chars:
                if ord(char) >= 32 and len(current_value) < 160:
                    current_value += char

        if pyxel.btnp(pyxel.KEY_BACKSPACE, 10, 3) and current_value:
            current_value = current_value[:-1]

        self._set_field_value(self.edit_field_index, current_value)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.editing_field = False
            self.edit_field_index = -1
            self.status_message = "配置已更新"
            self.status_color = 11
            return

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.editing_field = False
            self.edit_field_index = -1

    def _continue_to_character_creation(self):
        api_key = self.api_key.strip()
        base_url = self.base_url.strip()
        model = self.model.strip()

        if self.llm_enabled and (not api_key or not base_url or not model):
            self.status_message = "开启LLM时，API Key/Base URL/Model均为必填"
            self.status_color = 8
            return

        self.scene_manager.llm_settings = {
            "enabled": self.llm_enabled,
            "api_key": api_key,
            "base_url": base_url,
            "model": model
        }

        if self.llm_enabled:
            self.llm_client.configure(api_key, base_url, model)
        else:
            self.llm_client.disable()

        from src.scenes.scene_manager import SceneType
        self.scene_manager.change_scene(SceneType.CHARACTER_CREATION)

    def _is_paste_shortcut(self):
        """是否触发了 Ctrl/Cmd + V"""
        if not pyxel.btnp(pyxel.KEY_V):
            return False

        return (
            pyxel.btn(pyxel.KEY_CTRL) or
            pyxel.btn(pyxel.KEY_LCTRL) or
            pyxel.btn(pyxel.KEY_RCTRL) or
            pyxel.btn(pyxel.KEY_GUI) or
            pyxel.btn(pyxel.KEY_LGUI) or
            pyxel.btn(pyxel.KEY_RGUI)
        )

    def _paste_from_clipboard(self, target_field_index):
        """
        粘贴逻辑：
        1) 优先使用 pyxel.input_text（桌面端常见）
        2) Web(Pyodide) 尝试 navigator.clipboard.readText()
        """
        pasted = pyxel.input_text
        if pasted:
            return self._apply_pasted_text(pasted, target_field_index)

        # Web 环境：尝试直接读浏览器剪贴板（异步）
        try:
            from js import navigator
        except Exception:
            return False

        try:
            promise = navigator.clipboard.readText()
        except Exception:
            return False

        def on_success(text):
            text = str(text) if text is not None else ""
            if self._apply_pasted_text(text, target_field_index):
                self.status_message = "已粘贴"
                self.status_color = 11
            else:
                self.status_message = "剪贴板为空或格式无效"
                self.status_color = 8

        def on_error(_err):
            self.status_message = "无法读取剪贴板，请手动输入"
            self.status_color = 8

        promise.then(on_success).catch(on_error)
        return True

    def _apply_pasted_text(self, text, target_field_index):
        """应用粘贴内容，支持直接值或 .env 片段"""
        text = (text or "").replace("\r\n", "\n").strip()
        if not text:
            return False

        # 允许一次粘贴 .env 片段自动填充三项
        parsed = {}
        for line in text.split("\n"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key in ["LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL"]:
                parsed[key] = value

        if parsed:
            if "LLM_API_KEY" in parsed:
                self.api_key = parsed["LLM_API_KEY"][:160]
            if "LLM_BASE_URL" in parsed:
                self.base_url = parsed["LLM_BASE_URL"][:160]
            if "LLM_MODEL" in parsed:
                self.model = parsed["LLM_MODEL"][:160]
            self.status_message = "已从粘贴内容自动填充配置"
            self.status_color = 11
            return True

        # 普通粘贴：追加到当前字段
        current = self._get_field_value(target_field_index)
        self._set_field_value(target_field_index, (current + text)[:160])
        return True

    def _get_field_value(self, field_index):
        if field_index == 1:
            return self.api_key
        if field_index == 2:
            return self.base_url
        if field_index == 3:
            return self.model
        return ""

    def _set_field_value(self, field_index, value):
        if field_index == 1:
            self.api_key = value
        elif field_index == 2:
            self.base_url = value
        elif field_index == 3:
            self.model = value

    def draw(self):
        pyxel.cls(1)

        title = "LLM 设置"
        draw_text((WINDOW_WIDTH - text_width(title)) // 2, 12, title, 7)

        panel_x = 16
        panel_y = 34
        panel_w = WINDOW_WIDTH - 32
        panel_h = 164

        pyxel.rect(panel_x, panel_y, panel_w, panel_h, 0)
        pyxel.rectb(panel_x, panel_y, panel_w, panel_h, 7)
        pyxel.rectb(panel_x + 2, panel_y + 2, panel_w - 4, panel_h - 4, 12)

        options = [
            ("开启LLM", "是" if self.llm_enabled else "否"),
            ("API Key", self.api_key),
            ("Base URL", self.base_url),
            ("Model", self.model),
            ("", "继续")
        ]

        for i, (label, value) in enumerate(options):
            row_y = panel_y + 14 + i * 28
            is_selected = i == self.selected_option
            field_locked = (i in [1, 2, 3]) and (not self.llm_enabled)

            if is_selected:
                pyxel.rect(panel_x + 5, row_y - 2, panel_w - 10, 18, 5)

            if i == 4:
                btn_x = panel_x + (panel_w - text_width(value)) // 2
                color = 10 if is_selected else 7
                draw_text(btn_x, row_y, value, color)
                continue

            label_color = 6 if field_locked else (10 if is_selected else 7)
            value_color = 13 if field_locked else (10 if is_selected else 7)

            draw_text(panel_x + 10, row_y, f"{label}:", label_color)

            display_value = value
            if i in [1, 2, 3]:
                max_width = panel_w - 98
                while text_width(display_value) > max_width and len(display_value) > 0:
                    display_value = "..." + display_value[4:]

            value_x = panel_x + 72
            draw_text(value_x, row_y, display_value if display_value else "-", value_color)

            if self.editing_field and self.edit_field_index == i and self.cursor_visible:
                cursor_x = value_x + text_width(display_value)
                pyxel.rect(cursor_x, row_y, 2, 12, 7)

        status_x = panel_x + 8
        status_y = panel_y + panel_h + 8
        draw_text(status_x, status_y, self.status_message, self.status_color)

        hint = "↑↓选择, Enter编辑/确认, Ctrl/Cmd+V粘贴, Esc返回"
        draw_text((WINDOW_WIDTH - text_width(hint)) // 2, WINDOW_HEIGHT - 14, hint, 13)
