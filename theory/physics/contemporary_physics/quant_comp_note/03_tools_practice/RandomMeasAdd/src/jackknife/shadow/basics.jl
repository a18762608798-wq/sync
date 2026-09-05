# ---------------------
# shadow 基础组件：置换平均 + leave-one-out
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
- is_show_progress::Bool=true：是否显示进度。

返回
- Array{Float64}，长度 choose(n_ru, k)：每个 k 置换在测量笛卡尔积上
  平均后的 trace-product 均值。
"""
function get_comb_avgs_shadow(
    shadows::Array{<:AbstractShadow, 2},
    k::Int;
    O::Union{Nothing, MPO}=nothing,
    is_show_progress=false,
)
    @assert (k == 2 && isnothing(O)) || (k == 1) "O must be nothing for k=2, and k in the range of [1, 2]"

    # 预先枚举置换和测量笛卡尔积
    n_ru, n_m = size(shadows)
    combs = collect(combinations(1:n_ru, k))
    cprod = collect(CartesianIndices(ntuple(_ -> 1:n_m, k)))
    combs_num = length(combs)

    # 每个置换对测量求平均
    comb_avgs = zeros(Float64, combs_num)
    @showprogress desc="Combinations Processing..." enabled=is_show_progress @threads for pidx in eachindex(combs)
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
