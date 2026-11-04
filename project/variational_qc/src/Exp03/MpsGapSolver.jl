# CPU MPS/DMRG extension for exp03 (spec PRE-005, PRE-006; plan §7).
# The ED path remains the exact L_ED solver; this file is deliberately
# independent and writes no production data by itself.
#
# H(s,delta) is mapped from docs/experiment-notes/H.md to ITensor S=1/2 sites:
#   XX + YY = 2 (S+ S- + S- S+),   ZZ = 4 Sz Sz.
# The P=-2 sector is selected with a penalty Hamiltonian
#   H_pen = H + lambda_S Sz^2 + lambda_X (1 - Xbar),
# followed by explicit symmetry checks.  The energy reported to D02 is always
# recomputed from the original H, never from H_pen.

const MPS_METHOD = "mps-dmrg"
const MPS_PENALTY_SZ = 100.0
const MPS_PENALTY_X = 50.0
const MPS_SYM_TOL = 1e-3
const MPS_ENERGY_DRIFT_TOL = 1e-8
const MPS_TRUNC_TOL = 1e-8
const MPS_CHI_GAP_TOL = 1e-3
const MPS_ED_GAP_TOL = 1e-6
const MPS_L26_L28_GAP_TOL = 1e-3
const MPS_EXCITED_WEIGHT = 1000.0
const MPS_SWEEPS_GROUND = 20          # minimum ground-state sweeps
const MPS_SWEEPS_GROUND_MAX = 120      # cap; observer stops once energy drift < stop tol
const MPS_SWEEPS_EXCITED = 30          # minimum excited-state sweeps
const MPS_SWEEPS_EXCITED_MAX = 120     # cap; observer stops once energy drift < stop tol
const MPS_SWEEP_STOP_TOL = 1e-10
const MPS_EIGSOLVE_KRYLOVDIM = 16
const MPS_EIGSOLVE_MAXITER = 4
const MPS_EIGSOLVE_TOL = 1e-14
const MPS_INITIAL_CHI = 128
const MPS_NSTATES_INITIAL = 2
const MPS_NSTATES_MAX = 8
const MPS_CUTOFF = 1e-13
const MPS_NOISE_GROUND = [1e-6, 1e-7, 1e-8, 1e-9, 0.0]
const MPS_NOISE_EXCITED = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 0.0]

struct MpsDMRGParams
    chi::Int
    nsweeps_ground::Int
    nsweeps_ground_max::Int
    nsweeps_excited::Int
    nsweeps_excited_max::Int
    cutoff::Float64
    noise_ground::Vector{Float64}
    noise_excited::Vector{Float64}
    penalty_sz::Float64
    penalty_x::Float64
    nstates_initial::Int
    nstates_max::Int
    excited_weight::Float64
    sector_tol::Float64
    energy_drift_tol::Float64
    trunc_tol::Float64
    sweep_stop_tol::Float64
    eigsolve_krylovdim::Int
    eigsolve_maxiter::Int
    eigsolve_tol::Float64
    seed::Int
end

