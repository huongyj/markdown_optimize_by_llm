from requirement import *
import split_long_sentence
import split_into_semantic_blocks
from typing import List

def split_document(text: str, max_tokens: int, embedding_model: str) -> List[str]:
    """分块主流程（语义分割 → Token分割）"""
    semantic_blocks = split_into_semantic_blocks.split_into_semantic_blocks(text)
    final_chunks = []
    
    for block in semantic_blocks:
        block_chunks = split_long_sentence.split_long_sentence(block, max_tokens, embedding_model)
        final_chunks.extend(block_chunks)

    logging.info("文档分块处理完成, 一共被分成%d个块", len(final_chunks))
    return final_chunks


if __name__ == "__main__":
    with open("one.md", "r", encoding="utf-8") as f:
        content = f.read()

    chunks = split_document(content, max_tokens=512)

    for i, chunk in enumerate(chunks):
        print(f"-------------------{i}/{len(chunks)}-------------------\n", chunk)
        with open("three.md", "a", encoding="utf-8") as f:
            f.write(chunk)