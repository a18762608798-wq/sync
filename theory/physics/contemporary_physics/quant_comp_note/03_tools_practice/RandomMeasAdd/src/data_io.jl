# ---------------------
# 从 qmeas.random 输出中导入单个 group，并按 permuted_order 重排。
# ---------------------

"""
从 qmeas.random 生成的 npz 文件中导入单个测量 group。

npz 文件把所有 group 沿被测 qubit 维拼在一起，用 `meas_indices`（展平、
python 从 0 开始编号）和 `group_sizes` 记录分组方式。本函数切出第 `group_idx`
个 group（Julia 从 1 开始编号），把 qubit 编号转为 Julia 惯例（+1）得到
`site_indices`，再用 `permuted_order` 对结果、设置和 site 统一重排。

参数
- filepath::String：qmeas.random 生成的单个 .npz 文件路径。
- sites：全系统的 site index（`siteinds("Qubit", N)`）；整数 qubit 编号
  用来索引这个向量。
- meas_indices_py：python 的 meas_indices（从 0 开始的二维列表，如
  `[[2,5],[3,4]]`，从 summary json 解析而来）。Julia 里是 `Vector` 套向量
  或其他可迭代结构；内层每个元素都是从 0 开始的。
- group_idx::Int：要导入第几个 group（Julia 从 1 开始编号）。
- permuted_order：group 内 site 的置换向量（Julia 从 1 开始编号）。

返回
- permuted_group::MeasurementGroup
- permuted_sites：重排后的 site Index 对象。
"""
function import_random_group(
    filepath::String, sites, meas_indices_py, group_idx::Int, permuted_order
)
    groups_py = [collect(Int, g) for g in meas_indices_py]
    @assert 1 <= group_idx <= length(groups_py) "group_idx out of range"
    # python 从 0 开始 -> julia 从 1 开始的 qubit 编号
    qubits_jl = groups_py[group_idx] .+ 1
    site_indices = sites[qubits_jl]
    # 该 group 在展平后的 n_meas 维中所占的列区间
    offset = group_idx == 1 ? 0 : sum(length.(groups_py[1:(group_idx-1)]))

    cols = (offset+1):(offset+length(site_indices))

    group_data = npzread(filepath)
    meas_res = 2 .- Int64.(group_data["measurement_results"][:, :, cols])
    settings = ComplexF64.(group_data["measurement_settings"][:, cols, :, :])

    permuted_indices = site_indices[permuted_order]
    permuted_meas_res = meas_res[:, :, permuted_order]
    permuted_settings = settings[:, permuted_order, :, :]
    permuted_group = MeasurementGroup(
        permuted_meas_res, permuted_settings, permuted_indices
    )
    return permuted_group, permuted_indices
end

"""
简便重载：不依赖外部 python 列表，直接用 npz 文件自带的
`meas_indices` + `group_sizes` 还原分组。

参数
- filepath::String，全系统 siteinds 构成的 sites，第 group_idx 个 group
 （Julia 从 1 开始编号），permuted_order。
"""
function import_random_group(filepath::String, sites, group_idx::Int, permuted_order)
    group_data = npzread(filepath)
    flat = vec(Int64.(group_data["meas_indices"])) # python 从 0 开始编号
    sizes = vec(Int64.(group_data["group_sizes"]))
    @assert sum(sizes) == length(flat) "meas_indices/group_sizes mismatch"
    @assert 1 <= group_idx <= length(sizes) "group_idx out of range"
    offset = sum(sizes[1:(group_idx-1)]; init=0)
    # python 从 0 开始 -> julia 从 1 开始的 qubit 编号，再索引 sites
    qubits_jl = flat[(offset+1):(offset+sizes[group_idx])] .+ 1
    site_indices = sites[qubits_jl]
    cols = (offset+1):(offset+sizes[group_idx])

    meas_res = 2 .- Int64.(group_data["measurement_results"][:, :, cols])
    settings = ComplexF64.(group_data["measurement_settings"][:, cols, :, :])

    permuted_indices = site_indices[permuted_order]
    permuted_group = MeasurementGroup(
        meas_res[:, :, permuted_order],
        settings[:, permuted_order, :, :],
        permuted_indices,
    )
    return permuted_group, permuted_indices
end



