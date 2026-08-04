from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

class LLMService:
# 定义了一个类

    def __init__(self)->None:
        # 创建 `LLMService` 对象时会自动运行。
        
        self.api_key = LLM_API_KEY
        self.base_url = LLM_BASE_URL
        self.model = LLM_MODEL

    def is_configured(self)-> bool:
        """判断大模型配置是否完整。"""
        return bool(
            self.api_key
            and self.base_url
            and self.model
        )