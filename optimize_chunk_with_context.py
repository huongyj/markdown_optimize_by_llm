from requirement import *
from typing import List
import requests

# --- 逐块优化核心逻辑（新增上下文管理）---
def optimize_chunk_with_context(
    chunks: List[str],
    model_name: str,
) -> List[str]:
    """逐块优化并传递上下文"""
    logging.info("开始逐块优化文档")
    optimized_chunks = []

    for i in range(len(chunks)):
        # 获取当前块及前后overlap块（避免跨块结构断裂）
        logging.info(f"正在优化第{i+1}/{len(chunks)}个块")
        # context_chunks = chunks[start:i+1]        # 保留上下文
        current_chunk = chunks[i]

        if i == 0:
            # 构造包含上下文的提示词
            prompt = f"""
# 严格指令
对提供的Markdown文档第{i+1}/{len(chunks)}个部分严格按照以下要求，并执行修复。

<修复规则>
1. 修复OCR引起的拼写错误
    - 使用换行符分隔正确的单词。
    - 利用上下文来纠正错误。
    - 仅修复明显的错误，避免不必要的更改。
    - 不要添加额外的句号或任何不必要的标点符号。
    - 在适当的地方添加换行符，以保持段落的完整性。

2. 检查和修复公式格式
    - 确保所有数学公式使用正确的LaTeX格式。
    - 检查并修复公式中的OCR错误，如错误的符号或变量。
    - 保留公式的原始结构和内容，仅进行必要的修正。

3. 检查和修复表格格式
    - 所有的表格格式均为HTML格式。
    - 确保表格使用标准的HTML标签格式。
    - 检查并修复表格中的HTML标签错误，如缺失的闭合标签、错误的属性等。
    - 保留表格的原始结构和内容，仅进行必要的格式修正。
    - 检查并修复表格中的数据错误或不一致。
    - 保留表格的原始信息，仅进行必要的修正。

4. 保持原有结构和内容
    - 遇到简短标题，请直接输出，不需要解释。
    - 保留所有原始标题。
    - 若非标题，则保留原始文本中的所有重要信息作为正文输出。
    - 不要添加原始文本中没有的任何新信息。
    - 保持段落分隔。
    - 保留原始文本中完整的列表、表格和图片链接。

!!!无论片段内容是否简略，禁止回复任何说明、元数据和标识！请直接返回内容！
!!!禁止自言自语，禁止回答问题，禁止添加任何额外信息！
</修复规则>

<处理流程>
原始文本 → 检查OCR错误 → 最小化修复 → 输出文本
</处理流程>

# 待处理文本
{current_chunk}
    """
            
            # 调用Ollama优化
            try:
                response = requests.post(
                    "http://127.0.0.1:11434/api/generate",
                    json={
                        "model": model_name,
                        "prompt": prompt,
                        "temperature": 0.1,
                        "stream": False
                    }
                )
            except requests.exceptions.Timeout:
                logging.error("请求超时，请稍后重试")
            except requests.exceptions.HTTPError as e:
                logging.error(f"服务器返回错误状态码: {e.response.status_code}")

            optimized = response.json()["response"]
            optimized_chunks.append(optimized)            
            # print("\n-------------------------------上下文片段（供参考格式）：\n",optimized_chunks)
        else:
                        # 构造包含上下文的提示词
            prompt = f"""
# 严格指令
对提供的Markdown文档第{i+1}/{len(chunks)}个部分严格按照以下要求，并执行修复。

<修复规则>
1. 修复OCR引起的拼写错误
    - 使用换行符分隔正确的单词。
    - 利用上下文来纠正错误。
    - 仅修复明显的错误，避免不必要的更改。
    - 不要添加额外的句号或任何不必要的标点符号。
    - 在适当的地方添加换行符，以保持段落的完整性。

2. 检查和修复公式格式
    - 确保所有数学公式使用正确的LaTeX格式。
    - 检查并修复公式中的OCR错误，如错误的符号或变量。
    - 保留公式的原始结构和内容，仅进行必要的修正。

3. 检查和修复表格格式
    - 所有的表格格式均为HTML格式。
    - 确保表格使用标准的HTML标签格式。
    - 检查并修复表格中的HTML标签错误，如缺失的闭合标签、错误的属性等。
    - 保留表格的原始结构和内容，仅进行必要的格式修正。
    - 检查并修复表格中的数据错误或不一致。
    - 保留表格的原始信息，仅进行必要的修正。

4. 保持原有结构和内容
    - 遇到简短标题，请直接输出，不需要解释。
    - 保留所有原始标题。
    - 若非标题，则保留原始文本中的所有重要信息作为正文输出。
    - 不要添加原始文本中没有的任何新信息。
    - 保持段落分隔。
    - 保留原始文本中完整的列表、表格和图片链接。

!!!无论片段内容是否简略，禁止回复任何说明、元数据和标识！请直接返回内容！
!!!禁止自言自语，禁止回答问题，禁止添加任何额外信息！
</修复规则>

<处理流程>
原始文本 → 扫描OCR错误 → 最小化修复 → 输出文本
</处理流程>

<违规惩罚>
若添加任何说明，将删除整段输出
</违规惩罚>

# 待处理文本
{current_chunk}
    """
            
            # 调用Ollama优化
            try:
                response = requests.post(
                    "http://127.0.0.1:11434/api/generate",
                    json={
                        "model": model_name,
                        "prompt": prompt,
                        "temperature": 0.1,
                        "stream": False
                    }
                )
            except requests.exceptions.Timeout:
                logging.error("请求超时，请稍后重试")
            except requests.exceptions.HTTPError as e:
                logging.error(f"服务器返回错误状态码: {e.response.status_code}")
            optimized = response.json()["response"]
            optimized_chunks.append(optimized)
            # print(f"\n----------------优化结果为：\n{optimized}\n")
            # print("\n需要优化的当前片段：",current_chunk)

    logging.info("逐块优化完成")

    return optimized_chunks