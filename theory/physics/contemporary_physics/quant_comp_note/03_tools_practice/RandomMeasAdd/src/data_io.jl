# ---------------------
# 从 qmeas.random 输出（一次 SettingRun）导入 MeasurementGroup，并按 permuted_order 重排。
# ---------------------

"""
从 qmeas.random 生成的 npz 文件中导入一次 SettingRun 的完整数据，
构造一个 MeasurementGroup。

npz 文件存了一次 SettingRun 下所有被测 qubit 的数据
（`measurement_results` 形状为 (num_settings, num_shots, n_meas)，
n_meas 为所有 qmeas 分组拼起来的总列数），另有 `meas_indices`（展平、
python 从 0 开始编号）和 `group_sizes` 记录列分组方式。
本函数取全部列，qubit 编号转为 Julia 惯例（+1），
再用 `permuted_order` 对结果、设置和 site 统一重排。

参数
- filepath::String：qmeas.random 生成的单个 .npz 文件路径。
- sites：全系统的 site index（`siteinds("Qubit", N)`）；整数 qubit 编号
  用来索引这个向量。
- meas_indices_py：python 的 meas_indices（从 0 开始的二维列表，如
  `[[2,5],[3,4]]`，从 summary json 解析而来）。只用它的展平顺序还原
  qubit 编号，不按它切分。
- permuted_order：全部被测 site 的置换向量（Julia 从 1 开始编号），
  长度等于被测 qubit 总数。

返回
- permuted_group::MeasurementGroup
- permuted_sites：重排后的 site Index 对象。
"""
function import_random_group(
    filepath::String, sites, meas_indices_py, permuted_order
)
    # python 从 0 开始 -> julia 从 1 开始的 qubit 编号（展平后的全部被测 qubit）
    qubits_jl = vcat([collect(Int, g) for g in meas_indices_py]...) .+ 1
    site_indices = sites[qubits_jl]

    group_data = npzread(filepath)
    meas_res = 2 .- Int64.(group_data["measurement_results"])
    settings = ComplexF64.(group_data["measurement_settings"])

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
`meas_indices` 还原被测 qubit 编号。

参数
- filepath::String，全系统 siteinds 构成的 sites，
  全部被测 site 的 permuted_order。
"""
function import_random_group(filepath::String, sites, permuted_order)
    group_data = npzread(filepath)
    # python 从 0 开始 -> julia 从 1 开始的 qubit 编号，再索引 sites
    qubits_jl = vec(Int64.(group_data["meas_indices"])) .+ 1
    site_indices = sites[qubits_jl]

    meas_res = 2 .- Int64.(group_data["measurement_results"])
    settings = ComplexF64.(group_data["measurement_settings"])

    permuted_indices = site_indices[permuted_order]
    permuted_group = MeasurementGroup(
        meas_res[:, :, permuted_order],
        settings[:, permuted_order, :, :],
        permuted_indices,
    )
    return permuted_group, permuted_indices
end


