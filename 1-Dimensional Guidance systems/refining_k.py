import guidance_1d
import matplotlib.pyplot as plt
k_values = [0.5, 1, 2, 5, 10, 20, 30, 40, 50, 60]
results = {}

for k in k_values:
    results[k] = guidance_1d.guidance(k)
    print(f"k={k}, intercept time={results[k]['intercept_time']:.3f} s")

# Find the k with minimum intercept time
best_k = min(results, key=lambda x: results[x]['intercept_time'])
print(f"Optimal k: {best_k} → intercept time: {results[best_k]['intercept_time']:.3f} s")

# =========================
# Plot positions for all k
# =========================
plt.figure(figsize=(12,6))
for k in k_values:
    plt.plot(results[k]['time'], results[k]['position'], label=f'k={k}')

plt.axhline(50, color='r', linestyle='--', label='Target')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Missile Position vs Time for Different k Values')
plt.legend()
plt.grid(True)
plt.show()