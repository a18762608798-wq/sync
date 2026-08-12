import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from objective import objective, robust_objective

t = [0, 0, 0]
end = [0.5, 0.5]

evs = objective(
    t,
    end,
)
print(evs)

evs = robust_objective(t, end)

print(evs)