function mps_params(chi::Integer; nsweeps_ground::Integer=MPS_SWEEPS_GROUND,
                    nsweeps_ground_max::Integer=MPS_SWEEPS_GROUND_MAX,
                    nsweeps_excited::Integer=MPS_SWEEPS_EXCITED,
                    nsweeps_excited_max::Integer=MPS_SWEEPS_EXCITED_MAX,
                    cutoff::Real=MPS_CUTOFF,
                    noise_ground::AbstractVector{<:Real}=MPS_NOISE_GROUND,
                    noise_excited::AbstractVector{<:Real}=MPS_NOISE_EXCITED,
                    penalty_sz::Real=MPS_PENALTY_SZ,
                    penalty_x::Real=MPS_PENALTY_X,
                    nstates_initial::Integer=MPS_NSTATES_INITIAL,
                    nstates_max::Integer=MPS_NSTATES_MAX,
                    excited_weight::Real=MPS_EXCITED_WEIGHT,
                    sector_tol::Real=MPS_SYM_TOL,
                    energy_drift_tol::Real=MPS_ENERGY_DRIFT_TOL,
                    trunc_tol::Real=MPS_TRUNC_TOL,
                    sweep_stop_tol::Real=MPS_SWEEP_STOP_TOL,
                    eigsolve_krylovdim::Integer=MPS_EIGSOLVE_KRYLOVDIM,
                    eigsolve_maxiter::Integer=MPS_EIGSOLVE_MAXITER,
                    eigsolve_tol::Real=MPS_EIGSOLVE_TOL,
                    seed::Integer=1234)
    chi ≥ 2 || throw(ArgumentError("chi must be at least 2, got $chi"))
    nstates_initial ≥ 2 || throw(ArgumentError("nstates_initial must be at least 2"))
    nstates_max ≥ nstates_initial || throw(ArgumentError("nstates_max < nstates_initial"))
    nsweeps_ground ≥ 2 && nsweeps_excited ≥ 2 ||
        throw(ArgumentError("nsweeps must be at least 2"))
    nsweeps_ground_max ≥ nsweeps_ground ||
        throw(ArgumentError("nsweeps_ground_max < nsweeps_ground"))
    nsweeps_excited_max ≥ nsweeps_excited ||
        throw(ArgumentError("nsweeps_excited_max < nsweeps_excited"))
    eigsolve_krylovdim ≥ 3 && eigsolve_maxiter ≥ 1 ||
        throw(ArgumentError("invalid local eigensolver dimensions"))
    all(x -> isfinite(x) && x > 0,
        (cutoff, penalty_sz, penalty_x, excited_weight, sector_tol,
         energy_drift_tol, trunc_tol, sweep_stop_tol, eigsolve_tol)) ||
        throw(ArgumentError("tolerances and penalties must be finite and positive"))
    return MpsDMRGParams(Int(chi), Int(nsweeps_ground), Int(nsweeps_ground_max),
                         Int(nsweeps_excited), Int(nsweeps_excited_max), Float64(cutoff),
                         Float64.(collect(noise_ground)), Float64.(collect(noise_excited)),
                         Float64(penalty_sz), Float64(penalty_x), Int(nstates_initial),
                         Int(nstates_max), Float64(excited_weight), Float64(sector_tol),
                         Float64(energy_drift_tol), Float64(trunc_tol),
                         Float64(sweep_stop_tol), Int(eigsolve_krylovdim),
                         Int(eigsolve_maxiter), Float64(eigsolve_tol), Int(seed))
end

struct MpsStateResult
    index::Int
    E_pen::Float64
    E::Float64
    sz2::Float64
    xbar::Float64
    reflection::Float64
    max_bond_dim::Int
    accepted::Bool
    sweep_ok::Bool
    last_energy_change::Float64
    max_trunc_error::Float64
    n_sweeps::Int
    sweep_energies::Vector{Float64}
    trunc_errors::Vector{Float64}
end

struct MpsPointResult
    L::Int
    s::Float64
    delta::Float64
    E0::Float64
    E1::Float64
    delta_gap::Float64
    chi::Int
    chi_ladder::Vector{Int}
    nstates::Int
    n_accepted::Int
    sz2_0::Float64
    xbar_0::Float64
    reflection_0::Float64
    sz2_1::Float64
    xbar_1::Float64
    reflection_1::Float64
    max_bond_dim::Int
    last_energy_change::Float64
    max_trunc_error::Float64
    sweep_ok::Bool
    sector_ok::Bool
    overlap_min_eig::Float64
    wall_seconds::Float64
    peak_rss_mib::Float64
    states::Vector{MpsStateResult}
    method::String
    params::MpsDMRGParams
end

"""Potential DMRG ladder capped at `chi`, used for every state in a point."""
function mps_chi_ladder(chi::Integer)
    chi = Int(chi)
    chi ≥ 2 || throw(ArgumentError("chi must be at least 2, got $chi"))
    out = Int[]
    x = min(MPS_INITIAL_CHI, chi)
    while x < chi
        push!(out, x)
        x *= 2
    end
    push!(out, chi)
    return unique(out)
end

"""Peak resident set size of this Julia process, in MiB (Linux /proc)."""
function peak_rss_mib()
    path = "/proc/self/status"
    isfile(path) || return NaN
    for line in eachline(path)
        startswith(line, "VmHWM:") || continue
        fields = split(line)
        length(fields) ≥ 2 || return NaN
        return parse(Float64, fields[2]) / 1024
    end
    return NaN
end

