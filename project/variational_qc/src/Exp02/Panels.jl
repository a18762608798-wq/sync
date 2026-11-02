# Per-point D04 panel assembly for exp02 (spec POST-002).
# D03/D04a/D04b are stored already normalised (new paper-outline):
#   Ŝ(π) = S(π)/L,  Ô_str = −O_str,  Q = 4/3 − 2Ô_str − (4/3)Ŝ(π).
# ~Z_R uses the local kernel in ZTilde.jl (D01 retired).

struct PanelPoint
    s_hat_pi::Float64
    o_hat_str::Float64
    q_val::Float64
    z_tilde::Float64
end

"""Full (Ŝπ, Ôstr, Q, Zt) tuple for one ground-state vector."""
function panel_point(psi::AbstractVector)
    C = zz_correlators(psi)
    s_hat = structure_factor(C, pi) / 8   # Ŝ(π) = S(π)/L, L = 8
    o_hat = -string_order(psi)            # Ô_str = −O_str
    q_val = 4 / 3 - 2 * o_hat - (4 / 3) * s_hat
    zt = z_tilde(psi).z_tilde
    return PanelPoint(s_hat, o_hat, q_val, zt)
end
