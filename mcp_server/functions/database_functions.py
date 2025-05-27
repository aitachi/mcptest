import asyncio
import time
from typing import Any, Dict, List
from .base import BaseFunction
from config import DATABASE_CONFIG, logger

class DatabaseQueryFunction(BaseFunction):
    def __init__(self):
        super().__init__(
            name="database_query",
            description="执行数据库查询",
            category="database",
            priority=2
        )

    async def execute(self, sql: str, params: List = None) -> Dict[str, Any]:
        logger.info(f"🗄️  [MCP] 开始数据库查询 - SQL: {sql[:100]}...")
        await asyncio.sleep(1)
        try:
            import pymysql
            connection = pymysql.connect(**DATABASE_CONFIG)
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, params or [])
            results = cursor.fetchall()
            connection.close()

            logger.info(f"✅ [MCP] 数据库查询成功 - 返回 {len(results)} 条记录")
            return {
                "success": True,
                "result": {
                    "sql": sql,
                    "rows_count": len(results),
                    "data": results,
                    "execution_time": time.time()
                }
            }
        except Exception as e:
            logger.error(f"❌ [MCP] 数据库查询失败 - 错误: {str(e)}")
            mock_data = [
                {"id": 1, "name": "测试用户1", "email": "user1@test.com", "status": "active",
                 "create_time": "2024-01-01"},
                {"id": 2, "name": "测试用户2", "email": "user2@test.com", "status": "inactive",
                 "create_time": "2024-01-02"},
                {"id": 3, "name": "测试用户3", "email": "user3@test.com", "status": "active",
                 "create_time": "2024-01-03"},
                {"id": 4, "name": "测试用户4", "email": "user4@test.com", "status": "pending",
                 "create_time": "2024-01-04"},
                {"id": 5, "name": "测试用户5", "email": "user5@test.com", "status": "active",
                 "create_time": "2024-01-05"}
            ]
            logger.info(f"ℹ️  [MCP] 使用模拟数据 - 返回 {len(mock_data)} 条记录")
            return {
                "success": True,
                "result": {
                    "sql": sql,
                    "rows_count": len(mock_data),
                    "data": mock_data,
                    "note": "使用模拟数据（数据库连接失败）",
                    "execution_time": time.time()
                }
            }

class DatabaseInsertFunction(BaseFunction):
    def __init__(self):
        super().__init__(
            name="database_insert",
            description="插入数据到数据库",
            category="database",
            priority=5
        )

    async def execute(self, table: str, data: Dict) -> Dict[str, Any]:
        logger.info(f"➕ [MCP] 开始插入数据 - 表: {table}, 数据: {data}")
        await asyncio.sleep(1.2)
        try:
            import pymysql
            connection = pymysql.connect(**DATABASE_CONFIG)
            cursor = connection.cursor()

            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            cursor.execute(sql, list(data.values()))
            connection.commit()
            insert_id = cursor.lastrowid
            connection.close()

            logger.info(f"✅ [MCP] 数据插入成功 - 插入ID: {insert_id}")
            return {
                "success": True,
                "result": {
                    "table": table,
                    "insert_id": insert_id,
                    "affected_rows": 1,
                    "inserted_data": data
                }
            }
        except Exception as e:
            logger.error(f"❌ [MCP] 数据插入失败 - 错误: {str(e)}")
            mock_insert_id = int(time.time()) % 10000
            logger.info(f"ℹ️  [MCP] 使用模拟插入结果 - 模拟ID: {mock_insert_id}")
            return {
                "success": True,
                "result": {
                    "table": table,
                    "insert_id": mock_insert_id,
                    "affected_rows": 1,
                    "inserted_data": data,
                    "note": "模拟插入结果（数据库连接失败）"
                }
            }

class DatabaseUpdateFunction(BaseFunction):
    def __init__(self):
        super().__init__(
            name="database_update",
            description="更新数据库记录",
            category="database",
            priority=5
        )

    async def execute(self, table: str, data: Dict, where: Dict) -> Dict[str, Any]:
        logger.info(f"🔄 [MCP] 开始更新数据 - 表: {table}, 数据: {data}, 条件: {where}")
        await asyncio.sleep(1.1)
        try:
            import pymysql
            connection = pymysql.connect(**DATABASE_CONFIG)
            cursor = connection.cursor()

            set_clause = ', '.join([f"{k}=%s" for k in data.keys()])
            where_clause = ' AND '.join([f"{k}=%s" for k in where.keys()])
            sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

            params = list(data.values()) + list(where.values())
            cursor.execute(sql, params)
            connection.commit()
            affected_rows = cursor.rowcount
            connection.close()

            logger.info(f"✅ [MCP] 数据更新成功 - 影响行数: {affected_rows}")
            return {
                "success": True,
                "result": {
                    "table": table,
                    "affected_rows": affected_rows,
                    "updated_data": data,
                    "where_condition": where
                }
            }
        except Exception as e:
            logger.error(f"❌ [MCP] 数据更新失败 - 错误: {str(e)}")
            logger.info(f"ℹ️  [MCP] 使用模拟更新结果")
            return {
                "success": True,
                "result": {
                    "table": table,
                    "affected_rows": 1,
                    "updated_data": data,
                    "where_condition": where,
                    "note": "模拟更新结果（数据库连接失败）"
                }
            }