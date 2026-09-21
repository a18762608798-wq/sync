import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


from optimize_branch import optimize_branch

end = [0.5, 0.5]
result, history = optimize_branch(end, history=[])
print(result, history)
