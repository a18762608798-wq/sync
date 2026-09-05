using RandomMeasAdd

# 整个 npz（一次 SettingRun）即一个 MeasurementGroup，共 4 个被测 site。
test_index = 1

if test_index == 1
    group_path = joinpath(
        @__DIR__, "data", "aer_independent_pidx_-1",
        "aer_independent_pidx_-1_setting1_settings729_shots1024.npz",
    )
    # 缺省链式导入
    permuted_order = [1, 2, 3, 4]
    permuted_group, permuted_sites, G = import_random_group(
        group_path; permuted_order=permuted_order, is_mitigation=true,
    )
    @show permuted_sites
    @show size(permuted_group.measurements)
    @show isnothing(G)
    println(G)
end

