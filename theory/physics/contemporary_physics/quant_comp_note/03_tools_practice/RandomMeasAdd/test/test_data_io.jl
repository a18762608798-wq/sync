using RandomMeasAdd
using RandomMeas

N = 8
sites = siteinds("Qubit", N);

# 整个 npz（一次 SettingRun）即一个 MeasurementGroup，共 4 个被测 site。
test_index = 1

if test_index == 1
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

