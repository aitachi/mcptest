import asyncio
import time
from typing import List, Dict, Any
from config import logger


class TaskExecutor:
    def __init__(self, mcp_server, llm_client):
        self.mcp_server = mcp_server
        self.llm_client = llm_client
        logger.info("⚡ 初始化任务执行器")

    async def execute_with_llm_guidance(self, query: str, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        remaining_steps = steps.copy()

        logger.info(f"🚀 开始执行任务计划")
        logger.info(f"📋 计划步骤数: {len(steps)}")
        logger.info(f"🎯 原始查询: {query}")
        print(f"\n{'=' * 80}")
        print(f"🚀 开始执行任务计划，共 {len(steps)} 个步骤")
        print(f"🎯 用户查询: {query}")
        print(f"{'=' * 80}")

        step_counter = 1
        while remaining_steps:
            current_step = remaining_steps[0]

            logger.info(f"📍 执行步骤 {step_counter}: {current_step['function_name']}")
            print(f"\n📋 步骤 {step_counter}: 执行 {current_step['function_name']}")
            print(f"🔧 MCP功能调用: {current_step['function_name']}")
            print(f"📝 调用参数: {current_step['parameters']}")

            start_time = time.time()
            logger.info(f"⚡ [执行器] 调用MCP服务器执行功能: {current_step['function_name']}")
            result = await self.mcp_server.execute_function(
                current_step['function_name'],
                **current_step['parameters']
            )
            end_time = time.time()

            step_result = {
                "step": step_counter,
                "function_name": current_step['function_name'],
                "parameters": current_step['parameters'],
                "result": result,
                "execution_time": end_time - start_time,
                "timestamp": time.time()
            }
            results.append(step_result)
            remaining_steps.pop(0)

            if result.get("success"):
                logger.info(f"✅ 步骤 {step_counter} 执行成功 - 耗时: {step_result['execution_time']:.2f}秒")
                print(f"✅ 步骤 {step_counter} 执行成功")
                print(f"⏱️  执行时间: {step_result['execution_time']:.2f}秒")
                if "result" in result and result["result"]:
                    print(f"📊 执行结果: {result['result']}")
                    logger.info(f"📊 执行结果详情: {result['result']}")
            else:
                error_msg = result.get('error', 'Unknown error')
                logger.error(f"❌ 步骤 {step_counter} 执行失败: {error_msg}")
                print(f"❌ 步骤 {step_counter} 执行失败: {error_msg}")

            if remaining_steps:
                logger.info(f"🤖 询问大模型关于下一步的决策...")
                print(f"\n🤖 正在咨询大模型决定下一步操作...")

                decision = await self.llm_client.decide_next_step(query, results, remaining_steps)

                action = decision.get("action", "continue")
                reason = decision.get("reason", "No reason provided")

                logger.info(f"🧠 大模型决策: {action} - 理由: {reason}")
                print(f"🧠 大模型决策: {action}")
                print(f"💭 决策理由: {reason}")

                if action == "stop":
                    logger.info("🛑 大模型决定停止执行")
                    print("🛑 大模型决定停止执行")
                    break
                elif action == "modify" and decision.get("next_step"):
                    logger.info("🔄 大模型修改了下一步执行计划")
                    print("🔄 大模型修改了下一步执行计划")
                    old_step = remaining_steps[0]
                    new_step = decision["next_step"]
                    remaining_steps[0] = new_step
                    logger.info(f"📝 原计划: {old_step}")
                    logger.info(f"📝 新计划: {new_step}")
                    print(f"📝 修改前: {old_step['function_name']}")
                    print(f"📝 修改后: {new_step['function_name']}")
                elif action == "continue":
                    logger.info("➡️  大模型决定继续执行原计划")
                    print("➡️  大模型决定继续执行原计划")

                logger.info("⏳ 等待5秒后执行下一步...")
                print(f"\n⏳ 等待 5 秒后执行下一步...")

                for i in range(5, 0, -1):
                    print(f"⏰ {i}秒...", end="\r")
                    await asyncio.sleep(1)
                print(" " * 20, end="\r")

            step_counter += 1

        logger.info(f"🎉 任务计划执行完成！共执行 {len(results)} 个步骤")
        print(f"\n🎉 任务计划执行完成！")
        return results