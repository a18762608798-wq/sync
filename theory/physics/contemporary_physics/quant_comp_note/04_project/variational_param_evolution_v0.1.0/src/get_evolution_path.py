def get_bezier_value(p0, p1, pc, tr):
    p_value = (1 - tr) ** 2 * p0 + 2 * tr * (1 - tr) * pc + tr**2 * p1
    return p_value


def get_evolution_path(start, end, control, Δts, decompose_points):
    points_length = len(decompose_points)
    Δt_length = len(Δts)
    assert Δt_length == points_length, (
        "The length of Δts must be equal with the length of decompose_points."
    )
    assert all(0 <= dp <= 1 for dp in decompose_points), (
        "All decompose_points must be in the interval [0, 1]."
    )
    assert all(Δt > 0 for Δt in Δts), "All Δts must be positive."
    s0, δ0 = start
    s1, δ1 = end
    sc, δc = control
    T = sum(Δts)
    # get s_ls and δ_ls
    path = []
    t = 0
    for Δt_idx in range(Δt_length):
        decompose_point = decompose_points[Δt_idx]
        Δt = Δts[Δt_idx]
        t += Δt * decompose_point
        tr = t / T
        s = get_bezier_value(s0, s1, sc, tr)
        δ = get_bezier_value(δ0, δ1, δc, tr)
        path.append((s, δ))
        t += Δt * (1 - decompose_point)
    return path