"""Build the MPS Hamiltonian and the two symmetry-penalty MPOs."""
function mps_system(L::Integer, s::Real; delta::Real=DELTA_FIXED,
                    penalty_sz::Real=MPS_PENALTY_SZ,
                    penalty_x::Real=MPS_PENALTY_X)
    iseven(L) || throw(ArgumentError("L must be even, got $L"))
    2 ≤ L || throw(ArgumentError("L must be at least 2, got $L"))
    0 ≤ s ≤ 1 || throw(ArgumentError("s must lie in [0,1], got $s"))
    sites = siteinds("S=1/2", Int(L))
    jxx = exp(-Float64(delta))
    jz = exp(Float64(delta))
    os = OpSum()
    for (a, b) in odd_bonds(L)
        w = 1.0 - Float64(s)
        os += 2 * jxx * w, "S+", a, "S-", b
        os += 2 * jxx * w, "S-", a, "S+", b
        os += 4 * jz * w, "Sz", a, "Sz", b
    end
    for (a, b) in even_bonds(L)
        w = Float64(s)
        os += 2 * jxx * w, "S+", a, "S-", b
        os += 2 * jxx * w, "S-", a, "S+", b
        os += 4 * jz * w, "Sz", a, "Sz", b
    end
    H = MPO(os, sites)

    os_sz = OpSum()
    for i in 1:L
        os_sz += 1.0, "Sz", i
    end
    Sztot = MPO(os_sz, sites)
    Sz2 = apply(Sztot, Sztot)
    Xbar = MPO(sites, fill("X", Int(L)))
    Id = MPO(sites, "Id")
    Hpen = H + Float64(penalty_sz) * Sz2 + Float64(penalty_x) * (Id - Xbar)
    return (sites=sites, H=H, Hpen=Hpen, Sztot=Sztot, Sz2=Sz2,
            Xbar=Xbar, Id=Id)
end

"""Reflect the physical sites of an MPS, swapping auxiliary bonds.

This avoids constructing a reflection MPO.  The returned MPS is in the site-reversed
order and has the same physical indices in reversed positions, so
`inner(psi, reflect_mps(psi, sites))` is <psi|R|psi>.
"""
function reflect_mps(psi::MPS, sites)
    L = length(psi)
    length(sites) == L || throw(ArgumentError("site count does not match MPS length"))
    Ts = ITensor[]
    for j in 1:L
        k = L + 1 - j
        A = psi[k]
        lold = linkind(psi, k - 1)
        rold = linkind(psi, k)
        if j == 1
            lold === nothing && throw(ErrorException("left boundary is missing a link"))
            A = ITensors.permute(A, (sites[k], lold))
        elseif j == L
            rold === nothing && throw(ErrorException("right boundary is missing a link"))
            A = ITensors.permute(A, (rold, sites[k]))
        else
            (lold === nothing || rold === nothing) &&
                throw(ErrorException("interior site has a missing link"))
            A = ITensors.permute(A, (rold, sites[k], lold))
        end
        A = ITensors.replaceind(A, sites[k], sites[j])
        push!(Ts, A)
    end
    return MPS(Ts)
end

