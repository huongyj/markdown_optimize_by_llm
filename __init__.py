import re
import logging

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
# 配置日志信息
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')