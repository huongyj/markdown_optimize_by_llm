import re
from requirement import *  # Replace with actual function or class names
from typing import List
# 第二步
# 2222语义分块（重点修改）


def split_into_semantic_blocks(text: str) -> List[str]:
    blocks = []             # 存储最终的分块结果
    current_block = []      # 存储当前正在处理的块
    current_type = None     # 记录当前块的类型
    in_html_table = False   # 标记是否在 HTML 表格内

    html_table_start = re.compile(r'<\s*html\s*>', re.IGNORECASE)
    html_table_end = re.compile(r'</html>$', re.IGNORECASE)    # 匹配 HTML 表格的起始和结束标签

    for line in text.splitlines():
        stripped_line = line.strip()    # 去除首尾的空白字符
        line_type = None            # 初始化当前行的类型

        # 优先处理HTML表格
        if html_table_start.search(stripped_line) or  in_html_table:  # 匹配到 HTML 表格的起始标签
            in_html_table = True
            line_type = 'html_table'
            if html_table_end.search(stripped_line):  # 匹配到 HTML 表格的结束标签
                in_html_table = False
                line_type = 'html_table'
        # elif in_html_table:
        #     print("在html_table中")
        #     line_type = 'html_table'
        else:
            # 识别标题
            if re.match(r'^(#{1,4} )', stripped_line.lstrip()):
                line_type = 'heading'
            # 识别列表
            elif re.match(r'^([*+-]|\d+\.|\d+\)|[Aa]\.|\([Aa]\))\s', stripped_line):
                line_type = 'list'
            else:
                line_type = 'paragraph'

        # 块切换逻辑
        if line_type != current_type and current_block:
            blocks.append('\n'.join(current_block))
            current_block = []
        current_type = line_type
        current_block.append(line)  # 存储原始文本行

    if current_block:
        blocks.append('\n'.join(current_block))
    return blocks


if __name__ == "__main__":
    with open("one.md", "r", encoding="utf-8") as f:
        content = f.read()
    blocks = split_into_semantic_blocks(content)
    i = 1
    for block in blocks:
        print(f"\n---------------{i}/{len(blocks)}----------------\n", block)
        i += 1
        with open("two.md", "a", encoding="utf-8") as f:
            f.write(block)
    logging.info("预处理结果已保存至：two.md")