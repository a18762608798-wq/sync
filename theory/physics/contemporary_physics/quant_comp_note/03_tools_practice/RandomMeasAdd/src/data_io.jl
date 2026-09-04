# ---------------------
# Import one group from qmeas.random output according to permuted order.
# ---------------------

"""
Import a single measurement group from a qmeas.random npz file.

The npz file stores ALL groups concatenated along the measured-qubit
dimension, with `meas_indices` (flattened, python 0-based) and `group_sizes`
recording the grouping. This function slices out group `group_idx`
(Julia 1-based), converts qubit indices to Julia 1-based `site_indices`
(+1), and applies `permuted_order` consistently to results, settings and
site indices.

Arguments
- filepath::String: path to one .npz file produced by qmeas.random.
- sites: full-system site indices (`siteinds("Qubit", N)`); integer qubit
  numbers index into this vector.
- meas_indices_py: meas_indices from python (0-based 2D list, e.g. `[[2,5],[3,4]]`
  parsed from the summary json). In Julia this arrives as a `Vector` of
  vectors or an `AbstractVector` of iterables; each inner element is 0-based.
- group_idx::Int: which group to import (Julia 1-based).
- permuted_order: permutation vector (Julia 1-based) for the sites within the group.

Returns
- permuted_group::MeasurementGroup
- permuted_sites: permuted site Index objects for the group.
"""
function import_random_group(
    filepath::String, sites, meas_indices_py, group_idx::Int, permuted_order
)
    groups_py = [collect(Int, g) for g in meas_indices_py]
    @assert 1 <= group_idx <= length(groups_py) "group_idx out of range"
    # python 0-based -> julia 1-based qubit numbers
    qubits_jl = groups_py[group_idx] .+ 1
    site_indices = sites[qubits_jl]
    # column range of this group in the flattened n_meas dimension
    offset = group_idx == 1 ? 0 : sum(length.(groups_py[1:(group_idx-1)]))

    cols = (offset+1):(offset+length(site_indices))

    group_data = npzread(filepath)
    meas_res = 2 .- Int64.(group_data["measurement_results"][:, :, cols])
    settings = ComplexF64.(group_data["measurement_settings"][:, cols, :, :])

    permuted_indices = site_indices[permuted_order]
    permuted_meas_res = meas_res[:, :, permuted_order]
    permuted_settings = settings[:, permuted_order, :, :]
    permuted_group = MeasurementGroup(
        permuted_meas_res, permuted_settings, permuted_indices
    )
    return permuted_group, permuted_indices
end

"""
Convenience overload deriving the grouping from the npz file itself
(`meas_indices` + `group_sizes` keys) instead of an external python list.

Arguments
- filepath::String, sites (full-system siteinds), group_idx::Int
  (Julia 1-based), permuted_order.
"""
function import_random_group(filepath::String, sites, group_idx::Int, permuted_order)
    group_data = npzread(filepath)
    flat = vec(Int64.(group_data["meas_indices"])) # python 0-based
    sizes = vec(Int64.(group_data["group_sizes"]))
    @assert sum(sizes) == length(flat) "meas_indices/group_sizes mismatch"
    @assert 1 <= group_idx <= length(sizes) "group_idx out of range"
    offset = sum(sizes[1:(group_idx-1)]; init=0)
    # python 0-based -> julia 1-based qubit numbers, index into sites
    qubits_jl = flat[(offset+1):(offset+sizes[group_idx])] .+ 1
    site_indices = sites[qubits_jl]
    cols = (offset+1):(offset+sizes[group_idx])

    meas_res = 2 .- Int64.(group_data["measurement_results"][:, :, cols])
    settings = ComplexF64.(group_data["measurement_settings"][:, cols, :, :])

    permuted_indices = site_indices[permuted_order]
    permuted_group = MeasurementGroup(
        meas_res[:, :, permuted_order],
        settings[:, permuted_order, :, :],
        permuted_indices,
    )
    return permuted_group, permuted_indices
end



