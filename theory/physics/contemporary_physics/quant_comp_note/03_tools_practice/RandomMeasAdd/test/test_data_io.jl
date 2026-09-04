using RandomMeasAdd
using RandomMeas

N = 8
sites = siteinds("Qubit", N);

# Mirrors meas_indices in test/get_data.py (python 0-based 2D list).
meas_indices_py = [[2], [3], [4], [5]];

test_index = 1

if test_index == 1
    # Overload 1: grouping from the python meas_indices list.
    group_path = joinpath(
        @__DIR__, "data", "aer-shadow",
        "aer-shadow_setting0_settings81_shots1024.npz",
    )
    permuted_order = [1];
    permuted_group, permuted_sites = import_random_group(
        group_path, sites, meas_indices_py, 1, permuted_order
    )
    @show permuted_sites
    @show size(permuted_group.measurements)
elseif test_index == 2
    # Overload 2: grouping derived from meas_indices/group_sizes inside the npz.
    group_path = joinpath(
        @__DIR__, "data", "aer-shadow",
        "aer-shadow_setting0_settings81_shots1024.npz",
    )
    permuted_order = [1];
    permuted_group, permuted_sites = import_random_group(
        group_path, sites, 4, permuted_order
    )
    @show permuted_sites
    @show size(permuted_group.measurements)
end
