## sum over binary vectors


$$
\sum_{\vec s}  f(\vec s)
$$

这里本质上就是：

- $\vec s=(s_1,\dots,s_N))$
    
- 每个 $s_i\in{0,1}$
    
- 没有额外约束
    

所以是在对整个离散空间

$$
\{0,1\}^N  
$$

中的所有点求和，也就是

 $$
\sum_{\vec s\in{0,1}^N} f(\vec s) = 
\sum_{s_1=0}^1 \cdots \sum_{s_N=0}^1 f(s_1,\dots,s_N).  
$$