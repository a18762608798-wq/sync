# Data calculation

## Data storage and display

### Format case

```matlab
format short
```

### Order

* common

```matlab
short %Fixed point number: 3-digit integers and 4-digit decimals，if it is out of range, using short e.
long %Fixed point number: 3-digit integers and 4-digit decimals, if it is out of range, using longe.
short e%Floating number-rounding off: 1-digit integers and 4-digit decimals.
long e%Floating number-rounding off: 1-digit intrgers ans 15-digit decimals.
short g%Floating or fixed point number: 5-digit
short g%Floating or fixed point number: 15-digit
```

* scarce

```matlab
hex %16-digit hexadecimal
bank %Fixed point number
+ %reveal positive or negative number
rational %Fractional approximation
```

* Concept specification
  * Float number: float number is approximation of rounding off like **short e** and **long g**. 
  * Fixed point number: The degree of accuracy an not be turned.

## Special variables

```matlab
pi 
eps %minimum value interval,2.2204e-16;
Inf %more than 10^308;
NaN %non-number,case:0/0;
0 %less than 10^-322;
realmin %minninum floating point number;
realmax %maximum floating point number;
```

## Equation

### equation with one unknown quantity
* $ax^2+bx+c=0$

```matlab 
syms a b c x;
f=a*x^2+b*x+c==0;
solution=solve(f,x);
```

### equation with multiple unknown quantity

* 
$$
\begin{cases}
\frac{1}{x}+\frac{1}{y+z}=\frac{1}{r_1}\\
\frac{1}{y}+\frac{1}{x+z}=\frac{1}{r_2}\\
\frac{1}{z}+\frac{1}{x+y}=\frac{1}{r_3}\\
\end{cases}
$$

```matlab
syms x y z r1 r2 r3;
f1=1/x+1/(y+z)==1/r1;
f2=1/y+1/(z+x)==1/r2;
f3=1/z+1/(x+y)==1/r3;
[solution1,solution2,solution3]=solve(f1,f2,f3,x,y,z); %the sequence of x,y,z is effect to solutions
%If we use:
solutions=solve(1/x+1/(y+z)-1/r1,1/y+1/(z+x)-1/r2,1/z+1/(x+y)-1/r3);
%solutions is a structural body.
```

### ODE(ordinary differential equation)

* $\frac{dx}{dt}=-ax$

```matlab
solution=dsolve('Dx=-ax');
```

​	*This way can not be used,because $Dx$ can not be recognized:* 

```matlab
syms x,a
f=Dx+ax;
solution=dsolve(f);
```



