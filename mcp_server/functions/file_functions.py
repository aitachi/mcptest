import asyncio
import os
import json
from typing import Any, Dict
from .base import BaseFunction
from config import logger


class FileReadFunction(BaseFunction):
    def __init__(self):
        super().__init__(
            name="read_file",
            description="读取文件内容",
            category="file",
            priority=2
        )

    async def execute(self, file_path: str) -> Dict[str, Any]:
        logger.info(f"📖 [MCP] 开始读取文件 - 路径: {file_path}")
        await asyncio.sleep(0.8)
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                logger.info(f"✅ [MCP] 文件读取成功 - 大小: {len(content)} 字符")
            else:
                content = f"模拟文件内容 - {file_path}\n这是一个测试文件内容\n包含多行数据用于演示"
                logger.info(f"ℹ️  [MCP] 文件不存在，使用模拟内容")

            return {
                "success": True,
                "result": {
                    "file_path": file_path,
                    "content": content,
                    "size": len(content),
                    "lines": len(content.split('\n'))
                }
            }
        except Exception as e:
            logger.error(f"❌ [MCP] 文件读取失败 - 错误: {str(e)}")
            return {"success": False, "error": str(e)}


class FileWriteFunction(BaseFunction):
    def __init__(self):
        super().__init__(
            name="write_file",
            description="写入文件内容",
            category="file",
            priority=6
        )

    async def execute(self, file_path: str, content: str) -> Dict[str, Any]:
        logger.info(f"✍️  [MCP] 开始写入文件 - 路径: {file_path}, 内容长度: {len(content)}")
        await asyncio.sleep(1.2)
        try:
            os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ [MCP] 文件写入成功 - 路径: {file_path}")
            return {
                "success": True,
                "result": {
                    "file_path": file_path,
                    "content_length": len(content),
                    "message": f"成功写入文件 {file_path}",
                    "lines_written": len(content.split('\n'))
                }
            }
        except Exception as e:
            logger.error(f"❌ [MCP] 文件写入失败 - 错误: {str(e)}")
            return {"success": False, "error": str(e)}