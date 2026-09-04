# ---------------------
# 求 jackknife 的 leave-one-out 值
# ---------------------

"""
对随机幺正的所有 k 元置换求 trace-product 平均，再对测量指标求平均。

参数
- shadows::Array{<:AbstractShadow, 2}：(n_ru, n_m) 的 shadow 数组，
  n_ru 为随机幺正个数，n_m 为每个幺正下的测量次数。
- k::Int：置换大小（只支持 1 或 2）。

关键词参数
- O::Union{Nothing, MPO}=nothing：传给 get_trace_product 的 MPO 算符
  （仅 k == 1 时允许）。
- show_progress::Bool=true：是否显示进度。

返回
- Array{Float64}，长度 choose(n_ru, k)：每个 k 置换在测量笛卡尔积上
  平均后的 trace-product 均值。
"""
function get_comb_avgs_shadow(
    shadows::Array{<:AbstractShadow, 2},
    k::Int;
    O::Union{Nothing, MPO}=nothing,
    show_progress=true,
)
    @assert (k == 2 && isnothing(O)) || (k == 1) "O must be nothing for k=2, and k in the range of [1, 2]"

    # 预先枚举置换和测量笛卡尔积
    n_ru, n_m = size(shadows)
    combs = collect(combinations(1:n_ru, k))
    cprod = collect(CartesianIndices(ntuple(_ -> 1:n_m, k)))
    combs_num = length(combs)

    # 每个置换对测量求平均
    comb_avgs = zeros(Float64, combs_num)
    @showprogress desc="Combinations Processing..." enabled=show_progress @threads for pidx in eachindex(combs)
        r = combs[pidx]
        ssum = 0.0
        for m in cprod
            ssum += real(get_trace_product((shadows[r[i], m[i]] for i in 1:k)...; O))
        end
        comb_avgs[pidx] = ssum / length(cprod)
    end

    return comb_avgs
end

"""
get_combs_loos_shadow(n_ru, combs, avgs)

由置换平均算 leave-one-out 的 jackknife 估计。

参数
- n_ru::Int64：随机幺正总数。
- combs::Vector{Vector{Int64}}：幺正指标的 k 元组合向量。
- avgs::Vector{Float64}：每个组合的 trace-product 平均。

返回
- loos::Vector{Float64}：每个随机幺正的 leave-one-out jackknife 估计。

说明
幺正 i 的 leave-one-out 值，等于所有不含 i 的组合的置换平均之均值。
"""
function get_combs_loos_shadow(
    n_ru::Int64,
    combs::Vector{Vector{Int64}},
    avgs::Vector{Float64},
)
    k = length(first(combs))
    ssum = sum(avgs) # 平均之和
    incident_threads = zeros(Float64, n_ru, Threads.maxthreadid()) # 含每个随机幺正的组合之和
    # 求 leave-one-out。
    @threads for idx in eachindex(combs)
        tid = threadid()
        incident_indices = combs[idx] # 记下被关联的项。
        incident_val = avgs[idx]
        for index in incident_indices 
            incident_threads[index, tid] += incident_val
        end
    end
    incidents = vec(sum(incident_threads; dims=2))
    denom = binomial(n_ru - 1, k)
    loos = (ssum .- incidents) ./ denom # 得 loos

    return loos
end

"""
由 shadow 数据估计二阶矩（纯度），并对随机幺正算 jackknife 估计。

参数
- shadows::Array{<:AbstractShadow, 2}：(n_ru, n_m) 的 shadow 数据。

关键词参数
- compute_renyi::Bool=false：为 true 时返回 Rényi-2 熵估计
  （对平均纯度取 log2）；否则返回纯度。
- show_progress::Bool=true：置换平均时是否显示进度。

返回
- θ：标量估计（纯度或 Rényi-2，取决于 compute_renyi）。
- loos::Vector{Float64}：每个随机幺正的 leave-one-out jackknife 估计。
"""
function get_purity_loos_shadow(
    shadows::Array{<:AbstractShadow, 2}; compute_renyi::Bool=false, show_progress::Bool=true
)
    n_ru, n_m = size(shadows)
    @assert n_ru ≥ 3 "At least 3 random unitaries are required for 2-moment estimation."
    # 预先枚举置换
    combs = collect(combinations(1:n_ru, 2))

    # 每个置换对测量求平均
    comb_avgs = get_comb_avgs_shadow(shadows, 2; show_progress=show_progress)

    # 定义平均泛函
    avgfun(x) = compute_renyi ? (1 / (1 - 2)) * log2(mean(x)) : mean(x)

    θ = avgfun(comb_avgs)

    # jackknife loo 分组：不含幺正 i 的置换
    loos = get_combs_loos_shadow(
        n_ru,
        combs,
        comb_avgs,
    )

    return θ, loos
end

function get_purity_loos_shadow(shadows::Vector{<:AbstractShadow}; kwargs...)
    return get_purity_loos_shadow(reshape(shadows, length(shadows), 1); kwargs...)
end


