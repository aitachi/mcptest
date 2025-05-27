from typing import Dict, List, Any
from .functions.base import BaseFunction
from .functions.data_functions import DataProcessFunction, DataValidateFunction, DataAnalyzeFunction
from .functions.file_functions import FileReadFunction, FileWriteFunction
from .functions.web_functions import HttpRequestFunction, EmailSendFunction
from .functions.database_functions import DatabaseQueryFunction, DatabaseInsertFunction, DatabaseUpdateFunction
from config import logger


class FunctionRegistry:
    def __init__(self):
        self.functions: Dict[str, BaseFunction] = {}
        logger.info("🔧 初始化功能注册器")
        self._register_default_functions()
        logger.info(f"📦 功能注册完成，共注册 {len(self.functions)} 个功能")

    def _register_default_functions(self):
        functions = [
            DataProcessFunction(),
            DataValidateFunction(),
            DataAnalyzeFunction(),
            FileReadFunction(),
            FileWriteFunction(),
            HttpRequestFunction(),
            EmailSendFunction(),
            DatabaseQueryFunction(),
            DatabaseInsertFunction(),
            DatabaseUpdateFunction()
        ]

        for func in functions:
            self.register_function(func)

    def register_function(self, function: BaseFunction):
        self.functions[function.name] = function
        logger.info(f"✅ 注册功能: {function.name}")

    def get_function(self, name: str) -> BaseFunction:
        return self.functions.get(name)

    def get_all_functions(self) -> Dict[str, BaseFunction]:
        return self.functions

    def get_functions_info(self) -> List[Dict[str, Any]]:
        return [func.get_info() for func in self.functions.values()]