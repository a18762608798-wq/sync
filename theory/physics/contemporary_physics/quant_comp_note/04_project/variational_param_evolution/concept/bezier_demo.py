from pathlib import Path


import numpy as np
import matplotlib.pyplot as plt


def quadratic_bezier(p0, pc, p1, n=100):
    t = np.linspace(0, 1, n)
    return (
        (1 - t) ** 2 * np.array(p0)[:, None]
        + 2 * t * (1 - t) * np.array(pc)[:, None]
        + t**2 * np.array(p1)[:, None]
    )


p0 = np.array([0.2, 0.08])  # start: (s=0.2, delta=0.08)
p1 = np.array([0.6, -0.04])  # end:   (s=0.6, delta=-0.04)

control_points = [
    ([0.4, 0.10], "bend up"),
    ([0.4, -0.06], "bend down"),
    ([0.28, 0.12], "bend early"),
    ([0.52, 0.00], "bend late"),
]

fig, axes = plt.subplots(1, len(control_points), figsize=(14, 3.5))
for ax, (pc, label) in zip(axes, control_points):
    curve = quadratic_bezier(p0, pc, p1)
    ax.plot(curve[0], curve[1], "b-", linewidth=2)
    ax.scatter(*p0, color="green", s=50, zorder=5, label="start")
    ax.scatter(*p1, color="red", s=50, zorder=5, label="end")
    ax.scatter(*pc, color="gray", s=40, zorder=4, marker="x", label="control")
    ax.set_title(label)
    ax.set_xlabel("s")
    ax.set_ylabel("δ")
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    ax.set_aspect("equal")

plt.tight_layout()
HERE = Path(__file__).resolve().parent
path = HERE / "pics/bezier_demo.png"
plt.savefig(path, dpi=150)
print("saved bezier_demo.png")
