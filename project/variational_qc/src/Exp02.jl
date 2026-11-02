# Parent module for the exp02 task-local implementation.
# Depends only on Shared01 (S01/S02); the ~Z_R kernel is now local (D01 retired).

module Exp02

using LinearAlgebra
using NPZ, JSON3

export zz_correlators, structure_factor,
       string_order,
       reduced_density_matrix, mirror_operator, z_tilde, ZTildeResult,
       I_SITES, I1_SITES, I2_SITES,
       panel_point, PanelPoint,
       save_row, completed_rows, save_d03, assemble_D04,
       CHUNKS_DIRNAME, ROW_PREFIX, PROGRESS_NAME,
       D03_NAME, D04_NPZ_NAME, MANIFEST_NAME, SCHEMA

include("Exp02/Correlators.jl")
include("Exp02/StringOrder.jl")
include("Exp02/ZTilde.jl")
include("Exp02/Panels.jl")
include("Exp02/Store.jl")

end # module
