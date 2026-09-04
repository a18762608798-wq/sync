include("../src/RandomMeasAdd.jl")
using .RandomMeasAdd
using RandomMeas

# Full-system sites; integer qubit numbers index into this vector.
N = 8
sites = siteinds("Qubit", N)

# Mirrors meas_indices in test/get_data.py (python 0-based 2D list).
# NOTE: the current get_data.py uses singleton groups, so only single-site
# estimators (purity) run against it. Reflect / z_r need an even-size group;
# point group_path at a dataset generated with paired meas_indices
# (e.g. [(2, 5), (3, 4)]) to run branches 3-5.
meas_indices_py = [[2], [3], [4], [5]]
group_path = joinpath(
    @__DIR__, "data", "aer-shadow",
    "aer-shadow_setting0_settings81_shots1024.npz",
)

test_index = 1

if test_index == 1
    @show get_purity_shadow(
        group_path, sites, meas_indices_py, 1, [1]; compute_sem=true,
    )
elseif test_index == 2
    @show get_purity_hamming(
        group_path, sites, meas_indices_py, 1, [1]; compute_sem=true,
    )
elseif test_index == 3
    # Requires an even-size group (e.g. paired meas_indices dataset).
    @show get_reflect_shadow(
        group_path, sites, meas_indices_py, 1, [1, 2]; compute_sem=true,
    )
elseif test_index == 4
    # Requires an even-size group (e.g. paired meas_indices dataset).
    @show get_reflect_hamming(
        group_path, sites, meas_indices_py, 1, [1, 2]; compute_sem=true,
    )
elseif test_index == 5
    # Requires an even-size group (e.g. paired meas_indices dataset).
    @show get_z_r_shadow(
        group_path, sites, meas_indices_py, 1, [1, 2]; compute_sem=true,
    )
end
