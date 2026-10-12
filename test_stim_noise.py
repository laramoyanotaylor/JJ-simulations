import stim
import numpy as np

# physical error rate needs to be calculated
# using c++ mesh data
t_gate = 40e-9
T_phi = 15e-6
p_z = (1 - np.exp(-t_gate / T_phi)) / 2 # physical phase flip error rate

print("="*60)
print("Materials-to-qec bridging simulator")
print("="*60)
print(f"[PHYSICS] Calculates physical z-type error rate per gate cycle: {p_z:.6f}")

#build a stim circuit with noise
circuit = stim.Circuit()

#initialise data
circuit.append("R", [0, 1, 2, 3, 4])

#add material induced
circuit.append("Z_ERROR", [0, 1, 2], p_z)

#add cx gates 
circuit.append("H", [0, 1, 2])
circuit.append("CX", [0, 3, 1, 4])
circuit.append("CX", [1, 3, 2, 4])
circuit.append("H", [0, 1, 2])

#measure ancilla qubits
circuit.append("M", [3, 4])

circuit.append("DETECTOR", [stim.target_rec(-2)], [0])
circuit.append("DETECTOR", [stim.target_rec(-1)], [1])

#sample circuit
sampler = circuit.compile_sampler()
shots = 1000
samples = sampler.sample(shots=shots)

#logical errors and rate 
error_detected_count = np.sum(np.any(samples, axis=1))
detection_rate = (error_detected_count / shots) * 100

print(f"[STIM]   Compiled circuit and ran {shots} simulation shots.")
print(f"[SYSTEM] Syndromes detected errors in {detection_rate:.2f}% of execution cycles.")
print("="*60)
print("\nFirst 5 syndrome measurement samples (0 = Clean, 1 = Error Detected):")
print(samples[:5])

