import sys
import json
import numpy as np  # 新增

def main():
    # 获取输入参数（采样点数 N）
    try:
        N = int(sys.argv[1])
        if N <= 0:
            raise ValueError
    except:
        N = 100000  # 默认值，防止出错
    
    # NumPy 蒙特卡洛计算 π
    rng = np.random.default_rng()
    x = rng.random(N)          # [0,1) 区间 N 个随机数
    y = rng.random(N)
    inside = np.sum(x**2 + y**2 <= 1.0)  # 向量化判断落在单位圆内
    pi_approx = 4.0 * inside / N
    
    # 输出结果
    result = {
        "status": "success",
        "N": N,
        "pi_approx": float(pi_approx),
        "error_from_3.1415926535": abs(pi_approx - 3.141592653589793),
        "message": f"Hello from Golem! π ≈ {pi_approx} (N={N})"
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()