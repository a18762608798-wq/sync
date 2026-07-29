function get_spectrum(
    get_H::Function,
    eigvals::Int,
    param_lists...;
    sparse=true,
    sortby=real,
    rev=false,
)
    n = length(first(param_lists))
    @assert all(length(xs) == n for xs in param_lists)

    spectrum = Matrix{Float64}(undef, n, eigvals)
    state_group = Matrix{Qobj}(undef, n, eigvals)

    if sparse

        for (idx, params) in enumerate(zip(param_lists...))
            H = get_H(params...)

            Es, states, _ = eigsolve(
                H;
                eigvals=eigvals,
                sortby=sortby,
                rev=rev,
            )

            spectrum[idx, :] .= real.(Es)
            state_group[idx, :] .= states
        end
    else

        for (idx, params) in enumerate(zip(param_lists...))
            H = get_H(params...)

            Es, states, _ = eigenstates(
                H;
                sortby=sortby,
            )

            spectrum[idx, :] .= real.(Es)[1:eigvals]
            state_group[idx, :] .= states[1:eigvals]
        end

    end

    return spectrum, state_group
end
