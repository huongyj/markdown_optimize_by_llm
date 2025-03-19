from transformers import AutoTokenizer
from typing import List
import split_into_semantic_blocks
# 3333token分割


def split_long_sentence(sentence: str, max_tokens: int,embedding_model: str) -> List[str]:       # Token分割
    """按Token限制分割（保留代码结构）"""
    words = sentence.split()
    chunks = []             # 存储最终的分割结果
    current_chunk = []      # 存储当前正在处理的块
    current_chunk_tokens = 0    # 记录当前块的Token数
    # tokenizer = AutoTokenizer.from_pretrained("D:\\fucking_models\\embedding_model\\bge-m3")# 嵌入模型
    tokenizer = AutoTokenizer.from_pretrained(embedding_model)# 嵌入模型
    
    for word in words:
        word_tokens = len(tokenizer.encode(word, add_special_tokens=False))
        if current_chunk_tokens + word_tokens > max_tokens:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_chunk_tokens = word_tokens
        else:
            current_chunk.append(word)
            current_chunk_tokens += word_tokens
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


if __name__ == "__main__":
    final_chunks = []

    with open("one.md", "r", encoding="utf-8") as f:
        content = f.read()

    blocks = split_into_semantic_blocks.split_into_semantic_blocks(content)

    for block in blocks:
        chunks = split_long_sentence(block, max_tokens=512)
        final_chunks.extend(chunks)
    print(f"文档分块处理完成, 一共被分成{len(final_chunks)}个块")
    print(f"final_chunks:{final_chunks}")
