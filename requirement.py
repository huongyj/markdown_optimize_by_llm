import logging
import re
# 配置日志信息
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
USE_VERBOSE = False
DEFAULT_LOCAL_MODEL_NAME = "qwen2.5-7b-instruct-q8_0.gguf"
LOCAL_LLM_CONTEXT_SIZE_IN_TOKENS = 4096
HEADING_PATTERN = re.compile(
    r'^#\s*'  # 匹配原始错误的一级标题标记
    r'(\d+[\.\d]*\s+.+)'  # 捕获编号和标题内容（如 "1范围", "4.1产品结构"）
    r'|'  # 或
    r'([^\d\n]+)'  # 捕获无编号标题（如 "前言", "某某标准文件"）
    r'$', 
    re.MULTILINE
)

import logging
import colorlog


def get_logger(level=logging.INFO):
    # 创建logger对象
    logger = logging.getLogger()
    logger.setLevel(level)
    # 创建控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    # 定义颜色输出格式
    color_formatter = colorlog.ColoredFormatter(
        '%(log_color) - s%(asctime)s -|%(levelname)s|: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    # 将颜色输出格式添加到控制台日志处理器
    console_handler.setFormatter(color_formatter)
    # 移除默认的handler
    for handler in logger.handlers:
        logger.removeHandler(handler)
    # 将控制台日志处理器添加到logger对象
    logger.addHandler(console_handler)
    return logger

logging = get_logger()