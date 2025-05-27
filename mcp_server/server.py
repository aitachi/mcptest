import asyncio
from typing import Any, Dict, List
from .registry import FunctionRegistry
from config import logger


class MCPServer:
    def __init__(self):
        logger.info("🚀 初始化MCP服务器")
        self.registry = FunctionRegistry()
        self.is_running = False

    async def start(self):
        self.is_running = True
        logger.info("✅ MCP服务器启动成功")

    async def stop(self):
        self.is_running = False
        logger.info("🛑 MCP服务器已停止")

    async def execute_function(self, function_name: str, **kwargs) -> Dict[str, Any]:
        logger.info(f"🎯 [MCP] 接收到功能调用请求 - 功能: {function_name}")
        logger.info(f"📝 [MCP] 调用参数: {kwargs}")

        function = self.registry.get_function(function_name)
        if not function:
            error_msg = f"功能 {function_name} 未找到"
            logger.error(f"❌ [MCP] {error_msg}")
            return {"success": False, "error": error_msg}

        try:
            logger.info(f"⚡ [MCP] 开始执行功能: {function_name}")
            result = await function.execute(**kwargs)
            logger.info(f"✅ [MCP] 功能执行完成: {function_name}")
            return result
        except Exception as e:
            error_msg = f"功能执行异常: {str(e)}"
            logger.error(f"❌ [MCP] {error_msg}")
            return {"success": False, "error": error_msg}

    def get_available_functions(self) -> List[Dict[str, Any]]:
        functions = self.registry.get_functions_info()
        logger.info(f"📋 [MCP] 返回可用功能列表，共 {len(functions)} 个功能")
        return functions