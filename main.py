import os
import main_test
from requirement import *

#统计文件夹下的文件个数
def show_file_tree(path):

    #获取当前目录下的文件列表
    file_list=os.listdir(path)
    global folder_count
    folder_count = 0
     
     #遍历文件列表，如果当前文件不是文件夹，则文件数量+1，如果是文件夹，则文件夹数量+1且再调用统计文件个数的方法
    for i in file_list:
        path_now = path + "\\" + i
        if os.path.isdir(path_now)==True:
            folder_count=folder_count+1


def batch_optimize_markdown(input_dir: str, output_dir: str):
    """批量优化OCR生成的Markdown文件"""
    # 创建输出目录
    # os.makedirs(output_dir, exist_ok=True)
    i = 1
    # 遍历所有子文件夹
    for subdir in os.listdir(input_dir):
        
        logging.info(f"正在处理第{i}/{folder_count}个文件夹")
        i += 1

        subdir_path = os.path.join(input_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue
        
        # 查找Markdown文件
        md_files = [f for f in os.listdir(subdir_path) if f.endswith(".md")] # 查找subdir_path中以.md结尾的文件
        
        if not md_files:
            print(f"No markdown file found in {subdir_path}")
            continue
        
        # 读取Markdown内容
        md_file = md_files[0]  # 假设每个子文件夹只有一个md文件
        md_path = os.path.join(subdir_path, md_file)
        
        # 调用LLM优化（假设已有优化函数）
        main_test.optimize_ocr_document(
            md_path, 
            md_path,
            max_tokens=4096, 
            embedding_name="F:\\fucking models\\Qwen2.5-7B",
            model_name="qwen2.5:14b")  # 替换为实际优化函数

# 使用示例

if __name__ == '__main__':
    show_file_tree("ocr_result")

    logging.info(f"开始处理文件夹,目录下文件夹数量一共{folder_count}个")

    batch_optimize_markdown(
        input_dir="ocr_result",
        output_dir="optimized_output"
    )
    logging.info(f"所有文件夹(一共{folder_count}个)已全部处理完成")
