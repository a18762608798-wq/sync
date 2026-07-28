include("get_ssh_ZR.jl")
using ProgressMeter
using Roots
using NPZ

QUBIT_NUMS = [4i + 4 for i = 1:3]
S_POINT_NUM = 3

function save_phase_boundary(path::String)
    Qgroup_num = length(QUBIT_NUMS)
    δ_boundaries = zeros(Float64, Qgroup_num)
    s_points = zeros(Float64, Qgroup_num, 2S_POINT_NUM)
    s_boundaries = zeros(Float64, Qgroup_num, 2S_POINT_NUM)
    @showprogress Threads.@threads for group_idx = 1:Qgroup_num
        # get δ boundary
        δ_boundary = find_zero(s -> get_ssh_ZR(QUBIT_NUMS[group_idx], s, 1) - 0.0, (0.5, 0.8); xatol=1e-2)
        δ_boundaries[group_idx] = δ_boundary
        # get s boundary
        s_group = append!(
            collect(range(0.1, δ_boundary - 0.1; length=S_POINT_NUM)),
            collect(range(δ_boundary + 0.1, 1 - 0.1; length=S_POINT_NUM)),
        )
        s_points[group_idx, :] = s_group
        for s_idx = 1:S_POINT_NUM
            s_boundaries[group_idx, s_idx] = find_zero(
                δ -> get_ssh_ZR(QUBIT_NUMS[group_idx], s_group[s_idx], δ) - 0.5,
                (0, 1);
                xatol=1e-2
            )
        end
        for s_idx = (S_POINT_NUM+1):2S_POINT_NUM
            s_boundaries[group_idx, s_idx] = find_zero(
                δ -> get_ssh_ZR(QUBIT_NUMS[group_idx], s_group[s_idx], δ) + 0.5,
                (0, 1);
                xatol=1e-2
            )
        end
    end
    npzwrite(
        path,
        Dict(
            "QUBIT_NUMS" => QUBIT_NUMS,
            "s_points" => s_points,
            "delta_boundaries" => δ_boundaries,
            "s_boundaries" => s_boundaries,
        ),
    )
end


if abspath(PROGRAM_FILE) == @__FILE__
    path = joinpath(@__DIR__, "./data/boundary.npz")
    save_phase_boundary(path)
end

