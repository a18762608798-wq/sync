import os
import re
import csv
from collections import Counter
import pandas as pd
import numpy as np


# use to cancel proxy.
# unset http_proxy https_proxy all_proxy
# unset HTTP_PROXY HTTPS_PROXY ALL_PROXY
def is_text_file(file_path):
    """通过文件后缀判断是否为文本文件"""
    text_extensions = [".txt", ".md", ".qmd", ".tex", "html", ".ipynb"]
    return any(file_path.lower().endswith(ext) for ext in text_extensions)


def merge_all_text_files(root_directory, output_file="merged_all_files.txt"):
    """递归遍历目录，合并所有文本文件"""
    if not os.path.exists(root_directory):
        print(f"错误：目录 '{root_directory}' 不存在")
        return False

    print(f"开始遍历目录: {root_directory}")

    # 收集所有文本文件
    text_files = []
    for root, _, files in os.walk(root_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                text_files.append(file_path)

    print(f"找到 {len(text_files)} 个文本文件")

    if not text_files:
        print("未找到文本文件")
        return False

    # 合并文件
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(f"=== 文件合并报告 ===\n")
        outfile.write(f"源目录: {root_directory}\n")
        outfile.write(f"总文件数: {len(text_files)}\n")
        outfile.write("=" * 50 + "\n\n")

        for i, file_path in enumerate(text_files, 1):
            relative_path = os.path.relpath(file_path, root_directory)
            print(f"[{i}/{len(text_files)}] {relative_path}")

            outfile.write(f"=== 文件 {i}: {relative_path} ===\n")
            outfile.write("-" * 40 + "\n")

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                    outfile.write(infile.read())
            except:
                outfile.write("[文件读取失败]")

            outfile.write("\n\n" + "=" * 60 + "\n\n")

    print(f"\n合并完成！结果保存到: {os.path.abspath(output_file)}")
    return True


def count_word_frequency_and_save_csv(input_file, output_file="word_frequency.csv"):
    """
    统计txt文件中英文单词的频数，排除中文、标点符号、特殊符号和单个字母的单词，并保存到CSV文件

    参数:
        input_file (str): 输入的txt文件路径
        output_file (str): 输出的CSV文件路径，默认为'word_frequency.csv'
    """
    try:
        # 读取文件内容
        with open(input_file, "r", encoding="utf-8") as file:
            text = file.read()

        # 使用正则表达式提取只包含英文字母的单词，并转换为小写
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        # 过滤掉单个字母的单词（长度为1的单词）
        filtered_words = [word for word in words if len(word) >= 2]

        # 统计单词频数
        word_counts = Counter(filtered_words)

        # 按频数降序排列
        sorted_word_counts = sorted(
            word_counts.items(), key=lambda x: x[1], reverse=True
        )

        # 将结果保存到CSV文件
        with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # 写入CSV标题行
            writer.writerow(["word", "frequency"])
            # 写入数据行
            for word, count in sorted_word_counts:
                writer.writerow([word, count])

        print(
            f"统计完成！共找到 {len(sorted_word_counts)} 个不同单词（已排除单个字母的单词）"
        )
        print(f"结果已保存到: {output_file}")
        print(f"前10个最频繁的单词:")
        for word, count in sorted_word_counts[:10]:
            print(f"  {word}: {count}")

        return sorted_word_counts

    except FileNotFoundError:
        print(f"错误：文件 '{input_file}' 未找到。")
        return []
    except Exception as e:
        print(f"发生错误：{e}")
        return []


# 使用示例
if __name__ == "__main__":
    # 设置输入文件路径（请修改为您的实际文件路径）
    txt_path = "/home/ubuntu-usr/sync/tool/new_word_learn/data/merged_all_files.txt"
    frequency_csv = "/home/ubuntu-usr/sync/tool/new_word_learn/data/word_frequency.csv"
    merge_all_text_files("/home/ubuntu-usr/sync", txt_path)
    # 调用函数进行统计并保存到CSV
    result = count_word_frequency_and_save_csv(txt_path, frequency_csv)
    os.remove(txt_path)
