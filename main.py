import asyncio
from mcp_server.server import MCPServer
from agent.core import Agent
from config import logger


async def main():
    logger.info("🌟 系统启动开始")
    print("🌟 Agent-MCP系统启动中...")

    logger.info("🚀 初始化MCP服务器...")
    mcp_server = MCPServer()
    await mcp_server.start()

    logger.info("🤖 初始化Agent...")
    agent = Agent(mcp_server)

    print("\n🔧 可用功能列表:")
    functions = mcp_server.get_available_functions()
    for func in functions:
        print(f"  - {func['name']}: {func['description']} (优先级: {func['priority']}, 类别: {func['category']})")
        logger.info(f"📦 可用功能: {func['name']} - {func['description']}")

    test_queries = [
        "从数据库查询用户信息，验证数据格式，处理后保存到文件，并发送邮件通知",
        "读取配置文件内容，验证配置项的完整性，然后更新数据库中的系统设置",
        "查询数据库中的订单数据，进行数据分析生成统计报告，保存结果并发送邮件",
        "验证用户输入数据，发送HTTP请求获取外部数据，处理合并后插入数据库"
    ]

    for i, query in enumerate(test_queries, 1):
        logger.info(f"🔍 开始测试查询 {i}: {query}")
        print(f"\n{'=' * 80}")
        print(f"🔍 测试查询 {i}: {query}")
        print(f"{'=' * 80}")

        try:
            result = await agent.process_query(query)

            if result["success"]:
                logger.info(f"✅ 查询 {i} 处理成功")
                print(f"\n📊 执行总结:")
                summary = result["summary"]
                print(f"  ✅ 计划步骤: {summary['total_planned_steps']}")
                print(f"  ✅ 执行步骤: {summary['total_executed_steps']}")
                print(f"  ✅ 成功步骤: {summary['successful_steps']}")
                print(f"  ❌ 失败步骤: {summary['failed_steps']}")
                print(f"  ⏱️  总耗时: {summary['total_execution_time']:.2f}秒")
                print(f"  ⏱️  平均耗时: {summary['average_step_time']:.2f}秒")
                print(f"  📈 成功率: {summary['success_rate']:.1%}")
                print(f"  📊 状态: {summary['status']}")

                logger.info(f"📊 查询 {i} 总结: {summary}")
            else:
                logger.error(f"❌ 查询 {i} 处理失败: {result['message']}")
                print(f"❌ 查询处理失败: {result['message']}")

        except Exception as e:
            logger.error(f"❌ 查询 {i} 执行异常: {str(e)}")
            print(f"❌ 查询执行异常: {str(e)}")

        if i < len(test_queries):
            logger.info("⏳ 等待3秒后执行下一个测试...")
            print(f"\n⏳ 等待 3 秒后执行下一个测试...")
            await asyncio.sleep(3)

    logger.info("🛑 系统关闭...")
    await mcp_server.stop()
    logger.info("✅ 系统已完全关闭")
    print("\n✅ 系统测试完成！")


if __name__ == "__main__":
    asyncio.run(main())