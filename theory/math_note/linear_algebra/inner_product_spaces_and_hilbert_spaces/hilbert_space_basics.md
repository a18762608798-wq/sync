# Hilbert schmidt basics

## bases

For any operator or state, there are

$$
\begin{cases}
\hat \rho = \sum\limits_{i}tr(\hat R_i^\dagger \hat \rho)\hat R_i\\
\hat O = \sum\limits_l tr(\hat O_l^\dagger\hat O)\hat O_l^\dagger
\end{cases}
$$

where

$$
\begin{cases}
tr(\hat R_i^\dagger \hat R_j) = \delta_{ij}\\
\hat R_{i,b}^{a*} \hat {R_{i, d}^c} = \delta_{ac}\delta_{bd} 
\end{cases}
$$

The reason of completeness is own to the follow expression holds true for any $\rho$

$$
\rho = \sum_i tr(R^\dagger \rho) R_i
$$

## 夹角余弦

和向量类似

$$
\frac{tr(\rho_1\rho_2)}{\sqrt{tr(\rho_1^2)tr(\rho_2^2)}}
$$

本质上和铺平的向量没有区别，用张量表示很容易发现的.