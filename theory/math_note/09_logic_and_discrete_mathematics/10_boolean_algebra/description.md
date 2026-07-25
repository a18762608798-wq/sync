# description

## operation rules

### exchange rate

$$
\begin{split}
a \otimes b = b \otimes a\\
a\land b=b\land a,\\
a\lor b=b\lor a  
\end{split}
$$

### binding rate

$$
\begin{split}
a \oplus b \oplus c = a \oplus (b \oplus c)\\
a\land(b\land c)=(a\land b)\land c  \\
a\lor(b\lor c)=(a\lor b)\lor c 
\end{split}
$$

### Allocation rate

$$
\begin{split}
a\land(b\lor c)=(a\land b)\lor(a\land c)  \\
a\lor(b\land c)=(a\lor b)\land(a\lor c)  \\
\neg(a\land b)=\neg a\lor \neg b  \\
\neg(a\lor b)=\neg a\land \neg b  
\end{split}
$$

## important case


xor:

$$
\begin{cases}
a \oplus a = 0\\
a \oplus 0 = a\\
a\oplus 1=\neg a  
\end{cases}
$$


幂等律：  

$$
a\land a=a,\qquad a\lor a=a  
$$

零元和幺元：  

$$
a\land 1=a,\qquad a\lor 1=1  
$$

补元：  

$$
a\land \neg a=0,\qquad a\lor \neg a=1  
$$
