using RandomMeasAdd
using RandomMeas

N = 8
sites = siteinds("Qubit", N);

# 对应 test/get_data.py 的 meas_indices（python 从 0 开始的二维列表）；
# 整个 npz（一次 SettingRun）即一个 MeasurementGroup，共 4 个被测 site。
meas_indices_py = [[2], [3], [4], [5]];

test_index = 1

if test_index == 1
    # 重载 1：用 python 的 meas_indices 列表还原被测 qubit 编号。
    group_path = joinpath(
        @__DIR__, "data", "aer-shadow",
        "aer-shadow_setting0_settings81_shots1024.npz",
    )
    permuted_order = [1, 2, 3, 4];
    permuted_group, permuted_sites = import_random_group(
        group_path, sites, meas_indices_py, permuted_order
    )
    @show permuted_sites
    @show size(permuted_group.measurements)
elseif test_index == 2
    # 重载 2：直接用 npz 自带的 meas_indices 还原被测 qubit 编号。
    group_path = joinpath(
        @__DIR__, "data", "aer-shadow",
        "aer-shadow_setting0_settings81_shots1024.npz",
    )
    permuted_order = [1, 2, 3, 4];
    permuted_group, permuted_sites = import_random_group(
        group_path, sites, permuted_order
    )
    @show permuted_sites
    @show size(permuted_group.measurements)
end

