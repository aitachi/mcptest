import asyncio
from typing import Dict, Any, List
from .llm_client import LLMClient
from .executor import TaskExecutor
from config import logger


class Agent:
    def __init__(self, mcp_server):
        self.mcp_server = mcp_server
        self.llm_client = LLMClient()
        self.executor = TaskExecutor(mcp_server, self.llm_client)
        logger.info("🤖 Agent初始化完成")

    async def process_query(self, query: str) -> Dict[str, Any]:
        logger.info(f"🎯 Agent接收到用户查询: {query}")
        print(f"🤖 Agent 收到查询: {query}")

        logger.info("📋 获取MCP服务器可用功能列表...")
        print("\n🔍 获取可用功能...")
        available_functions = self.mcp_server.get_available_functions()
        logger.info(f"📦 获取到 {len(available_functions)} 个可用功能")

        for func in available_functions:
            logger.info(f"  - {func['name']}: {func['description']}")

        logger.info("🧠 调用大模型进行任务分析...")
        print("\n🧠 大模型分析任务...")
        task_analysis = await self.llm_client.analyze_task(query, available_functions)

        if not task_analysis.get("steps"):
            error_msg = "大模型无法生成执行计划"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "message": error_msg,
                "query": query
            }

        steps = task_analysis["steps"]
        reasoning = task_analysis.get("reasoning", "")

        logger.info(f"📋 大模型生成执行计划成功")
        logger.info(f"📊 计划步骤数: {len(steps)}")
        logger.info(f"💭 分析理由: {reasoning}")

        print(f"📋 大模型生成执行计划，共 {len(steps)} 个步骤:")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step['function_name']} - {step['parameters']}")
            logger.info(f"  步骤{i}: {step['function_name']} - 参数: {step['parameters']}")
        print(f"💭 分析理由: {reasoning}")

        logger.info("⚡ 开始执行任务计划...")
        results = await self.executor.execute_with_llm_guidance(query, steps)

        summary = self._generate_summary(query, steps, results)
        logger.info(f"📊 生成执行总结: {summary}")

        return {
            "success": True,
            "query": query,
            "steps": steps,
            "reasoning": reasoning,
            "results": results,
            "summary": summary
        }

    def _generate_summary(self, query: str, steps: List[Dict], results: List[Dict]) -> Dict[str, Any]:
        successful_steps = [r for r in results if r["result"].get("success")]
        failed_steps = [r for r in results if not r["result"].get("success")]

        total_time = sum(r["execution_time"] for r in results)

        summary = {
            "total_planned_steps": len(steps),
            "total_executed_steps": len(results),
            "successful_steps": len(successful_steps),
            "failed_steps": len(failed_steps),
            "total_execution_time": total_time,
            "average_step_time": total_time / len(results) if results else 0,
            "success_rate": len(successful_steps) / len(results) if results else 0,
            "status": "completed" if not failed_steps else "partial_success"
        }

        logger.info(
            f"📈 执行统计: 计划{summary['total_planned_steps']}步, 执行{summary['total_executed_steps']}步, 成功{summary['successful_steps']}步, 失败{summary['failed_steps']}步")
        logger.info(
            f"⏱️  总耗时: {summary['total_execution_time']:.2f}秒, 平均每步: {summary['average_step_time']:.2f}秒")
        logger.info(f"📊 成功率: {summary['success_rate']:.1%}")

        return summary