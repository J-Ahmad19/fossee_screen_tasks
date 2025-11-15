# Imports
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
ds = xr.open_dataset("screening_task1.nc")   # <--- change this

# The single data variable is 'forces' with dims like ('Element','Component')
F = ds["forces"]

# Inspect available labels so we know how to select
elem_dim, comp_dim = F.dims  # should be something like ('Element','Component')
elements_all = F.coords[elem_dim].values
components_all = F.coords[comp_dim].values
print("Dims:", F.dims)
print("Num elements:", len(elements_all))
print("Components:", components_all)

# Helper to find component names robustly
def find_component(cands):
    """
    Return the first Component label that contains ANY of the candidate substrings (case-insensitive).
    Example: find_component(['Mz_i','Mz i','Mz (i)','Mzi'])
    """
    labels = [str(x) for x in F.coords[comp_dim].values]
    low = [s.lower() for s in labels]
    for cand in cands:
        c = cand.lower()
        for lab, l in zip(labels, low):
            if c in l:
                return lab
    raise KeyError(f"Could not find any of {cands} in Component labels: {labels}")

# Try common variants (adjust/add if your labels differ)
name_Mz_i = find_component(["Mz_i","Mz i","MZ_I","Mz(i)","Mz-i","Mzi"])
name_Mz_j = find_component(["Mz_j","Mz j","MZ_J","Mz(j)","Mz-j","Mzj"])
name_Vy_i = find_component(["Vy_i","Vy i","VY_I","Vy(i)","Vy-i","Vyi"])
name_Vy_j = find_component(["Vy_j","Vy j","VY_J","Vy(j)","Vy-j","Vyj"])

print("Detected columns:",
      name_Mz_i, name_Mz_j, name_Vy_i, name_Vy_j)

# Central longitudinal girder element IDs (in the order along the girder)
girder_ids = [15, 24, 33, 42, 51, 60, 69, 78, 83]

# Some datasets store element IDs as strings; ensure the same dtype
elements_all_cast = elements_all.astype(type(girder_ids[0]))
missing = [e for e in girder_ids if e not in set(elements_all_cast)]
if missing:
    raise ValueError(f"These element IDs not found in dataset: {missing}")

# Slice only those elements, in the given order
sub = F.sel({elem_dim: girder_ids})

#  Pull i/j end values for Mz and Vy
Mz_i = sub.sel({comp_dim: name_Mz_i}).values.astype(float)
Mz_j = sub.sel({comp_dim: name_Mz_j}).values.astype(float)
Vy_i = sub.sel({comp_dim: name_Vy_i}).values.astype(float)
Vy_j = sub.sel({comp_dim: name_Vy_j}).values.astype(float)

#  Build node-wise lines:
# Start with _i of first element; then append _j of each element in sequence
Mz_line = np.array([Mz_i[0], *Mz_j])
Vy_line = np.array([Vy_i[0], *Vy_j])

# Build the x-axis (chainage)

L = None  # <-- set to an array of lengths (m) if data have them
if L is None:
    chainage = np.arange(len(girder_ids)+1, dtype=float)  # 0..N
else:
    L = np.asarray(L, dtype=float)
    assert L.shape[0] == len(girder_ids)
    chainage = np.concatenate([[0.0], np.cumsum(L)])


# Utilities for max/min labels and nice formatting
def annotate_extrema(ax, chainage, y, units, where="right"):
    i_max = int(np.nanargmax(y))
    i_min = int(np.nanargmin(y))
    # Max
    ax.annotate(f"Max: {y[i_max]:.2f} {units}",
                xy=(chainage[i_max], y[i_max]),
                xytext=(chainage[-1] if where=="right" else chainage[0], y[i_max]),
                textcoords="data",
                ha="right" if where=="right" else "left",
                va="bottom",
                arrowprops=dict(arrowstyle="->", lw=0.8))
    # Min (only if distinct)
    if i_min != i_max:
        ax.annotate(f"Min: {y[i_min]:.2f} {units}",
                    xy=(chainage[i_min], y[i_min]),
                    xytext=(chainage[0] if where=="right" else chainage[-1], y[i_min]),
                    textcoords="data",
                    ha="left" if where=="right" else "right",
                    va="top",
                    arrowprops=dict(arrowstyle="->", lw=0.8))

# Plots (clean, exam-friendly)

# Bending Moment Diagram
plt.figure()
plt.plot(chainage, Mz_line, marker="o", color="red")

# Add vertical lines for better visibility
for xi , bm in zip(chainage , Mz_line ):
    plt.vlines ( xi , 0 , bm , colors ='red', linestyles ='solid',
    linewidth =1)

plt.axhline(0, linewidth=1)
plt.xlabel("Distance(m)")
plt.ylabel("Bending moment Mz (kN·m)")
plt.title("Bending Moment Diagram – Central Longitudinal Girder\n(Signs per solver’s local axes)")
plt.grid(True)
annotate_extrema(plt.gca(), chainage, Mz_line, "kN·m", where="right")
plt.tight_layout()
plt.savefig("BMD_central_girder.png", dpi=220)

# Shear Force Diagram

plt.figure()
plt.plot(chainage, Vy_line, marker="o", color="blue")
# Add vertical lines for better visibility
for xi , sf in zip(chainage , Vy_line ):
    plt.vlines ( xi , 0 , sf , colors ='blue', linestyles ='solid',
    linewidth =1)
plt.axhline(0, linewidth=1)
plt.xlabel("Distance(m)")
plt.ylabel("Shear force Vy (kN)")
plt.title("Shear Force Diagram – Central Longitudinal Girder\n(Signs per solver’s local axes)")
plt.grid(True)
annotate_extrema(plt.gca(), chainage, Vy_line, "kN", where="right")
plt.tight_layout()
plt.savefig("SFD_central_girder.png", dpi=220)

# Optional: export table for submission
df = pd.DataFrame({"chainage": chainage, "Mz": Mz_line, "Vy": Vy_line})
df.to_csv("central_girder_Mz_Vy.csv", index=False)
print("Saved: BMD_central_girder.png, SFD_central_girder.png, central_girder_Mz_Vy.csv")
