import numpy as np

MESH_FILE = "junction_mesh.csv"
EXPECTED_THICKNESS_NM = 1.5
EXPECTED_INTERFACE_ROUGHNESS_NM = 0.15

mesh = np.genfromtxt(MESH_FILE, delimiter=",", names=True)
required_columns = {"X", "Z_Bottom", "Z_Top", "Local_Thickness"}
missing_columns = required_columns.difference(mesh.dtype.names or ())
if missing_columns:
    raise ValueError(f"Missing mesh columns: {sorted(missing_columns)}")

x = mesh["X"]
bottom = mesh["Z_Bottom"]
top = mesh["Z_Top"]
thickness = mesh["Local_Thickness"]

if not np.all(np.isfinite(thickness)):
    raise ValueError("Mesh contains non-finite thickness values")
if not np.all(thickness > 0):
    raise ValueError("Mesh contains non-positive oxide thickness values")
if not np.allclose(thickness, top - bottom):
    raise ValueError("Local_Thickness does not match Z_Top - Z_Bottom")

spacing = np.diff(x)
print(f"[MESH] points: {len(x)}")
print(f"[MESH] length: {x[-1] - x[0]:.3f} nm")
print(f"[MESH] spacing: {spacing.mean():.5f} nm (constant={np.allclose(spacing, spacing[0])})")
print(f"[MESH] thickness range: {thickness.min():.5f} to {thickness.max():.5f} nm")
print(f"[MESH] thickness mean: {thickness.mean():.5f} nm (target={EXPECTED_THICKNESS_NM:.2f} nm)")
print(f"[MESH] thickness standard deviation: {thickness.std(ddof=1):.5f} nm")
print(
    "[MESH] expected independent-interface standard deviation: "
    f"{np.sqrt(2) * EXPECTED_INTERFACE_ROUGHNESS_NM:.5f} nm"
)
print("[MESH] validation passed")
