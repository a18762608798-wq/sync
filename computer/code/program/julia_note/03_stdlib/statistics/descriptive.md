# descriptive

```{julia}
using Statistics
vec = [1, 2, 3, 4, 5, 6]
matrix = [1 2 3; 4 5 6]

mean(matrix; dims = 1)  
var(vec) # 样本方差
std(vec)
median(vec) # 中位数
```
