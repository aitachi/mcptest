import logging
import os
from datetime import datetime

DATABASE_CONFIG = {
    "host": "192.168.101.62",
    "user": "root",
    "password": "123456",
    "database": "envom",
    "port": 3306
}

LLM_CONFIG = {
    "base_url": "http://192.168.101.214:6007",
    "chat_endpoint": "/v1/chat/completions",
    "model_name": "Qwen3-32B-AWQ"
}


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/agent_{timestamp}.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger('AgentMCP')


logger = setup_logging()