"""
由 shadow 数据估计一阶矩（期望值），并算 jackknife 估计。

参数
- shadows::Array{<:AbstractShadow, 2}：(n_ru, n_m) 的 shadow 数据。

关键词参数
- O::Union{Nothing, MPO}=nothing：在 trace product 求值中用的 MPO 算符
  （估计期望值时用）。
- show_progress::Bool=true：置换平均时是否显示进度。

返回
- θ：标量估计（平均期望值）。
- loos::Vector{Float64}：每个随机幺正的 leave-one-out jackknife 估计。
"""
function get_momnet1_loos_shadow(
    shadows::Array{<:AbstractShadow, 2};
    O::Union{Nothing, MPO}=nothing,
    show_progress::Bool=true,
)
    n_ru, _ = size(shadows)
    @assert n_ru ≥ 2 "At least 2 random unitaries are required for 1-moment estimation."
    combs = collect(combinations(1:n_ru, 1))

    # 每个置换对测量求平均
    comb_avgs = get_comb_avgs_shadow(shadows, 1; O=O, show_progress=show_progress)
    θ = mean(comb_avgs)

    # jackknife loo 分组：不含幺正 i 的置换
    loos = get_combs_loos_shadow(
        n_ru,
        combs,
        comb_avgs,
    )

    return θ, loos
end

function get_momnet1_loos_shadow(shadows::Vector{<:AbstractShadow}; kwargs...)
    return get_momnet1_loos_shadow(reshape(shadows, length(shadows), 1); kwargs...)
end

"""
把 reflect 和 purity 估计组合起来，算 z_r 估计子及其 jackknife 值。

参数
- shadows::Array{<:AbstractShadow, 2}：算 reflect 算符期望用的 shadow
  (n_ru, n_m)。
- odd_shadows::Array{<:AbstractShadow, 2}：其中一个纯度分区的 shadow。
- even_shadows::Array{<:AbstractShadow, 2}：另一个互补纯度分区的 shadow。
- reflect_op::MPO：算 reflect 期望用的算符。

关键词参数
- show_progress::Bool=true：置换平均时是否显示进度。

返回
- z_r_val::Float64：组合后的估计值。
- z_r_loos::Vector{Float64}：z_r 的 jackknife leave-one-out 估计。

说明
- z_r = R / sqrt((P_odd + P_even)/2)，其中 R 为 reflect 期望，
  P_odd/P_even 为两个纯度估计。
"""
function get_z_r_loos_shadow(
    shadows::Array{<:AbstractShadow, 2},
    odd_shadows::Array{<:AbstractShadow, 2},
    even_shadows::Array{<:AbstractShadow, 2},
    reflect_op::MPO,
    show_progress::Bool=true,
)
    # 预先枚举置换（和测量的笛卡尔积）
    n_ru, _ = size(shadows)
    @assert n_ru ≥ 3 "At least 3 random unitaries are required for z_r estimation."
    reflect_combs = collect(combinations(1:n_ru, 1))
    purity_combs = collect(combinations(1:n_ru, 2))

    # 每个置换对测量求平均
    reflect_comb_avgs = get_comb_avgs_shadow(
        shadows, 1; O=reflect_op, show_progress=show_progress
    )
    reflect_expect = mean(reflect_comb_avgs)
    odd_comb_avgs = get_comb_avgs_shadow(
        odd_shadows, 2; show_progress=show_progress
    )
    odd_expect = mean(odd_comb_avgs)
    even_comb_avgs = get_comb_avgs_shadow(
        even_shadows, 2; show_progress=show_progress
    )
    even_expect = mean(even_comb_avgs)

    # Loo 分组：leave-one-out。
    # 取 reflect 的 leave-one-out。
    reflect_loos = get_combs_loos_shadow(
        n_ru,
        reflect_combs,
        reflect_comb_avgs,
    )
    # 取 purity 的 leave-one-out。
    odd_loos = get_combs_loos_shadow(
        n_ru,
        purity_combs,
        odd_comb_avgs,
    )
    even_loos = get_combs_loos_shadow(
        n_ru,
        purity_combs,
        even_comb_avgs,
    )
    # 取 z_r_loos
    Z_R(R_I_val, P_I1, P_I2) = R_I_val / sqrt((P_I1 + P_I2) / 2)
    z_r_est = Z_R(reflect_expect, odd_expect, even_expect)
    z_r_loos = Z_R.(reflect_loos, odd_loos, even_loos)

    return z_r_est, z_r_loos
end

"""
向量版简便重载：把输入 reshape 成二维再转调主函数 get_z_r_loos_shadow。
"""
function get_z_r_loos_shadow(
    shadows::Array{<:AbstractShadow, 1},
    odd_shadows::Array{<:AbstractShadow, 1},
    even_shadows::Array{<:AbstractShadow, 1},
    reflect_op::MPO,
    show_progress::Bool=true,
)
    return get_z_r_loos_shadow(
        reshape(shadows, length(shadows), 1),
        reshape(odd_shadows, length(odd_shadows), 1),
        reshape(even_shadows, length(even_shadows), 1),
        reflect_op,
        show_progress,
    )
end

