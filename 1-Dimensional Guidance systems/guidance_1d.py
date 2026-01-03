import time
import matplotlib.pyplot as plt

def time_fn(base_fn):
    def time_base_fn(*args, **kwargs):
        start = time.time()
        result = base_fn(*args, **kwargs)
        end = time.time()
        print(f"\nTask Time: {end - start:.3f} Seconds")
        return result
    return time_base_fn

@time_fn
def guidance(k, target=50.0, dt=0.05, tolerance=0.01, t_max=20):
    # missile state
    position = 0.0
    velocity = 0.0
    damping = 2 * (k ** 0.5)  # critical damping

    # storage for plotting
    positions = []
    velocities = []
    Accelerations = []
    times = []

    t = 0.0
    while True:
        error = target - position
        acceleration = k * error - damping * velocity

        velocity += acceleration * dt
        position += velocity * dt

        # store
        positions.append(position)
        velocities.append(velocity)
        Accelerations.append(acceleration)
        times.append(t)

        t += dt
        print(f"pos: {position:.5f}m")
        if abs(error) <= tolerance:
            break
        if t > t_max:
            print("Timeout — intercept failed")
            break
        time.sleep(dt)

    return {
        "position": positions,
        "velocity": velocities,
        "acceleration": Accelerations,
        "time": times,
        "intercept_time": t
    }

# Run simulation
result = guidance(k=5)

# Plot
plt.figure(figsize=(10,8))

plt.subplot(3,1,1)
plt.plot(result["time"], result["position"], label='Position')
plt.axhline(50, color='r', linestyle='--', label='Target')
plt.ylabel('Position (m)')
plt.legend()
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(result["time"], result["velocity"], label='Velocity', color='g')
plt.ylabel('Velocity (m/s)')
plt.legend()
plt.grid(True)

plt.subplot(3,1,3)
plt.plot(result["time"], result["acceleration"], label='Acceleration', color='k')
plt.ylabel('Acceleration (m/s²)')
plt.xlabel('Time (s)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
