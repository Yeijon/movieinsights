"""
* 配置记录日志，用于记录bug,,,
"""
import logging
from rich.logging import RichHandler

# 创建日志记录器
def init_console_logger():
    logging.basicConfig(level="DEBUG", format="%(message)s", datefmt="[%Y/%m/%X]", handlers=[RichHandler(rich_tracebacks=True)])
    log = logging.getLogger(__name__)
    return log

def init_logger():
    log = logging.getLogger(__name__)
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    handler = logging.FileHandler('record.log', encoding='utf-8')
    handler.setLevel(logging.NOTSET)
    handler.setFormatter(f_format)

    log.addHandler(handler)
    return log