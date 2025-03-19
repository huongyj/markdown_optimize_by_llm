import re
import preprocess_md
import split_document
import optimize_chunk_with_context
from requirement import *


# --- 主流程（整合所有步骤）---
def optimize_ocr_document(
    input_path: str ,
    output_path: str ,
    model_name: str,
    embedding_name: str,
    max_tokens: int,
):
    logging.info(f"开始优化OCR文档：{input_path}")
    # 读取OCR文件
    with open(input_path, "r", encoding="utf-8") as f:
        ocr_content = f.read()

    # 预处理OCR错误
    processed_content = preprocess_md.preprocess_md(ocr_content)
    
    # # 分块处理（语义+Token分割）
    # chunks = split_document.split_document(
    #     text=processed_content,
    #     max_tokens=max_tokens,
    #     embedding_model=embedding_name,
    # )
    
    # # 逐块优化（带上下文传递）
    # optimized_chunks = optimize_chunk_with_context.optimize_chunk_with_context(
    #     chunks=chunks,
    #     model_name=model_name
    # )
    
    # 合并结果并保存覆盖原本文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(processed_content)

    logging.info(f"OCR文档优化完成\n结果已保存至：{output_path}")

if __name__ == "__main__":
    optimize_ocr_document(
        input_path="GB_T 44080-2024_核电厂可靠性、可用性、可维修性和安全性管理规范.md",
        output_path="three.md",
        model_name="qwen2.5:14b",
        embedding_name="F:\\fucking models\\Qwen2.5-7B",
        max_tokens=4096,
    )