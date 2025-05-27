import asyncio
import json
import time
from typing import Any, Dict
from .base import BaseFunction
from config import logger


class HttpRequestFunction(BaseFunction):
    def __init__(self):
        super().__init__(
            name="http_request",
            description="发送HTTP请求",
            category="web",
            priority=3
        )

    async def execute(self, url: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
        logger.info(f"🌐 [MCP] 开始HTTP请求 - URL: {url}, 方法: {method}")
        await asyncio.sleep(2)

        mock_response = {
            "url": url,
            "method": method,
            "status_code": 200,
            "response_data": {
                "message": f"模拟响应来自 {url}",
                "timestamp": time.time(),
                "data": data or {},
                "headers": {"Content-Type": "application/json"}
            },
            "request_data": data
        }

        logger.info(f"✅ [MCP] HTTP请求完成 - 状态码: 200, 响应大小: {len(str(mock_response))} 字符")
        return {"success": True, "result": mock_response}


class EmailSendFunction(BaseFunction):
    def __init__(self):
        super().__init__(
            name="send_email",
            description="发送电子邮件",
            category="communication",
            priority=7
        )

    async def execute(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        logger.info(f"📧 [MCP] 开始发送邮件 - 收件人: {to}, 主题: {subject}")
        await asyncio.sleep(1.5)

        email_result = {
            "to": to,
            "subject": subject,
            "body_length": len(body),
            "sent_time": time.time(),
            "message_id": f"msg_{int(time.time())}",
            "status": "已发送"
        }

        logger.info(f"✅ [MCP] 邮件发送完成 - 消息ID: {email_result['message_id']}")
        return {"success": True, "result": email_result}