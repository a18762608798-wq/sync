# Parent module for the exp03 task-local implementation.
# Load order: Shared01 (read-only semantic reuse), then Exp03.

module Exp03

using LinearAlgebra
using SparseArrays
using Arpack
using NPZ, JSON3, Dates
using ITensors, ITensorMPS
using Random
using SHA
using Shared01: odd_bonds, even_bonds, H_DEF_ID  # read-only; load Shared01 first

export SectorBasisData, sector_basis, sector_hamiltonian,
       flip_all, reflect_bits, canonical_key,
       EXPECTED_BASIS_CONVENTION, H_DEF_ID, MAX_L,
       GapResult, solve_gap, DELTA_FIXED, s_grid_points,
       ARPACK_TOL, RESID_TOL, ARPACK_MAXITER, ARPACK_NCV,
       quadratic_fit,
       save_chunk, completed_chunks, assemble_D02, chunk_id, chunk_exists,
       SCHEMA, LS, BLOCK, D02_NPZ_NAME, MANIFEST_NAME,
       GAP_MIN_TOL, FIT_TOL,
       MpsDMRGParams, MpsStateResult, MpsPointResult, mps_params,
       mps_chi_ladder, mps_system, reflect_mps, solve_gap_mps,
       mps_point_valid, mps_chi_converged, peak_rss_mib,
       MPS_METHOD, MPS_PENALTY_SZ, MPS_PENALTY_X, MPS_SYM_TOL,
       MPS_ENERGY_DRIFT_TOL, MPS_TRUNC_TOL, MPS_CHI_GAP_TOL, MPS_ED_GAP_TOL,
       MPS_L26_L28_GAP_TOL, MPS_SWEEPS_GROUND, MPS_SWEEPS_GROUND_MAX,
       MPS_SWEEPS_EXCITED,
       MPS_SWEEPS_EXCITED_MAX, MPS_SWEEP_STOP_TOL,
       MPS_SCHEMA, MPS_CHUNKS_DIRNAME, MPS_BLOCK,
       mps_chunk_id, mps_chunk_path, mps_detail_path, mps_chunk_exists,
       mps_point_dict, save_mps_point_json, save_mps_chunk, load_mps_chunk,
       mps_completed_chunks, save_capacity_trial, save_capacity_summary,
       mps_params_dict, mps_runtime, mps_source_fingerprint,
       mps_record_valid, mps_record_matches, mps_pair_valid, save_mps_chunk_records,
       PAPER_LS, ED_LS

include("Exp03/SectorBasis.jl")
include("Exp03/GapSolver.jl")
include("Exp03/Fit.jl")
include("Exp03/Store.jl")
include("Exp03/MpsGapSolver.jl")
include("Exp03/MpsStore.jl")

end # module
