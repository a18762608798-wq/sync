# Run a Python script inside the project's CondaPkg environment.
#
#   julia --project=. scripts/run_py.jl scripts/plot_D02.py [args...]
#
# On Windows, calling the env's python.exe directly leaves `<env>\Library\bin`
# off PATH. Matplotlib imports fine, but the Agg backend then fails at draw
# time with a delay-load error (exit 0xC06D007F). CondaPkg.withenv() prepends
# the environment's bin directories, which is the supported way to launch it.

using CondaPkg

isempty(ARGS) && error("usage: julia --project=. scripts/run_py.jl <script.py> [args...]")
script = ARGS[1]
args = ARGS[2:end]

CondaPkg.withenv() do
    run(`$(CondaPkg.which("python")) $script $args`)
end
