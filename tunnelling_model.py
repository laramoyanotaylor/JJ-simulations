import numpy as np

MESH_FILE = "junction_mesh.csv"
OUTPUT_FILE = "junction_tunnelling.csv"

# Placeholder parameters for a sensitivity study, not calibrated device values.
BARRIER_HEIGHT_EV = 1.5
EFFECTIVE_MASS_RATIO = 0.4
ELECTRON_MASS_KG = 9.1093837e-31
ELECTRONVOLT_J = 1.602176634e-19
HBAR_JS = 1.054571817e-34

mesh = np.genfromtxt(MESH_FILE, delimiter=",", names=True)
thickness_nm = mesh["Local_Thickness"]

if np.any(thickness_nm <= 0):
    raise ValueError("The mesh contains non-positive oxide thickness values")

barrier_height_j = BARRIER_HEIGHT_EV * ELECTRONVOLT_J
effective_mass_kg = EFFECTIVE_MASS_RATIO * ELECTRON_MASS_KG
kappa_per_m = np.sqrt(2 * effective_mass_kg * barrier_height_j) / HBAR_JS
kappa_per_nm = kappa_per_m * 1e-9

# Normalize at the mean thickness so this test reports relative current only.
mean_thickness_nm = thickness_nm.mean()
relative_transmission = np.exp(
    -2 * kappa_per_nm * (thickness_nm - mean_thickness_nm)
)
relative_current = relative_transmission.mean()

output = np.column_stack((mesh["X"], thickness_nm, relative_transmission))
np.savetxt(
    OUTPUT_FILE,
    output,
    delimiter=",",
    header="X,Local_Thickness,Relative_Tunnelling_Weight",
    comments="",
)

print("[TUNNELLING] Relative WKB sensitivity model")
print(f"[TUNNELLING] barrier height: {BARRIER_HEIGHT_EV:.2f} eV (placeholder)")
print(f"[TUNNELLING] effective mass: {EFFECTIVE_MASS_RATIO:.2f} m_e (placeholder)")
print(f"[TUNNELLING] kappa: {kappa_per_nm:.3f} per nm")
print(f"[TUNNELLING] thickness range: {thickness_nm.min():.3f} to {thickness_nm.max():.3f} nm")
print(f"[TUNNELLING] relative weight range: {relative_transmission.min():.3e} to {relative_transmission.max():.3e}")
print(f"[TUNNELLING] junction-average relative current: {relative_current:.3f}")
print(f"[TUNNELLING] wrote {OUTPUT_FILE}")
