markdown

复制
# Agent-MCP 智能任务执行系统

一个基于大语言模型(LLM)和模型控制协议(MCP)的智能任务分析与自动执行系统。该系统能够理解用户的自然语言查询，自动分解为可执行的任务步骤，并通过MCP服务器调用相应的功能模块完成复杂的业务流程。

## 📋 目录

- [特性](#特性)
- [系统架构](#系统架构)
- [功能模块](#功能模块)
- [安装依赖](#安装依赖)
- [配置说明](#配置说明)
- [快速开始](#快速开始)
- [API文档](#api文档)
- [使用示例](#使用示例)
- [日志说明](#日志说明)
- [故障排除](#故障排除)
- [贡献指南](#贡献指南)

## ✨ 特性

- **智能任务分析**: 使用大语言模型分析自然语言查询，自动生成执行计划
- **模块化架构**: 基于MCP协议的可扩展功能模块系统
- **动态决策**: 执行过程中实时咨询LLM，根据执行结果动态调整策略
- **多功能支持**: 支持数据处理、文件操作、数据库操作、HTTP请求、邮件发送等
- **容错机制**: 完善的错误处理和模拟数据回退机制
- **详细日志**: 完整的执行过程记录和性能统计

## 🏗️ 系统架构

┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 用户查询 │───▶│ Agent 核心 │───▶│ LLM 客户端 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
│
▼
┌─────────────────┐
│ 任务执行器 │
└─────────────────┘
│
▼
┌─────────────────┐ ┌─────────────────┐
│ MCP 服务器 │───▶│ 功能注册器 │
└─────────────────┘ └─────────────────┘
│ │
▼ ▼
┌─────────────────────────────────────────┐
│ 功能模块 │
├─────────────┬───────────┬───────────────┤
│ 数据处理模块 │ 文件模块 │ 数据库模块 │
├─────────────┼───────────┼───────────────┤
│ 网络模块 │ 邮件模块 │ 验证模块 │
└─────────────┴───────────┴───────────────┘

markdown

复制

## 🧩 功能模块

### 数据处理模块 (Priority: 1-4)
- **validate_data**: 验证数据格式和完整性 (优先级: 1)
- **process_data**: 处理和转换数据格式 (优先级: 3)
- **analyze_data**: 分析数据并生成统计信息 (优先级: 4)

### 文件操作模块 (Priority: 2-6)
- **read_file**: 读取文件内容 (优先级: 2)
- **write_file**: 写入文件内容 (优先级: 6)

### 数据库模块 (Priority: 2-5)
- **database_query**: 执行数据库查询 (优先级: 2)
- **database_insert**: 插入数据到数据库 (优先级: 5)
- **database_update**: 更新数据库记录 (优先级: 5)

### 网络通信模块 (Priority: 3-7)
- **http_request**: 发送HTTP请求 (优先级: 3)
- **send_email**: 发送电子邮件 (优先级: 7)

### 优先级说明
- **优先级 1**: 验证类功能 - 确保数据有效性
- **优先级 2-3**: 读取/请求类功能 - 获取数据
- **优先级 4**: 分析类功能 - 数据分析处理
- **优先级 5-6**: 写入类功能 - 数据持久化
- **优先级 7**: 通知类功能 - 外部通信

## 📦 安装依赖

### 系统要求
- Python 3.8+
- MySQL 5.7+ (可选，有模拟数据回退)
- 大语言模型服务(如Qwen)

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd agent-mcp-system
创建虚拟环境
bash

复制
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
安装依赖包
bash

复制
pip install -r requirements.txt
依赖包列表 (requirements.txt)

复制
httpx>=0.24.0
pymysql>=1.0.0
asyncio
typing-extensions>=4.0.0
⚙️ 配置说明
1. 数据库配置 (config.py)
python

运行

复制
DATABASE_CONFIG = {
    "host": "192.168.101.62",      # 数据库主机地址
    "user": "root",                # 数据库用户名
    "password": "123456",          # 数据库密码
    "database": "envom",           # 数据库名称
    "port": 3306                   # 数据库端口
}
2. 大语言模型配置
python

运行

复制
LLM_CONFIG = {
    "base_url": "http://192.168.101.214:6007",  # LLM服务地址
    "chat_endpoint": "/v1/chat/completions",    # 聊天API端点
    "model_name": "Qwen3-32B-AWQ"              # 模型名称
}
3. 日志配置
日志文件保存在 logs/ 目录
文件名格式: agent_YYYYMMDD_HHMMSS.log
同时输出到控制台和文件
🚀 快速开始
1. 基本运行
bash

复制
python main.py
2. 自定义查询
python

运行

复制
import asyncio
from mcp_server.server import MCPServer
from agent.core import Agent

async def custom_query():
    # 初始化系统
    mcp_server = MCPServer()
    await mcp_server.start()
    agent = Agent(mcp_server)
    
    # 执行自定义查询
    query = "查询数据库用户信息并生成报告"
    result = await agent.process_query(query)
    
    print("执行结果:", result)
    await mcp_server.stop()

# 运行
asyncio.run(custom_query())
📚 API文档
Agent核心类
Agent.process_query(query: str)
处理用户查询并返回执行结果。

参数:

query (str): 自然语言查询
返回值:

python

运行

复制
{
    "success": bool,           # 执行是否成功
    "query": str,             # 原始查询
    "steps": List[Dict],      # 执行步骤
    "reasoning": str,         # LLM分析理由
    "results": List[Dict],    # 执行结果
    "summary": {              # 执行统计
        "total_planned_steps": int,
        "total_executed_steps": int,
        "successful_steps": int,
        "failed_steps": int,
        "total_execution_time": float,
        "average_step_time": float,
        "success_rate": float,
        "status": str
    }
}
MCP服务器类
MCPServer.execute_function(function_name: str, **kwargs)
执行指定的功能函数。

参数:

function_name (str): 功能名称
**kwargs: 功能参数
返回值:

python

运行

复制
{
    "success": bool,    # 执行是否成功
    "result": Any,      # 执行结果
    "error": str        # 错误信息(如果失败)
}
MCPServer.get_available_functions()
获取所有可用功能列表。

返回值:

python

运行

复制
[
    {
        "name": str,         # 功能名称
        "description": str,  # 功能描述
        "category": str,     # 功能类别
        "priority": int      # 优先级
    }
]
💡 使用示例
示例1: 数据库操作 + 文件处理
python

运行

复制
query = "从数据库查询用户信息，验证数据格式，处理后保存到文件，并发送邮件通知"

# 系统会自动分解为以下步骤:
# 1. validate_data - 验证查询参数
# 2. database_query - 查询用户信息
# 3. process_data - 处理数据格式
# 4. write_file - 保存到文件
# 5. send_email - 发送邮件通知
示例2: HTTP请求 + 数据处理
python

运行

复制
query = "验证用户输入数据，发送HTTP请求获取外部数据，处理合并后插入数据库"

# 系统会自动分解为以下步骤:
# 1. validate_data - 验证输入数据
# 2. http_request - 获取外部数据
# 3. process_data - 合并处理数据
# 4. database_insert - 插入数据库
示例3: 配置文件处理
python

运行

复制
query = "读取配置文件内容，验证配置项的完整性，然后更新数据库中的系统设置"

# 系统会自动分解为以下步骤:
# 1. read_file - 读取配置文件
# 2. validate_data - 验证配置完整性
# 3. database_update - 更新系统设置
📊 日志说明
日志级别
INFO: 正常执行信息
ERROR: 错误信息
DEBUG: 调试信息(可选开启)
重要日志标识
🌟 - 系统启动
🚀 - 服务初始化
🤖 - Agent操作
🧠 - LLM交互
⚡ - 功能执行
✅ - 执行成功
❌ - 执行失败
📊 - 统计信息
日志文件示例
apache

复制
2025-05-26 21:35:50,659 - AgentMCP - INFO - 🌟 系统启动开始
2025-05-26 21:35:50,660 - AgentMCP - INFO - 🚀 初始化MCP服务器...
2025-05-26 21:35:50,662 - AgentMCP - INFO - 🤖 Agent初始化完成
2025-05-26 21:36:14,340 - AgentMCP - INFO - ✅ [LLM] 大模型响应成功 - 耗时: 23.67秒
🔧 故障排除
常见问题
1. 数据库连接失败
问题: pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")

解决方案:

检查数据库配置信息
确认数据库服务运行状态
系统自动使用模拟数据继续执行
2. LLM服务不可用
问题: httpx.ConnectError: Connection failed

解决方案:

检查LLM服务地址和端口
确认网络连接正常
系统自动使用模拟响应继续执行
3. 函数参数错误
问题: DataProcessFunction.execute() got an unexpected keyword argument

解决方案:

检查函数定义和调用参数匹配
LLM会自动修正参数结构重试
查看日志中的参数修正过程
4. JSON解析失败
问题: json.JSONDecodeError: Expecting ',' delimiter

解决方案:

LLM响应格式问题，系统会使用备用解析策略
检查LLM服务配置和模型版本
查看原始响应日志排查问题
调试模式
启用详细日志输出:

python

运行

复制
import logging
logging.getLogger('AgentMCP').setLevel(logging.DEBUG)
🤝 贡献指南
添加新功能模块
创建功能类
python

运行

复制
from .base import BaseFunction

class CustomFunction(BaseFunction):
    def __init__(self):
        super().__init__(
            name="custom_function",
            description="自定义功能描述",
            category="custom",
            priority=5
        )
    
    async def execute(self, **kwargs):
        # 实现功能逻辑
        return {"success": True, "result": "执行结果"}
注册功能
在 registry.py 中添加:
python

运行

复制
from .functions.custom_functions import CustomFunction

def _register_default_functions(self):
    functions = [
        # ... 现有功能
        CustomFunction(),
    ]
测试功能
python

运行

复制
# 添加测试用例
query = "使用自定义功能处理数据"
result = await agent.process_query(query)
代码贡献流程
Fork 项目
创建功能分支 (git checkout -b feature/AmazingFeature)
提交更改 (git commit -m 'Add some AmazingFeature')
推送到分支 (git push origin feature/AmazingFeature)
创建 Pull Request
代码规范
使用类型注解
添加详细的docstring
遵循PEP 8编码规范
包含适当的错误处理
添加相应的日志输出
📈 性能统计
系统会自动记录以下性能指标:

执行时间: 每个步骤和总体执行时间
成功率: 步骤执行成功率统计
LLM响应时间: 大模型调用耗时
功能执行时间: 各功能模块执行耗时
性能优化建议
并行执行: 对于无依赖关系的步骤可考虑并行执行
缓存机制: 缓存常用的LLM响应和数据库查询结果
超时设置: 为长时间执行的操作设置合理超时
资源池: 使用连接池管理数据库连接
📄 许可证
本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详细信息。

🙏 致谢
感谢 OpenAI 和 Anthropic 等公司推动大语言模型技术发展
感谢开源社区提供的优秀工具和库
感谢所有贡献者的努力和支持
如有问题或建议，请创建 Issue 或联系项目维护者。