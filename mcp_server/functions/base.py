from abc import ABC, abstractmethod
from typing import Any, Dict, List
from config import logger


class BaseFunction(ABC):
    def __init__(self, name: str, description: str, category: str, priority: int = 5):
        self.name = name
        self.description = description
        self.category = category
        self.priority = priority
        logger.info(f"📦 注册功能: {name} - {description}")

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        pass

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "priority": self.priority
        }