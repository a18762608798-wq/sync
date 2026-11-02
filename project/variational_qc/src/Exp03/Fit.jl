# Least-squares fit for exp03 D02c (spec PRE-004).
# Model: Δ_sec(L) = a + b/L + c/L², i.e. y = a + b·x + c·x² with x = 1/L.
# Pure kernel, no I/O.

"""Least-squares coefficients `(a,b,c)` of `y = a + b·x + c·x²`."""
function quadratic_fit(xs::AbstractVector, ys::AbstractVector)
    length(xs) == length(ys) || throw(ArgumentError("xs/ys length mismatch"))
    n = length(xs)
    n ≥ 3 || throw(ArgumentError("quadratic_fit needs at least three points"))
    length(unique(xs)) == n || throw(ArgumentError("xs must be distinct"))

    s0 = float(n)
    s1 = sum(xs)
    s2 = sum(x -> x^2, xs)
    s3 = sum(x -> x^3, xs)
    s4 = sum(x -> x^4, xs)
    t0 = sum(ys)
    t1 = sum(xs .* ys)
    t2 = sum(xs .^ 2 .* ys)

    normal = [s0 s1 s2; s1 s2 s3; s2 s3 s4]
    rhs = [t0, t1, t2]
    coef = normal \ rhs
    return (a = coef[1], b = coef[2], c = coef[3])
end
