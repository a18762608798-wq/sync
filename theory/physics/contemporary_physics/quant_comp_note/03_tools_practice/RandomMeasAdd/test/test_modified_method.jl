using RandomMeasAdd

# get sub shadows
N = 8
sites = siteinds("Qubit", N)
group_path = joinpath(
    @__DIR__, "data", "aer_independent_pidx_-1",
    "aer_independent_pidx_-1_setting1_settings729_shots1024.npz",
)
sub_group, sub_indices = import_random_group(group_path, sites; permuted_order=[1, 2, 3, 4]);
sub_shadows = get_dense_shadows(sub_group);

test_index = 2

if test_index == 1
    # get expect shadows
    reflect_op = create_reflect_op(sub_indices)
    @show linkdims(reflect_op)
    @show modified_get_expect_shadow(reflect_op, sub_shadows; is_compute_sem=true, is_show_progress=true)
elseif test_index == 2
    reflect_op = create_reflect_op(sub_indices)
    # NOTICE: Which should be equal.
    @show modified_get_expect_shadow(reflect_op, sub_shadows, is_compute_sem=true, is_show_progress=true)
    @show modified_get_trace_moment(sub_shadows, 1; O=reflect_op, is_compute_sem=true, is_show_progress=true)
elseif test_index == 3
    @show modified_get_trace_moment(sub_shadows, 2; is_show_progress=true)
elseif test_index == 4
    @show modified_get_trace_moment(sub_shadows, 2; is_compute_sem=true, is_show_progress=true)
    @show modified_get_purity_shadow(sub_shadows; is_compute_sem=true, is_show_progress=true)
end
