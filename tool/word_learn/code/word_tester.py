import numpy as np
import pandas as pd
import os
import ollama
import asyncio
import pyttsx3
from word_score import process_word_list, calculate_score


class WordTester:
    def __init__(self):
        self.data_path = "./data"
        self.word_list_txt = os.path.join(self.data_path, "word_list.txt")
        self.word_score_csv = os.path.join(self.data_path, "word_score.csv")
        self.word_frequency_csv = os.path.join(self.data_path, "word_frequency.csv")
        self.word_unfamiliar_csv = os.path.join(self.data_path, "word_unfamiliar.csv")
        self.model_name = "gemma3:27b-cloud"

    async def translate_word(self, word):
        response = ollama.generate(
            model=self.model_name,
            system="给出我给出单词的音标（英）以及最常用的3-5个中文含义，以分号相隔; 需要严格按照格式,不要换行：比如我说technology, 你回答：[tekˈnɒlədʒi]。科技，技术；技术设备，先进机器；工艺学。",
            prompt=word,
        )
        return response["response"]

    @staticmethod
    def add_word(word, meaning, word_list_txt):
        with open(word_list_txt, "a", encoding="utf-8") as f:
            f.write(f"{word} # {meaning}\n")

    @staticmethod
    def delete_word(word, word_list_txt):
        if not os.path.exists(word_list_txt):
            print("单词列表文件不存在。")
            return
        with open(word_list_txt, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(word_list_txt, "w", encoding="utf-8") as f:
            delete_num = 0
            for line in lines:
                line_start = line[0 : min(len(line), len(word) + 1)]
                if line == "\n":
                    continue
                elif line_start == word and len(line) == len(word) + 1:
                    delete_num += 1
                    if delete_num == 1:
                        continue
                    else:
                        f.write(line)
                elif line_start == word + " ":
                    delete_num += 1
                    if delete_num == 1:
                        continue
                    else:
                        f.write(line)
                else:
                    f.write(line)

    async def test_word(self):
        engine = pyttsx3.init()  # 初始化语音引擎
        while True:
            # 重置文件，重新统计word_unfamiliar.csv
            process_word_list(self.word_list_txt, self.word_unfamiliar_csv)
            df1 = pd.read_csv(self.word_unfamiliar_csv)
            df2 = pd.read_csv(self.word_frequency_csv)
            calculate_score(df1, df2, self.word_score_csv)
            os.remove(self.word_unfamiliar_csv)
            word_score_df = pd.read_csv(self.word_score_csv)
            # 归一化score作为概率权重
            weights = word_score_df["score"] / word_score_df["score"].sum()
            # 随机选择一个索引（按权重概率）
            selected_idx = np.random.choice(word_score_df.index, p=weights)
            # 获取选中的整行数据
            selected_row = word_score_df.loc[selected_idx]
            word = selected_row["word"]
            translation_task = asyncio.create_task(self.translate_word(word))
            if (
                input("Please input the meaning of <{}>: ".format(word)).lower()
                == "exit"
            ):
                break
            engine.say(word)  # read the word aloud
            engine.runAndWait()
            meaning = await translation_task
            meaning = meaning.replace("\n", "").replace("\r", "")
            answer = input(
                "Correct meaning: <{}>, correct or not(y, n or d):".format(meaning)
            )
            if answer.lower() == "y":
                self.delete_word(word, self.word_list_txt)
                print("Great! Moving to the next word.")
            elif answer.lower() == "n":
                self.add_word(word, meaning, self.word_list_txt)
                print("Let's try again later.")
            elif answer.lower() == "d":
                print(word_score_df.head())
                input("Press Enter to continue...")
            elif answer.lower() == "exit":
                print("Exiting the tester.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    tester = WordTester()
    asyncio.run(tester.test_word())
