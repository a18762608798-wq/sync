# state product

## general state

Wait for learning.

## special state

### classical state

#### Bell base

We could explan the circuits via the transform of $\{ZI, IZ\}$ to $\{XX, ZZ\}$

Known bell base

$$
\begin{cases}
|\psi^-\rangle = \frac{1}{\sqrt 2} (|01\rangle \pm |10\rangle) \\
|\phi^-\rangle = \frac{1}{\sqrt 2} (|00\rangle \pm |11\rangle) \\
\end{cases}
$$

Bell state circuits are producted as follow

```text
|00⟩ + |11⟩
     ┌───┐     
q_0: ┤ H ├──■──
     └───┘┌─┴─┐
q_1: ─────┤ X ├
          └───┘
c: 2/══════════
               
Statevector([0.70710677+0.j, 0.        +0.j, 0.        +0.j,
             0.70710677+0.j],
            dims=(2, 2))

|00⟩ - |11⟩
     ┌───┐┌───┐     
q_0: ┤ X ├┤ H ├──■──
     └───┘└───┘┌─┴─┐
q_1: ──────────┤ X ├
               └───┘
c: 2/═══════════════
                    
Statevector([ 0.70710677+0.0000000e+00j,  0.        +0.0000000e+00j,
              0.        +0.0000000e+00j, -0.70710677-8.6595606e-17j],
            dims=(2, 2))

|01⟩ + |10⟩
     ┌───┐     
q_0: ┤ H ├──■──
     ├───┤┌─┴─┐
q_1: ┤ X ├┤ X ├
     └───┘└───┘
c: 2/══════════
               
Statevector([0.        +0.j, 0.70710677+0.j, 0.70710677+0.j,
             0.        +0.j],
            dims=(2, 2))


|01⟩ - |10⟩
     ┌───┐┌───┐     
q_0: ┤ X ├┤ H ├──■──
     ├───┤└───┘┌─┴─┐
q_1: ┤ X ├─────┤ X ├
     └───┘     └───┘
c: 2/═══════════════
                    
Statevector([ 0.        +0.0000000e+00j, -0.70710677-8.6595606e-17j,
              0.70710677+0.0000000e+00j,  0.        +0.0000000e+00j],
            dims=(2, 2))
```

#### GHZ state

$N$ 比特 GHZ 态通常定义为

$$
|\mathrm{GHZ}_N\rangle = \frac{|0\rangle^{\otimes N}+|1\rangle^{\otimes N}}{\sqrt2}.
$$

最常见的制备思路是：

1. 先在一个比特上制造叠加；
2. 再把这个比特的信息依次复制到其他比特上。

##### 标准制备电路

初态为 $|0\rangle^{\otimes N}$。

先对第一个比特施加 Hadamard 门：

$$
|0\cdots0\rangle \xrightarrow{H_1} \frac{|0\rangle+|1\rangle}{\sqrt2} \otimes|0\cdots0\rangle.
$$

然后以第一个比特为控制，对其余比特施加 CNOT：

$$
\mathrm{CNOT}_{1\to2},\; \mathrm{CNOT}_{1\to3},\; \ldots,\; \mathrm{CNOT}_{1\to N}.
$$

最终得到

$$
\frac{|00\cdots0\rangle+|11\cdots1\rangle}{\sqrt2}.
$$

例如三比特：

$$
|000\rangle \xrightarrow{H_1} \frac{|000\rangle+|100\rangle}{\sqrt2}
\xrightarrow{\mathrm{CNOT}_{1\to2}} \frac{|000\rangle+|110\rangle}{\sqrt2}
\xrightarrow{\mathrm{CNOT}_{1\to3}} \frac{|000\rangle+|111\rangle}{\sqrt2}.
$$

电路示意为

```text
q0: ──H──■────■──
         │    │
q1: ─────X────┼──
              │
q2: ──────────X──
```

##### 其他GHZ

**对相减的GHZ在最后任意一个比特取Z即可**

对于形如 $|0101...\rangle + |1010...\rangle$

只要加基础门制作后在需要1的位置加X门就可以.

例如 $|0101\rangle - |1010\rangle$

```text
     ┌───┐     ┌───┐┌───┐     
q_0: ┤ H ├──■──┤ Z ├┤ X ├─────
     └───┘┌─┴─┐└───┘└───┘     
q_1: ─────┤ X ├──■────────────
          └───┘┌─┴─┐     ┌───┐
q_2: ──────────┤ X ├──■──┤ X ├
               └───┘┌─┴─┐└───┘
q_3: ───────────────┤ X ├─────
                    └───┘     
Statevector([ 0.00000000e+00+0.j,  0.00000000e+00+0.j,  0.00000000e+00+0.j,
              0.00000000e+00+0.j,  4.32978030e-17+0.j,  7.07106769e-01+0.j,
              0.00000000e+00+0.j,  0.00000000e+00+0.j,  0.00000000e+00+0.j,
              0.00000000e+00+0.j, -7.07106769e-01+0.j,  4.32978030e-17+0.j,
              0.00000000e+00+0.j,  0.00000000e+00+0.j,  0.00000000e+00+0.j,
              0.00000000e+00+0.j],
            dims=(2, 2, 2, 2))
```

##### 高效制备

只允许相邻local gate就从中间出发即可.