function _mps_expect(psi::MPS, O)
    den = real(inner(psi, psi))
    den > 0 || throw(ErrorException("MPS has non-positive norm"))
    return real(inner(psi', O, psi)) / den
end

function _mps_reflection(psi::MPS, sites)
    den = real(inner(psi, psi))
    den > 0 || throw(ErrorException("MPS has non-positive norm"))
    return real(inner(psi, reflect_mps(psi, sites))) / den
end

function _state_result(index::Int, E_pen::Real, psi::MPS, sys,
                       params::MpsDMRGParams, observer)
    E = _mps_expect(psi, sys.H)
    sz2 = _mps_expect(psi, sys.Sz2)
    xbar = _mps_expect(psi, sys.Xbar)
    refl = _mps_reflection(psi, sys.sites)
    ev = Float64.(collect(ITensorMPS.energies(observer)))
    tr = Float64.(collect(ITensorMPS.truncerrors(observer)))
    last_change = length(ev) ≥ 2 ? abs(ev[end] - ev[end-1]) : Inf
    max_trunc = isempty(tr) ? Inf : maximum(tr)
    sweep_ok = length(ev) ≥ 2 && last_change < params.energy_drift_tol &&
               isfinite(max_trunc) && max_trunc < params.trunc_tol
    accepted = abs(sz2) < params.sector_tol && abs(xbar - 1) < params.sector_tol &&
               abs(refl - 1) < params.sector_tol
    return MpsStateResult(index, Float64(E_pen), E, sz2, xbar, refl,
                          maximum(linkdims(psi)), accepted, sweep_ok,
                          last_change, max_trunc, length(ev), ev, tr)
end

"""Run DMRG for the lowest two P=-2 states at (L,s), using one chi cap.

The penalty Hamiltonian is used only to generate candidate states.  The final
E0/E1 are the lowest two eigenvalues of the original H in the span of candidates
that pass the S_z=0, Xbar=+1, R=+1 checks.  If fewer than two such states are
found, throw rather than returning a sector-contaminated point.

The reported `sweep_ok` is the conjunction of the selected states' last-two-sweep
energy drift and truncation error checks.  Cross-chi convergence is evaluated by
the caller/test script (spec INV-005).
"""
function solve_gap_mps(L::Integer, s::Real, chi::Integer;
                       delta::Real=DELTA_FIXED,
                       params::MpsDMRGParams=mps_params(chi))
    params.chi == Int(chi) ||
        throw(ArgumentError("params.chi=$(params.chi) does not match chi=$chi"))
    iseven(L) || throw(ArgumentError("L must be even, got $L"))
    t0 = time()
    Random.seed!(params.seed)
    sys = mps_system(L, s; delta=delta, penalty_sz=params.penalty_sz,
                     penalty_x=params.penalty_x)
    ladder = mps_chi_ladder(chi)
    states = MpsStateResult[]
    prev = MPS[]

    while length(prev) < params.nstates_max
        k = length(prev) + 1
        # A Néel product has Z_tot=0 and is a deterministic, symmetry-neutral
        # starting point.  The penalties and DMRG then select the target Xbar
        # and reflection sectors.
        init = [isodd(n) ? "Up" : "Dn" for n in 1:L]
        psi = MPS(sys.sites, init)
        nsweeps = k == 1 ? params.nsweeps_ground_max : params.nsweeps_excited_max
        min_sweeps = k == 1 ? params.nsweeps_ground : params.nsweeps_excited
        stop_tol = params.sweep_stop_tol
        observer = ITensorMPS.DMRGObserver(; energy_tol=stop_tol, minsweeps=min_sweeps)
        if isempty(prev)
            E_pen, psi = ITensorMPS.dmrg(sys.Hpen, psi;
                                         nsweeps=nsweeps,
                                         maxdim=ladder,
                                         cutoff=params.cutoff,
                                         noise=k == 1 ? params.noise_ground :
                                                       params.noise_excited,
                                         observer=observer,
                                         eigsolve_krylovdim=params.eigsolve_krylovdim,
                                         eigsolve_maxiter=params.eigsolve_maxiter,
                                         eigsolve_tol=params.eigsolve_tol,
                                         outputlevel=0)
        else
            E_pen, psi = ITensorMPS.dmrg(sys.Hpen, prev, psi;
                                         nsweeps=nsweeps,
                                         maxdim=ladder,
                                         cutoff=params.cutoff,
                                         noise=k == 1 ? params.noise_ground :
                                                       params.noise_excited,
                                         weight=params.excited_weight,
                                         observer=observer,
                                         eigsolve_krylovdim=params.eigsolve_krylovdim,
                                         eigsolve_maxiter=params.eigsolve_maxiter,
                                         eigsolve_tol=params.eigsolve_tol,
                                         outputlevel=0)
        end
        push!(prev, psi)
        push!(states, _state_result(k, E_pen, psi, sys, params, observer))
        n_acc = count(st -> st.accepted, states)
        if length(states) ≥ params.nstates_initial && n_acc ≥ 2
            break
        end
    end

    acc_idx = findall(st -> st.accepted, states)
    length(acc_idx) ≥ 2 ||
        throw(ErrorException("MPS found only $(length(acc_idx)) accepted P=-2 states " *
                             "at L=$L s=$(Float64(s)) chi=$chi " *
                             "(need at least two); increase nstates or chi"))
    n = length(acc_idx)
    S = zeros(ComplexF64, n, n)
    Hm = zeros(ComplexF64, n, n)
    Xm = zeros(ComplexF64, n, n)
    Rm = zeros(ComplexF64, n, n)
    Sm = zeros(ComplexF64, n, n)
    for ii in 1:n, jj in 1:n
        a = acc_idx[ii]
        b = acc_idx[jj]
        S[ii, jj] = inner(prev[a], prev[b])
        Hm[ii, jj] = inner(prev[a]', sys.H, prev[b])
        Xm[ii, jj] = inner(prev[a]', sys.Xbar, prev[b])
        Sm[ii, jj] = inner(prev[a]', sys.Sz2, prev[b])
        Rm[ii, jj] = inner(prev[a], reflect_mps(prev[b], sys.sites))
    end
    S = (S + S') / 2
    Hm = (Hm + Hm') / 2
    Xm = (Xm + Xm') / 2
    Sm = (Sm + Sm') / 2
    Rm = (Rm + Rm') / 2
    F = eigen(Hermitian(S))
    min_eig = minimum(real.(F.values))
    min_eig > 1e-10 ||
        throw(ErrorException("candidate MPS overlap is singular at L=$L s=$(Float64(s)) " *
                             "chi=$chi (min eigenvalue $min_eig)"))
    U = F.vectors * Diagonal(1 ./ sqrt.(real.(F.values)))
    Hn = U' * Hm * U
    Xn = U' * Xm * U
    Rn = U' * Rm * U
    Sn = U' * Sm * U
    Hn = (Hn + Hn') / 2
    Xn = (Xn + Xn') / 2
    Rn = (Rn + Rn') / 2
    Sn = (Sn + Sn') / 2
    Fh = eigen(Hermitian(Hn))
    order = sortperm(real.(Fh.values))
    length(order) ≥ 2 || throw(ErrorException("subspace has fewer than two states"))

    metrics = []
    for q in 1:2
        c = Fh.vectors[:, order[q]]
        c = c / norm(c)
        push!(metrics, (E=real(dot(c, Hn * c)),
                        sz2=real(dot(c, Sn * c)),
                        xbar=real(dot(c, Xn * c)),
                        refl=real(dot(c, Rn * c))))
    end
    sector_ok = all(abs(m.sz2) < params.sector_tol &&
                    abs(m.xbar - 1) < params.sector_tol &&
                    abs(m.refl - 1) < params.sector_tol for m in metrics)
    # Subspace eigenvectors can mix every accepted candidate. Earlier rejected
    # candidates must also be converged before their energy ordering is trusted.
    sweep_ok = all(st -> st.sweep_ok, states)
    max_trunc = maximum(st.max_trunc_error for st in states)
    last_change = maximum(st.last_energy_change for st in states)
    maxbond = maximum(st.max_bond_dim for st in states)

    E0 = metrics[1].E
    E1 = metrics[2].E
    E1 ≥ E0 - 1e-10 || throw(ErrorException("subspace energies are not ordered"))
    return MpsPointResult(Int(L), Float64(s), Float64(delta), E0, E1, E1 - E0,
                          Int(chi), ladder, length(states), length(acc_idx),
                          metrics[1].sz2, metrics[1].xbar, metrics[1].refl,
                          metrics[2].sz2, metrics[2].xbar, metrics[2].refl,
                          maxbond, last_change, max_trunc, sweep_ok, sector_ok,
                          min_eig, time() - t0, peak_rss_mib(), states, MPS_METHOD, params)
end

"""Hard validity gate for one MPS point (not a cross-chi convergence claim)."""
function mps_point_valid(r::MpsPointResult; sym_tol::Real=MPS_SYM_TOL,
                         drift_tol::Real=MPS_ENERGY_DRIFT_TOL,
                         trunc_tol::Real=MPS_TRUNC_TOL)
    return isfinite(r.E0) && isfinite(r.E1) && isfinite(r.delta_gap) &&
           r.delta_gap ≥ -1e-12 && r.n_accepted ≥ 2 &&
           r.sweep_ok && r.sector_ok && r.overlap_min_eig > 1e-10 &&
           r.last_energy_change < drift_tol && r.max_trunc_error < trunc_tol &&
           abs(r.sz2_0) < sym_tol && abs(r.xbar_0 - 1) < sym_tol &&
           abs(r.reflection_0 - 1) < sym_tol &&
           abs(r.sz2_1) < sym_tol && abs(r.xbar_1 - 1) < sym_tol &&
           abs(r.reflection_1 - 1) < sym_tol
end

function mps_chi_converged(rlo::MpsPointResult, rhi::MpsPointResult;
                           tol::Real=MPS_CHI_GAP_TOL)
    rlo.L == rhi.L && abs(rlo.s - rhi.s) < 1e-12 ||
        throw(ArgumentError("chi comparison must use the same (L,s)"))
    rhi.chi == 2rlo.chi && rhi.delta == rlo.delta ||
        throw(ArgumentError("chi comparison requires chi/2chi and the same delta"))
    return mps_point_valid(rlo) && mps_point_valid(rhi) &&
           abs(rlo.delta_gap - rhi.delta_gap) < tol
end
