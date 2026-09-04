# -------------
# reflect 的 shadow 估计
# -------------

"""
get_reflect_shadow(filepath, sites, meas_indices_py, permuted_order; G, compute_sem, show_progress)

用经典 shadow 计算反射算符 Z_r 的期望值。

参数
- filepath::String：存好的 shadow/group 数据路径。
- sites：全系统的 site index。
- meas_indices_py：python 的 meas_indices（从 0 开始的二维列表）。
- permuted_order：在算 shadow 之前对 site 做的置换顺序。

关键词参数
- G::Vector{Float64}：每个 site 的权重（默认全 1），按 permuted_order 置换。
- compute_sem::Bool：为 true 时同时计算均值标准误差（SEM）。
- show_progress::Bool：为 true 时计算过程中显示进度。

返回
- compute_sem == false：返回 real(expectation)::Float64。
- compute_sem == true：返回 (real(expectation)::Float64, sem::Float64)。

说明
本函数从 filepath 载入重排后的 group，为重排后的系统构造 dense shadow，
再构造反射用的相邻 swap 算符，把期望/SEM 估计交给
modified_get_expect_shadow。
"""
function get_reflect_shadow(
    filepath::String,
    sites,
    meas_indices_py,
    permuted_order;
    G=fill(1.0, sum(length.(meas_indices_py)))::Vector{Float64},
    compute_sem=false,
    show_progress=true,
)
    permuted_G = G[permuted_order]
    permuted_group, permuted_indices = import_random_group(
        filepath, sites, meas_indices_py, permuted_order
    )
    permuted_shadows = get_dense_shadows(permuted_group; G=permuted_G)
    adjacent_swap_op = create_adjacent_swap_op(permuted_indices)

    if compute_sem
        reflect_expect, sem = modified_get_expect_shadow(
            adjacent_swap_op,
            permuted_shadows;
            compute_sem=compute_sem,
            show_progress=show_progress,
        )
        return real(reflect_expect), sem
    else
        reflect_expect = modified_get_expect_shadow(
            adjacent_swap_op,
            permuted_shadows;
            compute_sem=compute_sem,
            show_progress=show_progress,
        )
        return real(reflect_expect)
    end
end

# -------------
# reflect 的 hamming 估计
# -------------
"""
get_reflect_hamming(data::MeasurementData)

对单个 MeasurementData 用 Hamming 距离法算反射期望值。

参数
- data::MeasurementData：单个测量数据集。

返回
- reflect_est::Float64：反射期望的估计值。

说明
估计子公式：R = (1/NM) * Σ_m 2^pairs * (-2)^(-hamming_dist(m))，
其中系统按相邻奇偶 site 配成对。
"""
function get_reflect_hamming(
    data::MeasurementData,
)
    # 取数据
    qubits_num = data.N
    m_num = data.NM
    results = data.measurement_results
    pairs_num = qubits_num ÷ 2
    odd_order = [2i - 1 for i in 1:pairs_num]
    even_order = [2i for i in 1:pairs_num]

    # 算 reflect 估计
    ssum = 0
    for m_idx = 1:m_num
        result = results[m_idx, :]
        odd_result = @view result[odd_order]
        even_result = @view result[even_order]
        hamming_dist = sum(odd_result .!= even_result)
        ssum += (-2.0)^(-hamming_dist)
    end
    ssum *= 2.0^pairs_num

    reflect_est = ssum / m_num

    return reflect_est
end

"""
get_reflect_hamming(filepath, sites, meas_indices_py, permuted_order; compute_sem, show_progress)

用 Hamming 距离法从存好的测量数据算反射期望值，对各随机幺正设置求平均。

参数
- filepath::String：qmeas.random 生成的 .npz 文件路径。
- sites：全系统的 site index。
- meas_indices_py：python 的 meas_indices（从 0 开始的二维列表）。
- permuted_order：全部被测 site 的置换向量。

关键词参数
- compute_sem::Bool：为 true 时计算各随机幺正设置间的均值标准误差（SEM）。
- show_progress::Bool：为 true 时显示进度。

返回
- compute_sem == false：返回 reflect_est::Float64。
- compute_sem == true：返回 (reflect_est::Float64, sem::Float64)。

说明
本函数载入重排后的 group，对每个随机幺正设置调用
get_reflect_hamming(::MeasurementData) 算 Hamming 距离反射估计，
再对各设置求平均。
"""
function get_reflect_hamming(
    filepath::String,
    sites,
    meas_indices_py,
    permuted_order;
    compute_sem=false,
    show_progress=true,
)
    # 取数据
    group, _ = import_random_group(
        filepath, sites, meas_indices_py, permuted_order
    )
    u_num = group.NU
    datas = group.measurements
    reflect_ests = Vector{Float64}(undef, u_num)

    # 算 reflect 估计
    ssum = 0
    @showprogress desc="hamming_est..." enabled=show_progress @threads  for u_idx = 1:u_num
        data = datas[u_idx]
        reflect_ests[u_idx] = get_reflect_hamming(data)
    end
    
    reflect_est = mean(reflect_ests)

    if compute_sem
        sem = std(reflect_ests) / sqrt(u_num)
        return reflect_est, sem
    else
        reflect_est = mean(reflect_ests)
        return reflect_est
    end

end
