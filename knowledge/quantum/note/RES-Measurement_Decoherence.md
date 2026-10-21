# Measurement Essence via Decoherence

**INTERPRET:**

测量的本质是什么? 测量与所谓偏好基, 环境的关联是什么?

**ASSUME:**

$S$ 为量子比特， $A$ 为 仪器 ， $E$ 为 环境。

**DEFINITION:**

$$
[H_{AE}, |0\rangle_A\langle 0|] \approx 0 \tag{1}
$$

满足 (1) 的 $\{|0\rangle_A, |1\rangle_A\}$ 称为偏好基。测量过程环境只能被其作用. 也即 $A \rightarrow E$.

$$
D_{ji} = \langle E_j'|E_i'\rangle \tag{2}
$$

称为退相干因子。

## Phase 1

**INTERPRET:**

这里证明双比特系统没有传统测量概念.

**WLOG**:

$$
|\psi_{S_0}\rangle = |s_0\rangle + |s_1\rangle
$$

**NOTE:**

这里由于态都是等权叠加忽略叠加系数.

**HAVE:**

考虑指针需要记录态的状态, 不妨设测量过程有:

$$
U_{SA} |s_0a_0\rangle = |s_0a_0\rangle + |s_0a_1\rangle \tag{3}
$$

**WHERE:**

$$
U_{SA} = CNOT
$$

**INTUITION:**

这里似乎已经可以用指针标定态. 但是需要注意, $(3)$ 作为bell态分解方式不唯一. 因此实际上没有其他环境, 只有人类指针和被测量系统, 我们似乎无法诠释自己和被测量系统是什么.

## Phase 2

**INTERPRET:**

引入环境和偏好基.

**BECAUSE:**

偏好基在环境下保持稳定, 因此只有A作用E, E基本不作用A. 可以把这种作用抽象为CNOT.

**HAVE:**

$$
U_{AE} (|0\rangle_A + |1\rangle_A)|0\rangle_E = |00\rangle_{AE} + |11\rangle_{AE} \tag{4}
$$

**LET:**

把被偏好基标定的系统状态也记做 0, 1.

**BY:**

(3)(4)

**HAVE:**

$$
U_{SAE} (|0\rangle + |1\rangle)|01\rangle = GHZ
$$

**INTERPRET:**

注意这个GHZ无法像 (3) 中bell state那样被重写. 所以**偏好基是特殊唯一**的.

**THEREFORE:**

此时观察SA子系统, 有:

$$
\rho_{SA} = |00\rangle\langle 00| + |11\rangle \langle 11|
$$

退化为经典状态, 但是环境起到了筛选所谓偏好基的作用.

**INTUITION:**

同样的也可以作为多世界诠释, 人处于$|0\rangle_E$ 和 处于 $|1\rangle_E$ 的份数不同, 反应除了local的概率, 参考[RES-ManyWorlds_EqualWight](RES-ManyWorlds_EqualWeight.md)

## Phase3

**INTERPRET:**

如果无法完全区分E, 代表什么?

**BY:**

(2)

**HAVE:**

$$
\rho_{SA} = |00\rangle \langle 00| + |11\rangle \langle 11| + D_{10}|00\rangle\langle 11| + D_{01}|11\rangle\langle 00| \tag{5}
$$

**INTERPRET:**

这意味着子系统的态也没有完全被破坏. 但是这没有太大意义, 因为我们无法区分E和E', 自然无法区分指针A到底什么状态.

## Summary

测量是通过仪器与被测系统建立关联，并使相应的指针信息被其他物理系统记录，从而形成**可区分、可稳定**读取结果的过程。

只是仪器的跟随没有意义, 传统的**信息需要被环境(包括人)记录**, 而可以被稳定记录的指针状态在该分支观察者(**受控位**)的视角中是经典的.

测量结果被第三个系统以完全可区分的状态记录，使 SA 的约化态成为经典混合形式
