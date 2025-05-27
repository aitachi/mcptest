import httpx
import json
import time
from typing import Dict, Any, List
from config import LLM_CONFIG, logger


class LLMClient:
    def __init__(self):
        self.base_url = LLM_CONFIG["base_url"]
        self.chat_endpoint = LLM_CONFIG["chat_endpoint"]
        self.model_name = LLM_CONFIG["model_name"]
        logger.info(f"🧠 初始化大模型客户端 - 模型: {self.model_name}")

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        url = f"{self.base_url}{self.chat_endpoint}"

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 1000
        }

        headers = {
            "Content-Type": "application/json"
        }

        logger.info(f"🌐 [LLM] 发送请求到大模型 - URL: {url}")
        logger.info(f"📝 [LLM] 请求消息数量: {len(messages)}")

        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()
                end_time = time.time()

                response_content = result["choices"][0]["message"]["content"]
                logger.info(f"✅ [LLM] 大模型响应成功 - 耗时: {end_time - start_time:.2f}秒")
                logger.info(f"📄 [LLM] 响应长度: {len(response_content)} 字符")

                return response_content
        except Exception as e:
            logger.error(f"❌ [LLM] 大模型调用失败: {str(e)}")
            return self._get_mock_response(messages)

    def _get_mock_response(self, messages: List[Dict[str, str]]) -> str:
        logger.info("🔄 [LLM] 使用模拟响应")
        last_message = messages[-1]["content"]

        if "任务分析" in last_message or "执行计划" in last_message:
            # 根据查询内容智能生成不同的执行计划
            if "数据库" in last_message and "文件" in last_message:
                return '''
{
    "steps": [
        {
            "function_name": "validate_data",
            "parameters": {"data": "用户查询参数", "rules": {"min_length": 1}}
        },
        {
            "function_name": "database_query", 
            "parameters": {"sql": "SELECT * FROM users WHERE status='active' LIMIT 10"}
        },
        {
            "function_name": "process_data",
            "parameters": {"data": "数据库查询结果", "operation": "format"}
        },
        {
            "function_name": "write_file",
            "parameters": {"file_path": "output/user_data.txt", "content": "格式化后的用户数据"}}
        }
    ],
    "reasoning": "首先验证输入参数，然后查询数据库获取用户信息，对数据进行格式化处理，最后保存到文件中"
}
'''
            elif "HTTP" in last_message or "网络" in last_message:
                return '''
{
    "steps": [
        {
            "function_name": "validate_data",
            "parameters": {"data": "请求参数", "rules": {"required": true}}
        },
        {
            "function_name": "http_request", 
            "parameters": {"url": "https://api.example.com/data", "method": "GET"}
        },
        {
            "function_name": "process_data",
            "parameters": {"data": "API响应数据", "operation": "transform"}
        },
        {
            "function_name": "database_insert",
            "parameters": {"table": "api_data", "data": {"content": "处理后的数据", "source": "external_api"}}}
        }
    ],
    "reasoning": "验证请求参数，发送HTTP请求获取外部数据，处理API响应，将结果插入数据库"
}
'''
            else:
                return '''
{
    "steps": [
        {
            "function_name": "validate_data",
            "parameters": {"data": "输入数据", "rules": {"min_length": 1}}
        },
        {
            "function_name": "process_data",
            "parameters": {"data": "验证后的数据", "operation": "normalize"}
        },
        {
            "function_name": "analyze_data",
            "parameters": {"data": "处理后的数据"}
        },
        {
            "function_name": "write_file",
            "parameters": {"file_path": "output/analysis_result.txt", "content": "分析结果报告"}}
        }
    ],
    "reasoning": "验证输入数据，进行数据处理和标准化，分析数据生成统计信息，将分析结果保存到文件"
}
'''
        else:
            # 决策下一步的智能响应
            if "失败" in last_message:
                return '''
{
    "action": "modify",
    "next_step": {
        "function_name": "process_data",
        "parameters": {"data": "使用模拟数据", "operation": "format"}
    },
    "reason": "上一步执行失败，修改参数使用模拟数据继续执行"
}
'''
            else:
                return '''
{
    "action": "continue",
    "next_step": {
        "function_name": "process_data",
        "parameters": {"data": "上一步的成功结果", "operation": "format"}
    },
    "reason": "上一步执行成功，继续按计划执行下一步"
}
'''

    async def analyze_task(self, query: str, available_functions: List[Dict]) -> Dict[str, Any]:
        logger.info(f"🔍 [LLM] 开始任务分析 - 查询: {query}")

        functions_info = "\n".join([
            f"- {func['name']}: {func['description']} (优先级: {func['priority']}, 类别: {func['category']})"
            for func in available_functions
        ])

        prompt = f"""
你是一个智能任务分析助手。根据用户查询，从可用功能中选择合适的功能，并生成执行计划。

可用功能:
{functions_info}

用户查询: {query}

请分析用户查询，选择合适的功能，并按逻辑顺序排列。返回JSON格式的执行计划，包含以下字段：
- steps: 步骤列表，每个步骤包含function_name和parameters
- reasoning: 选择这些功能的理由

注意：
1. 优先选择优先级低的功能（数字越小优先级越高）
2. 按照逻辑顺序排列功能：验证->查询/读取->处理->分析->写入/发送
3. 根据查询内容智能匹配参数

示例返回格式:
{{
    "steps": [
        {{
            "function_name": "validate_data",
            "parameters": {{"data": "用户输入数据", "rules": {{"min_length": 1}}}}
        }},
        {{
            "function_name": "database_query",
            "parameters": {{"sql": "SELECT * FROM users WHERE status='active' LIMIT 10"}}
        }},
        {{
            "function_name": "process_data", 
            "parameters": {{"data": "查询结果", "operation": "format"}}
        }},
        {{
            "function_name": "write_file",
            "parameters": {{"file_path": "output/processed_data.txt", "content": "处理后的数据"}}
        }}
    ],
    "reasoning": "根据用户查询，首先验证输入数据，然后查询数据库获取用户信息，对数据进行格式化处理，最后保存到文件"
}}
"""

        messages = [{"role": "user", "content": prompt}]
        logger.info(f"🧠 [LLM] 发送任务分析请求")
        response = await self.chat_completion(messages)

        try:
            result = json.loads(response)
            logger.info(f"✅ [LLM] 任务分析成功 - 生成 {len(result.get('steps', []))} 个步骤")
            logger.info(f"💭 [LLM] 分析理由: {result.get('reasoning', '')}")
            return result
        except Exception as e:
            logger.error(f"❌ [LLM] 任务分析结果解析失败: {str(e)}")
            logger.error(f"📄 [LLM] 原始响应: {response}")
            return {"steps": [], "reasoning": "解析失败"}

    async def decide_next_step(self, query: str, execution_history: List[Dict], remaining_steps: List[Dict]) -> Dict[
        str, Any]:
        logger.info(f"🤔 [LLM] 开始决策下一步 - 已执行 {len(execution_history)} 步，剩余 {len(remaining_steps)} 步")

        history_text = "\n".join([
            f"步骤{i + 1}: {step['function_name']} - {'成功' if step['result']['success'] else '失败'} - 结果: {step['result'].get('result', step['result'].get('error', ''))}"
            for i, step in enumerate(execution_history)
        ])

        remaining_text = "\n".join([
            f"- {step['function_name']}: {step['parameters']}"
            for step in remaining_steps
        ])

        prompt = f"""
根据执行历史和剩余步骤，决定下一步操作。

原始查询: {query}

已执行步骤:
{history_text}

剩余步骤:
{remaining_text}

请根据执行情况决定下一步动作，返回JSON格式的决定，包含以下字段：
- action: "continue"(继续执行), "modify"(修改下一步), "stop"(停止执行)
- next_step: 如果action是continue或modify，提供下一步的function_name和parameters
- reason: 决定的理由

判断规则：
1. 如果上一步失败且是关键步骤，考虑停止或修改
2. 如果上一步成功，通常继续执行
3. 可以根据上一步的结果调整下一步的参数

示例返回格式:
{{
    "action": "continue",
    "next_step": {{
        "function_name": "process_data",
        "parameters": {{"data": "从上一步获取的具体数据", "operation": "format"}}
    }},
    "reason": "上一步数据查询成功，继续执行数据处理，并使用实际查询结果作为输入"
}}
"""

        messages = [{"role": "user", "content": prompt}]
        logger.info(f"🧠 [LLM] 发送决策请求")
        response = await self.chat_completion(messages)

        try:
            result = json.loads(response)
            action = result.get("action", "continue")
            reason = result.get("reason", "")
            logger.info(f"✅ [LLM] 决策完成 - 动作: {action}")
            logger.info(f"💭 [LLM] 决策理由: {reason}")
            return result
        except Exception as e:
            logger.error(f"❌ [LLM] 决策结果解析失败: {str(e)}")
            logger.error(f"📄 [LLM] 原始响应: {response}")
            return {"action": "continue", "reason": "解析失败，默认继续执行"}