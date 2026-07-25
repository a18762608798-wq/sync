from multiprocessing import Pool
import time
import os


def square_number(x):
    print(f"任务 {x} 在进程 {os.getpid()} 执行")
    time.sleep(1)
    return x * x


def main():
    data = list(range(1, 100))

    with Pool(processes=10) as pool:
        results = pool.map(square_number, data)

    print(results)


if __name__ == "__main__":
    main()
