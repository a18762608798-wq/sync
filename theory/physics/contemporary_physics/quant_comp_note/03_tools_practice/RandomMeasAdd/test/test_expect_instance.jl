include("../src/RandomMeasAdd.jl")
using .RandomMeasAdd
using RandomMeas

# 全系统的 site；整数 qubit 编号用来索引这个向量。
N = 8
sites = siteinds("Qubit", N)

# 对应 test/get_data.py 的 meas_indices（python 从 0 开始的二维列表）；
# 整个 npz（一次 SettingRun）即一个 MeasurementGroup，共 4 个被测 site。
meas_indices_py = [[2], [3], [4], [5]]
permuted_order = [1, 2, 3, 4]
group_path = joinpath(
    @__DIR__, "data", "aer-shadow",
    "aer-shadow_setting0_settings81_shots1024.npz",
)

test_index = 1

if test_index == 1
    @show get_purity_shadow(
        group_path, sites, meas_indices_py, permuted_order; compute_sem=true,
    )
elseif test_index == 2
    @show get_purity_hamming(
        group_path, sites, meas_indices_py, permuted_order; compute_sem=true,
    )
elseif test_index == 3
    @show get_reflect_shadow(
        group_path, sites, meas_indices_py, permuted_order; compute_sem=true,
    )
elseif test_index == 4
    @show get_reflect_hamming(
        group_path, sites, meas_indices_py, permuted_order; compute_sem=true,
    )
elseif test_index == 5
    @show get_z_r_shadow(
        group_path, sites, meas_indices_py, permuted_order; compute_sem=true,
    )
end
