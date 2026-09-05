using RandomMeasAdd

# 数据集选择：scheme 取 "independent"/"shared"，pidx 取 1/0/-1；
# shadow 估计子和 purity_hamming 要求各比特独立幺正，只能用 independent 数据；
# reflect_hamming 按 permuted_order 下的相邻配对算 swap，shared 数据正好对应
pidx = -1
permuted_order = [1, 2, 3, 4]
run_tag = "setting1_settings729_shots1024"

test_indices = collect(1:6)

if 1 in test_indices
    scheme = "independent"
    group_path = joinpath(
        @__DIR__, "data", "aer_$(scheme)_pidx_$(pidx)",
        "aer_$(scheme)_pidx_$(pidx)_$(run_tag).npz",
    )
    @show get_purity_shadow(
        group_path; permuted_order=permuted_order, is_compute_sem=true, is_show_progress=true,
    )
end
if 2 in test_indices
    scheme = "independent"
    group_path = joinpath(
        @__DIR__, "data", "aer_$(scheme)_pidx_$(pidx)",
        "aer_$(scheme)_pidx_$(pidx)_$(run_tag).npz",
    )
    @show get_purity_hamming(
        group_path; permuted_order=permuted_order, is_compute_sem=true, is_show_progress=true,
    )
end
if 3 in test_indices
    scheme = "independent"
    group_path = joinpath(
        @__DIR__, "data", "aer_$(scheme)_pidx_$(pidx)",
        "aer_$(scheme)_pidx_$(pidx)_$(run_tag).npz",
    )
    @show get_reflect_shadow(
        group_path; permuted_order=permuted_order, is_compute_sem=true, is_show_progress=true,
    )
end
if 4 in test_indices
    scheme = "shared"
    group_path = joinpath(
        @__DIR__, "data", "aer_$(scheme)_pidx_$(pidx)",
        "aer_$(scheme)_pidx_$(pidx)_$(run_tag).npz",
    )
    @show get_reflect_hamming(
        group_path; permuted_order=permuted_order, is_compute_sem=true, is_show_progress=true,
    )
end
if 5 in test_indices
    scheme = "independent"
    group_path = joinpath(
        @__DIR__, "data", "aer_$(scheme)_pidx_$(pidx)",
        "aer_$(scheme)_pidx_$(pidx)_$(run_tag).npz",
    )
    # NOTE: 这里对permted_order的 odd 和 even 相间要求已经被在get_data的时候考虑.
    @show get_z_r_shadow(
        group_path; permuted_order=permuted_order, is_compute_sem=true, is_show_progress=true,
    )
end
if 6 in test_indices
    scheme = "shared"
    group_path = joinpath(
        @__DIR__, "data", "aer_$(scheme)_pidx_$(pidx)",
        "aer_$(scheme)_pidx_$(pidx)_$(run_tag).npz",
    )
    @show get_z_r_hamming(
        group_path; permuted_order=permuted_order, is_compute_sem=true, is_show_progress=true,
    )
end




