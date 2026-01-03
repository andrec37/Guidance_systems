# this is a 1 dimensional guidance system, designed to program a missile to track a target and hit it
# target: a plane
# what we are guiding: missile
import time
import matplotlib.pyplot as plt
#==============
#constraints
#==============
# Storage for plotting
positions = []
velocities = []
times = []
Accelerations = []

# target and missile state - missile mass = 1kg
target = 50 # where we want to go
position = 0 # where we are now
velocity = 0 # speed of the missile

# guidance and physics parameters
k = 9 # how aggressive the system is (acceleration strength)
damping = 2 * (k ** 0.5) # to reduce oscillations F = d*v where d is dampening and v is velocity, mass = 1kg - derived using a canonical formula to find the critical dampening value
tolerance = 0.01 # close enough
dt = 0.1 # step duration (sensors only measure every step)

#============
# functions
#============
def time_fn(base_fn):
    def time_base_fn():
        start = time.time()
        base_fn()
        end = time.time()
        print(f"\nTask Time: {end - start} Seconds")
    return time_base_fn

@time_fn
def guidance():
    global position
    global velocity
    t = 0
    t_max = 20
    while True:
        error = target - position # Line-of-sight error
        acceleration = k * error - damping * velocity#  guidance law (acceleration command)

        velocity += acceleration * dt # intergrate acceleration
        position += velocity * dt # intergrate velocity

        # store the data
        times.append(t)
        positions.append(position)
        velocities.append(velocity)
        Accelerations.append(acceleration)

        print(f"pos: {position:.5f}m")
        if abs(target - position) <= tolerance:
            break
        time.sleep(dt)
        t += dt
        if t > t_max:
            print("Timeout — intercept failed")
            break


guidance()

plt.figure(figsize=(10,5))

# Position
plt.subplot(3,1,1)
plt.plot(times, positions, label='Position')
plt.axhline(target, color='r', linestyle='--', label='Target')
plt.ylabel('Position (m)')
plt.legend()
plt.grid(True)

# Velocity
plt.subplot(3,1,2)
plt.plot(times, velocities, label='Velocity', color='g')
plt.ylabel('Velocity (m/s)')
plt.xlabel('Time (s)')
plt.legend()
plt.grid(True)

# Acceleration
plt.subplot(3,1,3)
plt.plot(times,
         Accelerations,
         label = 'Acceleration',
         color = 'k'
         )
plt.ylabel('Acceleration (m/s^2)')
plt.xlabel('Time (s)')
plt.legend()
plt.grid(True)
plt.show()