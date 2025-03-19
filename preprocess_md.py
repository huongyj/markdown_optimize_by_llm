from requirement import *

# 第一步
# --- 预处理函数 ---
def preprocess_md(content: str) -> str:
    content = re.sub(r'[ 　]+', ' ', content)  
    content = content.replace("．", ".").replace(". ", ".")
    content = content.replace("）", ")").replace("（", "(")     # 将全角转换为半角

    NON_NUMERIC_HEADING_PATTERN = re.compile(r'^\n#\s+([^\d].*)$',re.MULTILINE)        # 匹配无数字标题
    content = NON_NUMERIC_HEADING_PATTERN.sub(r'\1', content)                  # 删除其一级标题格式

    LOWER_HEADING_PATTERN = re.compile(r'^\n#\s+([\d]+\..*)$',re.MULTILINE)            # 匹配一级以上级标题
    content = LOWER_HEADING_PATTERN.sub(r'\1',content)                         # 删除其一级标题格式

    SECOND_HEADING_PATTERN = re.compile(r'^(\d+\.\d+[^\.\d].*)$',re.MULTILINE)          # 匹配二级标题
    content = SECOND_HEADING_PATTERN.sub(lambda m: f"## {m.group(1).strip()}", content) # 修改为二级标题格式
    
    THIRD_HEADING_PATTERN = re.compile(
    r'^(\d+\.\d+\.\d)'  # 匹配三级标题
    # r'(\d+[\.]+\d+[\.]+\d+)'  # 匹配三级编号
    r'([^\.\d].*)',  # 捕获标题内容
    re.MULTILINE)      # 匹配三级标题
    content = THIRD_HEADING_PATTERN.sub(replacer, content)
    logging.info("预处理完成")

    return content


def replacer(match):
        # 提取匹配内容
        # prefix = match.group(1)  # 原始错误标记（如 '# '）
        number_part = match.group(1)  # 编号部分（如 '1.1.1'）
        title_text = match.group(2)  # 标题内容
        
        # 判断是否满足转换条件
        if len(title_text) > 15:
            # 超过长度则保留原始格式
            return f"{number_part}{title_text}"
        
        # 转换为三级标题
        return f"\n### {number_part}{title_text}"

if __name__ == "__main__":
    # 读取文件
    with open("GB_T 44080-2024_核电厂可靠性、可用性、可维修性和安全性管理规范.md", "r", encoding="utf-8") as f:
        content = f.read()
    # 预处理
    processed_content = preprocess_md(content)
    # 保存结果
    with open("one.md", "w", encoding="utf-8") as f:
        f.write(processed_content)
    logging.info("预处理结果已保存至：one.md")