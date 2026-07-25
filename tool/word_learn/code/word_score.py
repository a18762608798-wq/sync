import re
import csv
from collections import Counter
import pandas as pd
import os
import numpy as np

def process_word_list(input_file_path, output_csv_path):
    """
    从文本文件按行读取单词，统计频数并写入CSV文件，过滤#号之后的文字
    
    参数:
        input_file_path (str): 输入文件路径
        output_csv_path (str): 输出CSV文件路径
    """
    try:
        word_counter = Counter()
        
        # 按行读取文件
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 去除行尾换行符
                line = line.strip()
                
                # 跳过空行
                if not line:
                    continue
                
                # 过滤#号之后的文字
                if '#' in line:
                    line = line.split('#')[0].strip()
                
                # 跳过处理后为空的行
                if not line:
                    continue
                
                # 转换为小写
                word = line.lower()
                
                # 直接统计，不添加额外过滤条件
                word_counter[word] += 1
        
        # 按频数降序排序
        sorted_words = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)
        
        # 写入CSV文件
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # 写入表头
            writer.writerow(['word', 'unfamiliar'])
            # 写入数据
            for word, count in sorted_words:
                writer.writerow([word, count])
        
        print(f"处理完成！共统计 {len(sorted_words)} 个条目")
        print(f"结果已保存至: {output_csv_path}")
        
        return True
    
    except FileNotFoundError:
        print(f"错误：文件未找到 - {input_file_path}")
        return False
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return False

def calculate_score(df1, df2, output_path):
    # 按word列合并两个CSV文件
    merged_df = pd.merge(df1, df2, on='word', how='left')

    # 处理没有找到frequency的情况（用0填充）
    merged_df['frequency'] = merged_df['frequency'].fillna(0)

    # 计算score列：score = (unfamiliar * log(frequency + 5))^4.0 / 10^6
    merged_df['score'] = (merged_df['unfamiliar'] * np.log(merged_df['frequency'] + 5)) ** 4.0 / 10**6

    # 将score列移动到word列之后
    cols = list(merged_df.columns)
    word_idx = cols.index('word')
    cols.remove('score')
    cols.insert(word_idx + 1, 'score')
    merged_df = merged_df[cols]

    # 排序
    merged_df = merged_df.sort_values(by='score', ascending=False)

    # 保存结果到新的CSV文件
    merged_df.to_csv(output_path, index=False)

    # 显示结果
    print("处理完成！结果已保存到:", output_path)
    print("\n前几行数据预览：")
    print(merged_df.head())

# 使用示例
if __name__ == "__main__":
    word_list_txt = "/home/ubuntu-usr/sync/tool/new_word_learn/data/word_list.txt"
    word_unfamiliar_csv = '/home/ubuntu-usr/sync/tool/new_word_learn/data/word_unfamiliar.csv'
    success = process_word_list(word_list_txt, word_unfamiliar_csv)
    # calculate_score 
    word_frequency_csv = '/home/ubuntu-usr/sync/tool/new_word_learn/data/word_frequency.csv'
    df1 = pd.read_csv(word_unfamiliar_csv)  # 替换为您的第一个CSV文件路径
    df2 = pd.read_csv(word_frequency_csv)  # 替换为您的第二个CSV文件路径
    word_score_csv = '/home/ubuntu-usr/sync/tool/new_word_learn/data/word_score.csv'
    calculate_score(df1, df2, word_score_csv)
    os.remove(word_unfamiliar_csv)
    
    