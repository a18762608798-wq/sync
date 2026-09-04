# --------------------------------------
# ----------反射量 (Z_r)----------
# --------------------------------------

"""
get_z_r_shadow(filepath, sites, meas_indices_py, group_idx, permuted_order; G, compute_sem, show_progress)

用经典 shadow 估计 Z_r 量（反射相关的观测量），
做法是把系统按相邻 site 配对，再由这些配对算出 Z_r。

参数
- filepath::String
    存好的 shadow/group 数据路径。
- sites
    全系统的 site index。
- meas_indices_py
    python 的 meas_indices（从 0 开始的二维列表）。
- group_idx::Int
    要导入第几个 group（Julia 从 1 开始编号）。
- permuted_order
    算 shadow 之前对 site 做的置换顺序。

关键词参数
- G::Vector{Float64}
    每个 site 的权重（默认全 1），按 permuted_order 置换。
- compute_sem::Bool
    为 true 时同时返回 jackknife 偏差估计和 SEM。
- show_progress::Bool
    为 true 时计算过程中显示进度。

返回
- compute_sem == false：返回 z_r_val::Float64（估计值）。
- compute_sem == true：返回三元组 (z_r_val::Float64, bias_estimate::Float64, sem::Float64)，
  其中 bias_estimate = z_r_val - z_r_jack（由 jackknife 值算出），sem 为标准误差。

说明
本函数：
- 载入重排后的 group，
- 把 qubit 按相邻配对拆成奇偶两个子系统，
- 为全系统和子系统分别构造 dense shadow，
- 构造相邻 swap 算符，
- 经 get_z_r_loos_shadow 算 jackknife 值，得到估计和（可选的）SEM。
"""
function get_z_r_shadow(
    filepath::String,
    sites,
    meas_indices_py,
    group_idx::Int,
    permuted_order;
    G=fill(1.0, length(collect(meas_indices_py[group_idx])))::Vector{Float64},
    compute_sem=false,
    show_progress=true,
)
    # 取三个系统的信息
    # 取 group
    permuted_group, permuted_indices = import_random_group(
        filepath, sites, meas_indices_py, group_idx, permuted_order
    )
    qubits_num = length(permuted_order)
    pairs_num = qubits_num ÷ 2
    odd_order = [2i - 1 for i in 1:pairs_num]
    even_order = [2i for i in 1:pairs_num]
    odd_group = reduce_to_subsystem(permuted_group, odd_order)
    even_group = reduce_to_subsystem(permuted_group, even_order)
    # 取每个系统的 G
    permuted_G = G[permuted_order]
    odd_G = permuted_G[odd_order]
    even_G = permuted_G[even_order]
    # 生成 shadow
    shadows = get_dense_shadows(permuted_group; G=permuted_G)
    odd_shadows = get_dense_shadows(odd_group; G=odd_G)
    even_shadows = get_dense_shadows(even_group; G=even_G)
    # 生成算符
    adjacent_swap_op = create_adjacent_swap_op(permuted_indices)

    # 算期望和 sem
    # 取 jackknife 信息
    n_ru = size(shadows, 1)
    z_r_est, z_r_loos = get_z_r_loos_shadow(
        shadows, odd_shadows, even_shadows, adjacent_swap_op, show_progress
    )
    # 取 sem
    if compute_sem
        variance = (n_ru - 1)^2 / n_ru * var(z_r_loos)
        sem = sqrt(variance)
        z_r_jack = n_ru * z_r_est - (n_ru - 1) * mean(z_r_loos)
        return z_r_est, z_r_est - z_r_jack, sem
    else
        return z_r_est
    end
end

