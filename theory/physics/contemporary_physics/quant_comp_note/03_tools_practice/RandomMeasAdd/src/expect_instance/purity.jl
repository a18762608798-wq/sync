# ----------
# purity（纯度）
# ----------
"""
get_purity_shadow(filepath, sites, meas_indices_py, group_idx, permuted_order; G, compute_sem, show_progress)

用经典 shadow 从存好的测量数据估计纯度 Tr(ρ²)。

参数
- filepath::String：qmeas.random 生成的 .npz 文件路径。
- sites：全系统的 site index。
- meas_indices_py：python 的 meas_indices（从 0 开始的二维列表）。
- group_idx::Int：要导入第几个 group（Julia 从 1 开始编号）。
- permuted_order：group 内 site 的置换向量。

关键词参数
- G::Vector{Float64}：每个 site 的权重（默认全 1），按 permuted_order 置换。
- compute_sem::Bool：为 true 时同时计算均值标准误差（SEM）。
- show_progress::Bool：为 true 时显示进度。

返回
- compute_sem == false：返回 purity::Float64。
- compute_sem == true：返回 (purity::Float64, sem::Float64)。

说明
本函数从 filepath 载入重排后的 group，构造 dense shadow，
再交给 modified_get_purity_shadow 做纯度估计。
"""
function get_purity_shadow(
    filepath::String,
    sites,
    meas_indices_py,
    group_idx::Int,
    permuted_order;
    G=fill(1.0, length(collect(meas_indices_py[group_idx])))::Vector{Float64},
    compute_sem=false,
    show_progress=true,
)
    permuted_G = G[permuted_order]
    permuted_group, permuted_indices = import_random_group(
        filepath, sites, meas_indices_py, group_idx, permuted_order
    )
    shadows = get_dense_shadows(permuted_group; G=permuted_G)

    if compute_sem
        purity, _, sem = modified_get_purity_shadow(
            shadows;
            compute_sem=compute_sem,
            show_progress=show_progress,
        )
        return purity, sem

    else
        purity = modified_get_purity_shadow(
            shadows;
            compute_sem=compute_sem,
            show_progress=show_progress,
        )
        return purity

    end
end

"""
get_purity_hamming(filepath, sites, meas_indices_py, group_idx, permuted_order; compute_sem, show_progress)

用基于重叠的方法（"hamming" 变体）从存好的测量数据估计纯度 Tr(ρ²)，
对各随机幺正设置求平均。

参数
- filepath::String：qmeas.random 生成的 .npz 文件路径。
- sites：全系统的 site index。
- meas_indices_py：python 的 meas_indices（从 0 开始的二维列表）。
- group_idx::Int：要导入第几个 group（Julia 从 1 开始编号）。
- permuted_order：group 内 site 的置换向量。

关键词参数
- compute_sem::Bool：为 true 时计算各随机幺正设置间的均值标准误差（SEM）。
- show_progress::Bool：为 true 时显示进度。

返回
- compute_sem == false：返回 purity_est::Float64。
- compute_sem == true：返回 (purity_est::Float64, sem::Float64)。

说明
本函数载入重排后的 group，对每个随机幺正设置调用
get_overlap(data, data; apply_bias_correction=true) 算纯度，
再对各设置求平均。
"""
function get_purity_hamming(
    filepath::String,
    sites,
    meas_indices_py,
    group_idx::Int,
    permuted_order;
    compute_sem=false,
    show_progress=true,
)
    group, _ = import_random_group(
        filepath, sites, meas_indices_py, group_idx, permuted_order
    )

    u_num = group.NU
    datas = group.measurements
    purity_ests = Vector{Float64}(undef, u_num)

    @showprogress desc="hamming_est..." enabled=show_progress @threads for u_idx = 1:u_num
        data = datas[u_idx]
        purity_ests[u_idx] = get_overlap(data, data, apply_bias_correction=true)
    end

    purity_est = mean(purity_ests)

    if compute_sem
        sem = std(purity_ests) / sqrt(u_num)
        return purity_est, sem

    else
        purity_est = mean(purity_ests)
        return purity_est

    end
end



