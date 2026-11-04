#!/usr/bin/env julia

using Dates

# ---------- 常量配置 ----------
const LOG_FILE   = "/home/mintusr/.local/share/ya-provider/ya-provider_rCURRENT.log"
const CHECK_SECS = 5 * 60             # 每 10 分钟检查一次（单位：秒）
const START_PRICE = 0.01               # 起始 CPU 价 (GLM/hour)
const MIN_PRICE   = 0.0001
const MAX_PRICE   = 0.5
const UP_STEP     = 0.10               # 有单 +10%
const DOWN_STEP   = 0.10               # 无单 -10%

# 认为“有单/有需求”的关键词
const ORDER_KEYWORDS = (
    "ExeUnit initialized",            # 任务已真正启动
    "Reached Agreements limit: 1",    # 供不应求 → 也当作“有单”
)

# ⚠️ 排除关键词：仅在“未命中 ORDER_KEYWORDS”时才起效
# 命中这些词，代表确实在发生但还没到下单（例如协商阶段），按“无单”处理；如果一个都没出现，则视为“本轮不操作”
const EXCLUDE_KEYWORDS = (
    "negotiating Proposal",
)

# ---------- 工具函数 ----------
"""
返回：
true      → 命中 ORDER_KEYWORDS（涨价）
false     → 未命中 ORDER_KEYWORDS，但命中 EXCLUDE_KEYWORDS（降价）
:ignore   → 两者都没命中 / 读取异常（本轮不操作）
"""
function check_new_orders(log_path::String, since_time::DateTime)
    found_order   = false
    found_exclude = false

    try
        open(log_path, "r") do io
            for line in eachline(io)
                # 形如: [2025-10-17T21:31:01.972+0800 ...]
                if startswith(line, "[") && ncodeunits(line) >= 20
                    ts = tryparse(DateTime, line[2:20], dateformat"yyyy-mm-ddTHH:MM:SS")
                    if ts !== nothing && ts > since_time
                        # 1) 优先检查订单关键词
                        for k in ORDER_KEYWORDS
                            if occursin(k, line)
                                found_order = true
                                break
                            end
                        end
                        if found_order
                            break
                        end
                        # 2) 只有未命中订单关键词时，才检查排除关键词
                        for k in EXCLUDE_KEYWORDS
                            if occursin(k, line)
                                found_exclude = true
                                break
                            end
                        end
                        # 不 break 整个循环，继续看后续行是否会出现订单关键词
                    end
                end
            end
        end
    catch e
        @warn "读取/解析日志失败" error=e
        return :ignore
    end

    if found_order
        return true
    elseif found_exclude
        return false
    else
        return :ignore
    end
end

clamp_price(p) = max(MIN_PRICE, min(MAX_PRICE, p))

# ---------- 主逻辑 ----------
function main()
    cmd = `golemsp settings set --cpu-per-hour $(START_PRICE)`
    try
        run(cmd)
    catch e
        @warn "执行 golemsp 命令失败" error=e
    end
    println("执行命令: ", cmd)
    println("开始自动调价，每 $(div(CHECK_SECS,60)) 分钟检查一次，初始价格为：$(START_PRICE)")

    # 局部状态
    adj_param = 3
    adj_max = 5
    last_status = 1
    cpu_price  = START_PRICE
    last_check = now() - Second(CHECK_SECS)

    while true
        sleep(CHECK_SECS)
        state = check_new_orders(LOG_FILE, last_check)
        last_check = now()

        # :ignore → 本轮不调整、不执行命令
        if state == :ignore
            println("⏸️ 未命中订单关键词且无排除关键词，本轮不操作。")
            continue
        end

        if state == true
            if last_status == 1
                adj_param += 1
            else
                adj_param = 1
            end
            last_status = 1
            cpu_price *= (1 + UP_STEP * adj_param)
            cpu_price = clamp_price(cpu_price)
            println("✅ 检测到接单/需求旺盛，上调 CPU 价格, current price -> $(cpu_price)")
        elseif state == false  # state === false
            if last_status == 0
                adj_param += 1
            else
                adj_param = 1
            end
            last_status = 0
            cpu_price *= (1 - DOWN_STEP * adj_param)
            cpu_price = clamp_price(cpu_price)
            println("⚠️ 最近无单（仅见排除关键词），下调 CPU 价格, current price -> $(cpu_price)")
        end

        adj_param = min(adj_param, adj_max)

        cmd = `golemsp settings set --cpu-per-hour $(cpu_price)`
        println("执行命令: ", cmd)
        try
            run(cmd)
        catch e
            @warn "执行 golemsp 命令失败" error=e
        end
    end
end

main()

