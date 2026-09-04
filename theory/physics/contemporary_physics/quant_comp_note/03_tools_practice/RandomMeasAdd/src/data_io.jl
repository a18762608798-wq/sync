# ---------------------
# 从 qmeas.random 输出（一次 SettingRun）导入 MeasurementGroup，并按 permuted_order 重排。
# ---------------------

"""
从 qmeas.random 生成的 npz 文件中导入一次 SettingRun 的完整数据，
构造一个 MeasurementGroup。

npz 文件存了一次 SettingRun 下所有被测 qubit 的数据
（`measurement_results` 形状为 (num_settings, num_shots, n_meas)），
另有 `meas_indices`（展平、python 从 0 开始编号）记录被测 qubit。
本函数取全部列，qubit 编号转为 Julia 惯例（+1），
再用 `permuted_order` 对结果、设置和 site 统一重排。
summary json 只给人看，导入不需要它。

参数
- filepath::String：qmeas.random 生成的单个 .npz 文件路径。
- sites：全系统的 site index（`siteinds("Qubit", N)`）；整数 qubit 编号
  用来索引这个向量。
- permuted_order：全部被测 site 的置换向量（Julia 从 1 开始编号），
  长度等于被测 qubit 总数。缺省为 `nothing`，表示链式（恒等置换），
  即按 npz 列顺序直接导入。

返回
- permuted_group::MeasurementGroup
- permuted_sites：重排后的 site Index 对象。
"""
function import_random_group(filepath::String, sites; permuted_order=nothing)
    group_data = npzread(filepath)
    # python 从 0 开始 -> julia 从 1 开始的 qubit 编号，再索引 sites
    qubits_jl = vec(Int64.(group_data["meas_indices"])) .+ 1
    site_indices = sites[qubits_jl]

    meas_res = 2 .- Int64.(group_data["measurement_results"])
    settings = ComplexF64.(group_data["measurement_settings"])

    # 缺省链式：保持 npz 列顺序
    if isnothing(permuted_order)
        permuted_order = collect(1:length(site_indices))
    end
    permuted_indices = site_indices[permuted_order]
    permuted_group = MeasurementGroup(
        meas_res[:, :, permuted_order],
        settings[:, permuted_order, :, :],
        permuted_indices,
    )
    return permuted_group, permuted_indices
end

