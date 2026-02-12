# -*- coding: utf-8 -*-
"""
LLM 客户端模块
用于与大语言模型 API 通信
"""

import os
import threading
import queue
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class LLMClient:
    """大语言模型客户端"""
    
    def __init__(self):
        """初始化 LLM 客户端"""
        env_config = self.read_env_config()
        self.api_key = env_config['api_key']
        self.base_url = env_config['base_url']
        self.model = env_config['model']
        self.available = False
        self._init_client()
        
        # 用于异步通信的队列
        self.response_queue = queue.Queue()

    def read_env_config(self):
        """读取 .env 中的 LLM 配置"""
        return {
            'api_key': os.getenv('LLM_API_KEY', '').strip(),
            'base_url': os.getenv('LLM_BASE_URL', '').strip(),
            'model': os.getenv('LLM_MODEL', '').strip()
        }

    def configure(self, api_key, base_url, model):
        """在运行时更新 LLM 配置（不写入 .env）"""
        self.api_key = (api_key or '').strip()
        self.base_url = (base_url or '').strip()
        self.model = (model or '').strip()
        self._init_client()

    def disable(self):
        """强制禁用 LLM（保留已填配置）"""
        self.available = False
        print("[LLM] 已手动禁用")
        
    def _init_client(self):
        """初始化客户端"""
        self.available = False

        print(f"[LLM] 初始化客户端...")
        print(f"[LLM] API Key: {self.api_key[:10]}..." if self.api_key else "[LLM] API Key: 未设置")
        print(f"[LLM] Base URL: {self.base_url}")
        print(f"[LLM] Model: {self.model}")
        
        if not self.api_key or not self.base_url or not self.model:
            print("警告: LLM配置不完整，AI对话功能将不可用")
            return
            
        self.available = True
        print("[LLM] 客户端初始化成功")
            
    def is_available(self):
        """检查 LLM 是否可用"""
        return self.available
        
    def chat(self, messages, max_tokens=150):
        """
        发送对话请求 - 使用 urllib 直接发送 HTTP 请求
        """
        if not self.available:
            return "(AI not enabled)"
            
        try:
            import urllib.request
            import ssl
            
            print(f"[LLM] 正在发送请求到 {self.model}...")
            
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            # 创建 SSL 上下文
            ctx = ssl.create_default_context()
            
            with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result['choices'][0]['message']['content'].strip()
                print(f"[LLM] 请求成功，回复: {content}")
                return content
                
        except Exception as e:
            error_msg = str(e)
            print(f"[LLM] 请求失败: {error_msg}")
            return f"(Error: {error_msg[:40]})"
            
    def chat_async(self, messages, callback, max_tokens=150):
        """
        异步发送对话请求
        """
        def _request():
            print("[LLM] 异步线程开始执行...")
            try:
                result = self.chat(messages, max_tokens)
                print(f"[LLM] 异步线程完成")
                self.response_queue.put(result)
            except Exception as e:
                print(f"[LLM] 异步线程异常: {e}")
                self.response_queue.put(f"(Error: {str(e)[:40]})")
            
        thread = threading.Thread(target=_request)
        thread.daemon = True
        thread.start()
        print("[LLM] 异步线程已启动")
        
    def check_response(self):
        """检查是否有响应可用（非阻塞）"""
        try:
            return self.response_queue.get_nowait()
        except queue.Empty:
            return None


# 全局 LLM 客户端实例
_llm_client = None


def get_llm_client():
    """获取全局 LLM 客户端实例"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
