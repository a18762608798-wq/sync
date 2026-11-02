# S01 input gate: basis-convention assertion and schema check.
# Lives in Shared01 because the convention is a property of the S01 dataset,
# not of any single consumer (exp02 and any future reader share it).

# Must equal the S01 manifest entry verbatim; consumers refuse to run otherwise.
const EXPECTED_BASIS_CONVENTION =
    "site m (1-indexed) <-> bit (m-1) of basis index, LSB = site 1; |0> is Z=+1"

"""
    assert_s01_gate(manifest, expected_basis)

Refuse to run on missing/wrong-schema S01 or a mismatched basis convention
(no silent adaptation). Returns the degenerate index set on success.
"""
function assert_s01_gate(manifest, expected_basis::AbstractString)
    manifest["schema"] == "shared01/v1" || throw(ErrorException("unexpected S01 schema"))
    manifest["basis_convention"] == expected_basis ||
        throw(ErrorException("S01 basis convention mismatch; refusing silent adaptation"))
    return Set{Tuple{Int,Int}}([(Int(p["grid_index"][1]), Int(p["grid_index"][2]))
                                for p in manifest["degenerate_points"]])
end
