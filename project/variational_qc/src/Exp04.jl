# Parent module for the exp04 task-local implementation.
# Load order: Shared01, Exp02 (read-only
# observable kernels), then Exp04.

module Exp04

using LinearAlgebra
using Random
using Optim
using NPZ, JSON3
using Shared01: H_DEF_ID  # provenance only; load Shared01 first
using Exp02: zz_correlators, structure_factor, string_order, z_tilde  # read-only kernels (D09)

export psi_triv, psi_topo, psi_afm, LEG_LABELS, psi_init,
       AnsatzMeta, build_meta, nparams, apply_circuit!, apply_occ!, occ_layout,
       bond_bases, apply_bond_vec!, prim_unitary,
       LegStep, PointResult, run_point, run_leg, run_leg_global, energy_of, pshift_gradient,
       adjoint_gradient!, GradWork, make_gradwork, bond_schedule,
       expect_ztot, overlap_xbar, overlap_reflect,
       MASTER_SEED, N_GLOBAL, TOP_K, G_TOL, X_TOL, F_TOL, MAX_ITERS,
       OPTIMIZATION_PROTOCOL, MAX_GLOBAL_ATTEMPTS, MAX_REFINE_CALLS,
       STAG_WINDOW, STAG_TOL, STAG_E_TOL,
       save_line, completed_lines, assemble_S06_S03,
       build_D09, D09_NPZ_NAME,
       PHASE_TRIV, PHASE_TOPO, PHASE_AFM,
       SCHEMA, DELTAS, S_GRID, THETA_MAX,
       LINE_ID, S06_NPZ_NAME, S03_NPZ_NAME, MANIFEST_NAME

include("Exp04/InitStates.jl")
include("Exp04/Ansatz.jl")
include("Exp04/VQELoop.jl")
include("Exp04/Store.jl")
include("Exp04/D09.jl")

end # module
